# src/mindbank_poc/api/routers/retrieval.py
from typing import Any, Dict, List, Optional
from fastapi import APIRouter, HTTPException, Depends, Query
from pydantic import BaseModel, Field
from datetime import datetime

from mindbank_poc.api.schemas import AggregateInput, NormalizedUnitSchema, FilterRequest, SegmentSearchResponse, SegmentSearchResultItem, SegmentSchema, SegmentFilterRequest
from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.retrieval.service import get_retrieval_service, RetrievalService, SearchResultItemInternal
from mindbank_poc.core.retrieval.cluster_retrieval import get_cluster_retrieval_service
from mindbank_poc.core.retrieval.segment_retrieval import get_segment_retrieval_service
from mindbank_poc.core.knowledge_store import get_knowledge_store

router = APIRouter(
    prefix="/retrieval",
    tags=["retrieval"],
    responses={404: {"description": "Not found"}},
)

logger = get_logger(__name__)

# Модель запроса поиска
class SearchRequest(BaseModel):
    """Схема для запроса поиска."""
    query_text: Optional[str] = Field(
        default=None,
        description="Текст запроса для поиска"
    )
    filters: Optional[Dict[str, Any]] = Field(
        default=None,
        description="Фильтры по метаданным"
    )
    archetype: Optional[str] = Field(
        default=None,
        description="Фильтр по архетипу"
    )
    mode: str = Field(
        default="hybrid",
        description="Режим поиска: 'semantic', 'fulltext', 'hybrid'"
    )
    limit: int = Field(
        default=10,
        description="Максимальное количество результатов"
    )

# Модель результата поиска
class SearchResultItem(BaseModel):
    """Схема для результата поиска."""
    score: float = Field(
        description="Релевантность результата (от 0 до 1)"
    )
    normalized_unit: NormalizedUnitSchema = Field(
        description="Нормализованная единица знаний"
    )
    raw_aggregate: Optional[AggregateInput] = Field(
        default=None,
        description="Исходный агрегат"
    )

# Модель ответа API поиска
class SearchResponse(BaseModel):
    """Схема для ответа API поиска."""
    results: List[SearchResultItem] = Field(
        default_factory=list,
        description="Список результатов поиска"
    )

@router.post("/search", response_model=SearchResponse)
async def search_normalized_units(
    request: SearchRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service)
):
    """
    Выполняет поиск по нормализованным данным.
    
    - Можно указать текст для поиска (query_text)
    - Можно указать фильтры по метаданным (filters)
    - Можно указать фильтр по архетипу (archetype)
    - Можно выбрать режим поиска: семантический, полнотекстовый или гибридный
    - Можно ограничить количество результатов (limit)
    """
    try:
        # Вызываем сервис поиска
        internal_results: List[SearchResultItemInternal] = await retrieval_service.search(
            query_text=request.query_text,
            metadata_filters=request.filters,
            archetype=request.archetype,
            search_mode=request.mode,
            limit=request.limit
        )

        # Преобразуем внутренние результаты в схему ответа API
        api_results: List[SearchResultItem] = []
        for item in internal_results:
            # Проверяем, что агрегат был найден (на случай ошибок при загрузке)
            if item.raw_aggregate:
                 # Создаем копию NormalizedUnitSchema с уникальным ID если нужно
                 unit_schema = NormalizedUnitSchema.model_validate(item.unit)
                 
                 # Если такой aggregate_id уже был добавлен в результаты, сделаем его уникальным
                 existing_ids = [r.normalized_unit.aggregate_id for r in api_results]
                 if unit_schema.aggregate_id in existing_ids:
                     # Добавляем уникальный суффикс к ID для API ответа
                     unique_suffix = f"-{id(item.unit)}"
                     unit_schema.aggregate_id = f"{unit_schema.aggregate_id}{unique_suffix}"
                     logger.info(f"Made aggregate_id unique for API: {unit_schema.aggregate_id}")
                 
                 api_results.append(
                     SearchResultItem(
                         score=item.score,
                         normalized_unit=unit_schema,
                         raw_aggregate=item.raw_aggregate # AggregateInput уже является Pydantic схемой
                     )
                 )

        return SearchResponse(results=api_results)
    except Exception as e:
        logger.error(f"Error during search: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

@router.post("/filter", response_model=SearchResponse)
async def filter_normalized_units(
    request: FilterRequest,
    retrieval_service: RetrievalService = Depends(get_retrieval_service)
):
    """
    Выполняет поиск по нормализованным данным только по фильтрам без текстового запроса.
    
    - Можно указать архетип контента (архетип)
    - Можно указать источник данных (source)
    - Можно указать автора контента (author)
    - Можно указать диапазон дат создания (date_from, date_to)
    - Можно указать типы классификации (classification_types)
    - Можно указать дополнительные метаданные (custom_metadata)
    - Можно указать теги (tags)
    - Можно указать максимальное количество результатов (limit)
    - Можно указать поле и порядок сортировки (sort_by, sort_order)
    """
    try:
        logger.info(f"API filter_normalized_units called with: source={request.source}, limit={request.limit}")
        
        # Вызываем сервис фильтрации
        internal_results: List[SearchResultItemInternal] = await retrieval_service.filter_search(
            archetype=request.archetype,
            source=request.source,
            source_name=request.source_name,
            author=request.author,
            date_from=request.date_from,
            date_to=request.date_to,
            classification_types=request.classification_types,
            custom_metadata=request.custom_metadata,
            tags=request.tags,
            limit=request.limit,
            sort_by=request.sort_by,
            sort_order=request.sort_order
        )

        logger.info(f"API filter_search returned {len(internal_results)} internal results")

        # Преобразуем внутренние результаты в схему ответа API
        api_results: List[SearchResultItem] = []
        for i, item in enumerate(internal_results):
            logger.debug(f"Processing internal result {i}: raw_aggregate is {'present' if item.raw_aggregate else 'None'}")
            
            # Создаем копию NormalizedUnitSchema с уникальным ID если нужно
            unit_schema = NormalizedUnitSchema.model_validate(item.unit)
            
            # Если такой aggregate_id уже был добавлен в результаты, сделаем его уникальным
            existing_ids = [r.normalized_unit.aggregate_id for r in api_results]
            if unit_schema.aggregate_id in existing_ids:
                # Добавляем уникальный суффикс к ID для API ответа
                unique_suffix = f"-{id(item.unit)}"
                unit_schema.aggregate_id = f"{unit_schema.aggregate_id}{unique_suffix}"
                logger.info(f"Made aggregate_id unique for API: {unit_schema.aggregate_id}")
            
            # Создаем fallback агрегат если исходный не найден
            raw_aggregate = item.raw_aggregate
            if raw_aggregate is None:
                logger.info(f"Creating fallback aggregate for unit {item.unit.id}")
                # Создаем минимальный агрегат на основе нормализованной единицы
                raw_aggregate = AggregateInput(
                    id=item.unit.aggregate_id or f"fallback-{item.unit.id}",
                    group_id=item.unit.group_id or "unknown",
                    entries=[],  # Пустой список entries для fallback
                    metadata={
                        "source": item.unit.metadata.get("source", "unknown"),
                        "source_name": item.unit.metadata.get("source_name"),
                        "author": item.unit.metadata.get("author"),
                        "created_at": item.unit.created_at.isoformat() if item.unit.created_at else None,
                        "archetype": item.unit.archetype,
                        "fallback": True  # Помечаем как fallback агрегат
                    }
                )
            
            api_results.append(
                SearchResultItem(
                    score=item.score,
                    normalized_unit=unit_schema,
                    raw_aggregate=raw_aggregate
                )
            )

        logger.info(f"API returning {len(api_results)} results out of {len(internal_results)} internal results")
        return SearchResponse(results=api_results)
    except Exception as e:
        logger.error(f"Error during filter search: {e}")
        raise HTTPException(
            status_code=500,
            detail=f"Internal server error: {str(e)}"
        )

# ------------------------------------------------------------
# Новый эндпойнт: поиск сегментов через кластеры
# ------------------------------------------------------------

@router.post("/search_segments", response_model=SegmentSearchResponse, status_code=200)
async def search_segments(
    query: str = Query(..., description="Текст запроса"),
    k: int = Query(5, description="Количество кластеров"),
    m: int = Query(20, description="Количество сегментов"),
):
    """Двухшаговый поиск: сначала выбираем TOP-K кластеров, затем TOP-M сегментов.
    """
    try:
        cluster_service = await get_cluster_retrieval_service()
        clusters_scored = await cluster_service.search_clusters(query_text=query, k=k)
        if not clusters_scored:
            return SegmentSearchResponse(results=[])

        cluster_ids = [c.id for c, _ in clusters_scored]

        segment_service = await get_segment_retrieval_service()
        segments_scored = await segment_service.search_segments(query_text=query, cluster_ids=cluster_ids, m=m)

        api_results: List[SegmentSearchResultItem] = []
        ks = get_knowledge_store()
        for seg, score in segments_scored:
            # собираем полный текст
            full_text_parts = []
            try:
                for uid in seg.raw_unit_ids:
                    unit = await ks.get(uid)
                    if unit and getattr(unit, "text_repr", None):
                        full_text_parts.append(unit.text_repr)
            except Exception as e:
                logger.error(f"Error building full_text for segment {seg.id}: {e}")

            api_seg = SegmentSchema(
                id=seg.id,
                cluster_id=None,  # заполним позже при необходимости
                title=seg.title,
                summary=seg.summary,
                group_id=seg.group_id,
                entity_count=len(seg.entities),
                unit_count=len(seg.raw_unit_ids),
                created_at=seg.created_at,
                full_text="\n".join(full_text_parts) if full_text_parts else None,
            )
            api_results.append(SegmentSearchResultItem(score=round(score, 3), segment=api_seg))

        return SegmentSearchResponse(results=api_results)
    except Exception as e:
        logger.error(f"Error in /search_segments: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail="Internal error")

@router.post("/filter_segments", response_model=SegmentSearchResponse, status_code=200)
async def filter_segments(
    request: SegmentFilterRequest,
):
    """
    Фильтрует сегменты по метаданным без текстового поиска.
    
    Позволяет агенту получать сегменты по различным критериям:
    - По группе (например, конкретный чат или источник)
    - По содержимому заголовка или резюме
    - По наличию определенных сущностей
    - По количеству юнитов в сегменте
    - По дате создания (можно получить последний митинг, первый за период и т.д.)
    
    Примеры использования:
    - Получить последний митинг: sort_by="created_at", sort_order="desc", limit=1
    - Получить митинги за вчера: date_from="2023-12-01T00:00:00Z", date_to="2023-12-01T23:59:59Z"
    - Найти митинги с упоминанием API: entity_contains="API"
    """
    try:
        ks = get_knowledge_store()
        
        # Вызываем метод фильтрации сегментов
        segments = await ks.filter_segments(
            group_id=request.group_id,
            source=request.source,
            source_name=request.source_name,
            title_contains=request.title_contains,
            summary_contains=request.summary_contains,
            entity_contains=request.entity_contains,
            min_unit_count=request.min_unit_count,
            max_unit_count=request.max_unit_count,
            date_from=request.date_from.isoformat() if request.date_from else None,
            date_to=request.date_to.isoformat() if request.date_to else None,
            limit=request.limit,
            sort_by=request.sort_by,
            sort_order=request.sort_order
        )
        
        # Преобразуем в API-схему
        api_results: List[SegmentSearchResultItem] = []
        for segment in segments:
            # Собираем полный текст сегмента
            full_text_parts = []
            try:
                for unit_id in segment.raw_unit_ids:
                    unit = await ks.get(unit_id)
                    if unit and getattr(unit, "text_repr", None):
                        full_text_parts.append(unit.text_repr)
            except Exception as e:
                logger.error(f"Error building full_text for segment {segment.id}: {e}")
            
            api_segment = SegmentSchema(
                id=segment.id,
                cluster_id=None,  # Заполним при необходимости
                title=segment.title,
                summary=segment.summary,
                group_id=segment.group_id,
                entity_count=len(segment.entities),
                unit_count=len(segment.raw_unit_ids),
                created_at=segment.created_at,
                full_text="\n".join(full_text_parts) if full_text_parts else None,
            )
            
            # Для фильтрации score всегда 1.0 (нет семантического поиска)
            api_results.append(SegmentSearchResultItem(score=1.0, segment=api_segment))
        
        logger.info(f"Filter segments returned {len(api_results)} results")
        return SegmentSearchResponse(results=api_results)
        
    except Exception as e:
        logger.error(f"Error in /filter_segments: {e}", exc_info=True)
        raise HTTPException(status_code=500, detail=f"Internal error: {str(e)}")
