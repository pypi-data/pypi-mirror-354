"""
Реализация хранилища знаний на основе ChromaDB.
"""
import os
import json
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, List, Tuple, Union, Set
import uuid
import asyncio
import aiofiles

import chromadb
from chromadb.config import Settings
from chromadb.utils import embedding_functions

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings
from .base import BaseKnowledgeStore
from ..normalizer.models import NormalizedUnit
from ..enrichment.models import SegmentModel, ClusterModel

# Получаем логгер
logger = get_logger(__name__)


class ChromaKnowledgeStore(BaseKnowledgeStore):
    """
    Реализация хранилища знаний на основе ChromaDB.
    
    Использует ChromaDB для эффективного векторного поиска и хранения нормализованных юнитов.
    Преимущества по сравнению с JSONL:
    - Оптимизированный векторный поиск
    - Сохранение/загрузка данных без необходимости хранить все в памяти
    - Поддержка метаданных для фильтрации
    - Улучшенная масштабируемость
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Инициализация хранилища.
        
        Args:
            config: Конфигурация хранилища, может содержать:
                   - data_dir: путь к директории для хранения данных
                   - collection_name: имя коллекции в ChromaDB
        """
        super().__init__(config or {})
        
        # Директория для хранения данных
        self.data_dir = Path(self.config.get("data_dir", settings.storage.knowledge_dir))
        self.data_dir.mkdir(exist_ok=True, parents=True)
        
        # Имя коллекции
        self.collection_name = self.config.get("collection_name", "normalized_units")
        
        # Путь к ChromaDB
        self.chroma_path = self.data_dir / "chroma_db"
        self.chroma_path.mkdir(exist_ok=True, parents=True)
        
        # Логгирование инициализации
        logger.info(f"ChromaKnowledgeStore initialized. Data directory: {self.data_dir.resolve()}")
        logger.info(f"ChromaDB path: {self.chroma_path.resolve()}")
        logger.info(f"Collection name: {self.collection_name}")
        
        # Инициализация клиента ChromaDB (persistent)
        self.client = chromadb.PersistentClient(
            path=str(self.chroma_path.resolve()),
            settings=Settings(
                anonymized_telemetry=False
            )
        )
        
        # Получение или создание коллекции
        try:
            # Создаем функцию эмбеддингов None, чтобы отключить встроенную функцию эмбеддингов
            # Это важно, так как мы хотим использовать только наши собственные эмбеддинги от OpenAI
            self.collection = self.client.get_or_create_collection(
                name=self.collection_name,
                metadata={"description": "Нормализованные единицы знаний"},
                embedding_function=None  # Отключаем встроенную функцию эмбеддингов
            )
            logger.info(f"ChromaKnowledgeStore: Collection '{self.collection_name}' ready")
        except Exception as e:
            logger.error(f"Error initializing ChromaDB collection: {e}", exc_info=True)
            raise
    
    async def store(self, unit: NormalizedUnit) -> str:
        """
        Сохраняет нормализованную единицу в хранилище.
        
        Args:
            unit: Нормализованная единица для сохранения
            
        Returns:
            Идентификатор сохраненной единицы (unit.id)
        """
        try:
            # Идентификатор для ChromaDB (используем unit.id)
            doc_id = unit.id
            
            # Текстовое представление для поиска
            document = unit.text_repr
            
            # Векторное представление (если есть)
            embedding = unit.vector_repr
            
            # Метаданные для хранения и фильтрации
            metadata = {
                "unit_id": unit.id,
                "aggregate_id": unit.aggregate_id,
                "group_id": unit.group_id,
                "normalized_at": unit.normalized_at.isoformat(),
                "archetype": unit.archetype,  # 🎯 ДОБАВЛЯЕМ АРХЕТИП!
                # Копируем классификацию в метаданные для фильтрации
                **{f"class_{k}": str(v) for k, v in unit.classification.items()},
                # Копируем метаданные юнита для фильтрации (только строковые и числовые)
                **{k: str(v) if not isinstance(v, (int, float, bool, str)) else v 
                   for k, v in unit.metadata.items() 
                   if v is not None}
            }
            
            # Сохраняем полный объект как JSON в документе
            full_unit_json = unit.model_dump_json()
            
            # Проверяем, существует ли документ с таким ID
            try:
                existing = self.collection.get(ids=[doc_id])
                if existing and existing['ids']:
                    # Если существует, обновляем
                    logger.info(f"Updating existing unit with ID {doc_id}")
                    self.collection.update(
                        ids=[doc_id],
                        embeddings=[embedding] if embedding else None,
                        metadatas=[metadata],
                        documents=[full_unit_json]
                    )
                else:
                    # Если не существует, добавляем
                    logger.info(f"Adding new unit with ID {doc_id}")
                    self.collection.add(
                        ids=[doc_id],
                        embeddings=[embedding] if embedding else None,
                        metadatas=[metadata],
                        documents=[full_unit_json]
                    )
            except Exception as e:
                # Если произошла ошибка (например, коллекция пуста), добавляем
                logger.warning(f"Error checking existence, adding as new: {e}")
                self.collection.add(
                    ids=[doc_id],
                    embeddings=[embedding] if embedding else None,
                    metadatas=[metadata],
                    documents=[full_unit_json]
                )
            
            logger.info(f"Stored unit with ID {doc_id} in ChromaDB")
            return doc_id
        
        except Exception as e:
            logger.error(f"Error storing unit in ChromaDB: {e}", exc_info=True)
            raise
    
    async def get(self, unit_id: str) -> Optional[NormalizedUnit]:
        """
        Получает нормализованную единицу из хранилища по идентификатору.
        
        Args:
            unit_id: Идентификатор единицы (unit.id)
            
        Returns:
            Нормализованная единица или None, если единица не найдена
        """
        try:
            # Запрашиваем документ по ID
            result = self.collection.get(ids=[unit_id], include=["documents"])
            
            # Проверяем, найден ли документ
            if not result or not result['documents'] or not result['documents'][0]:
                logger.debug(f"Unit with ID {unit_id} not found in ChromaDB")
                return None
            
            # Десериализуем JSON в объект NormalizedUnit
            try:
                unit_json = result['documents'][0]
                unit = NormalizedUnit.model_validate_json(unit_json)
                return unit
            except Exception as e:
                logger.error(f"Error deserializing unit from ChromaDB: {e}", exc_info=True)
                return None
        
        except Exception as e:
            logger.error(f"Error retrieving unit from ChromaDB: {e}", exc_info=True)
            return None
    
    async def load_all(self) -> List[NormalizedUnit]:
        """
        Загружает все нормализованные юниты из хранилища.
        
        Returns:
            Список всех нормализованных юнитов
        """
        try:
            # Запрашиваем все документы из коллекции с метаданными для фильтрации
            result = self.collection.get(include=["documents", "metadatas"])
            
            # Проверяем, есть ли результаты
            if not result or not result['documents']:
                logger.warning("No units found in ChromaDB")
                return []
            
            # Десериализуем каждый JSON в объект NormalizedUnit
            units = []
            metadatas = result.get('metadatas', [])
            
            for i, unit_json in enumerate(result['documents']):
                try:
                    if unit_json:  # Проверяем, что JSON не пустой
                        # Получаем метаданные для проверки типа документа
                        metadata = metadatas[i] if i < len(metadatas) else {}
                        doc_type = metadata.get('doc_type', 'unit')  # по умолчанию считаем unit
                        
                        # Обрабатываем только units, пропускаем segments и другие типы
                        if doc_type == 'unit' or doc_type is None:
                            unit = NormalizedUnit.model_validate_json(unit_json)
                            units.append(unit)
                        else:
                            logger.debug(f"Skipping document with doc_type '{doc_type}' in load_all")
                except Exception as e:
                    logger.error(f"Error deserializing unit from ChromaDB: {e}", exc_info=True)
            
            logger.info(f"Loaded {len(units)} units from ChromaDB")
            return units
        
        except Exception as e:
            logger.error(f"Error loading all units from ChromaDB: {e}", exc_info=True)
            return []
    
    async def delete(self, unit_id: str) -> bool:
        """
        Удаляет нормализованную единицу из хранилища по идентификатору.
        
        Args:
            unit_id: Идентификатор единицы (unit.id)
            
        Returns:
            True, если удаление успешно, иначе False
        """
        try:
            # Удаляем документ по ID
            self.collection.delete(ids=[unit_id])
            logger.info(f"Deleted unit with ID {unit_id} from ChromaDB")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting unit from ChromaDB: {e}", exc_info=True)
            return False
    
    async def delete_all(self) -> bool:
        """
        Удаляет все нормализованные единицы из хранилища.
        
        Returns:
            True, если удаление успешно, иначе False
        """
        try:
            # Удаляем всю коллекцию и создаем заново
            self.client.delete_collection(name=self.collection_name)
            self.collection = self.client.create_collection(
                name=self.collection_name,
                metadata={"description": "Нормализованные единицы знаний"}
            )
            logger.info(f"Deleted all units from ChromaDB collection '{self.collection_name}'")
            return True
        
        except Exception as e:
            logger.error(f"Error deleting all units from ChromaDB: {e}", exc_info=True)
            return False
    
    async def search(
        self, 
        query_text: Optional[str] = None,
        where_filters: Optional[Dict[str, Any]] = None,
        limit: int = 10
    ) -> List[Tuple[NormalizedUnit, float]]:
        """
        Выполняет поиск в хранилище по тексту и/или фильтрам метаданных.
        
        Args:
            query_text: Текст запроса для семантического поиска  
            where_filters: Фильтры по метаданным
            limit: Максимальное количество результатов
            
        Returns:
            Список кортежей (unit, score) с найденными единицами и их релевантностью
        """
        try:
            # Проверяем, есть ли критерий поиска (текст или фильтры)
            if not query_text and not where_filters:
                logger.warning("Search requires either query_text or where_filters")
                return []
            
            # Получаем вектор для поиска, если есть query_text
            query_vector = None
            if query_text:
                # Используем embed_provider для получения вектора
                # Нужно импортировать и получить провайдер
                from mindbank_poc.api.normalizers.config import load_config
                from mindbank_poc.core.normalizer.normalizer import Normalizer
                
                normalizer_config = load_config()
                normalizer = Normalizer(normalizer_config)
                embed_response = await normalizer.embed_provider.embed_text(query_text)
                
                # Получаем вектор из ответа (может быть как .embedding, так и .vector)
                if hasattr(embed_response, 'embedding'):
                    query_vector = embed_response.embedding
                elif hasattr(embed_response, 'vector'):
                    query_vector = embed_response.vector
                else:
                    # Если response сам является списком
                    query_vector = embed_response if isinstance(embed_response, list) else None
                
                if query_vector is None:
                    logger.error("Failed to extract query vector from embed response")
                    return []
                    
                logger.info(f"Generated query vector with {len(query_vector)} dimensions")
            
            # Подготавливаем фильтры метаданных в формате ChromaDB
            chroma_filter = None
            if where_filters:
                # Конвертируем фильтры в формат ChromaDB
                filter_conditions = []
                for key, value in where_filters.items():
                    # Обрабатываем специальные префиксы для совместимости
                    if key.startswith("metadata."):
                        # Убираем префикс metadata. для прямого доступа
                        filter_key = key[9:]  # удаляем "metadata."
                    elif key in ["type", "topic", "category"]:
                        # Классификационные поля имеют префикс class_
                        filter_key = f"class_{key}"
                    else:
                        filter_key = key
                    
                    # Добавляем условие фильтра
                    filter_conditions.append({filter_key: value})
                
                # Формируем правильный формат фильтра для ChromaDB
                if len(filter_conditions) == 1:
                    # Одно условие - используем простой формат
                    chroma_filter = filter_conditions[0]
                elif len(filter_conditions) > 1:
                    # Несколько условий - используем $and оператор
                    chroma_filter = {"$and": filter_conditions}
                else:
                    chroma_filter = None
            
            # Выполняем поиск
            if query_vector:
                # Семантический поиск по вектору
                result = self.collection.query(
                    query_embeddings=[query_vector],
                    where=chroma_filter,
                    n_results=limit,
                    include=["documents", "distances", "metadatas"] # Запрашиваем дистанции и метаданные
                )
            elif where_filters: # Если вектора нет, но есть фильтры
                # Только фильтрация по метаданным
                result = self.collection.get(
                    where=chroma_filter,
                    limit=limit,
                    include=["documents", "metadatas"] # Запрашиваем документы и метаданные
                )
            else: # На случай, если контроль выше пропустит
                return []
            
            # Проверяем, есть ли результаты
            # Для query результат в result["documents"][0], для get в result["documents"]
            documents = result.get('documents')
            if not documents or (isinstance(documents, list) and not documents[0]):
                logger.warning("No results found in ChromaDB query")
                return []
            
            # Обработка результатов
            results_list = []
            docs_to_process = documents[0] if query_vector else documents
            distances_list = result.get('distances')[0] if query_vector and result.get('distances') else None
            metadatas_list = result.get('metadatas')[0] if query_vector and result.get('metadatas') else result.get('metadatas', [])
            
            for i, unit_json in enumerate(docs_to_process):
                try:
                    if unit_json:
                        # Получаем метаданные для определения типа документа
                        metadata = metadatas_list[i] if i < len(metadatas_list) else {}
                        doc_type = metadata.get('doc_type', 'unit')
                        
                        if doc_type in ['segment', 'cluster']:
                            # Для мигрированных сегментов и кластеров создаем "псевдо-unit"
                            unit = self._create_migrated_unit_wrapper(unit_json, metadata, doc_type)
                        else:
                            # Обычная десериализация для настоящих units
                            unit = NormalizedUnit.model_validate_json(unit_json)
                        
                        score = 0.99 # Скор по умолчанию для get()
                        
                        if distances_list:
                            distance = float(distances_list[i])
                            # Преобразуем косинусную дистанцию [0, 2] в скор [0.99, ~0]
                            # similarity = 1.0 - (distance / 2.0) # Сходство [0, 1]
                            # score = 0.99 * (similarity ** 0.8) # Нелинейное масштабирование
                            score = max(0.01, 0.99 * (1.0 - (distance / 2.0))) # Линейное масштабирование
                            score = round(score, 2)
                            
                        results_list.append((unit, score))
                except Exception as e:
                    logger.error(f"Error deserializing search result from ChromaDB: {e}", exc_info=True)
            
            logger.info(f"Found {len(results_list)} results in ChromaDB")
            # Сортируем по скору, если был векторный поиск
            if query_vector:
                results_list.sort(key=lambda item: item[1], reverse=True)
                
            return results_list
        
        except Exception as e:
            logger.error(f"Error searching in ChromaDB: {str(e)}", exc_info=True)
            return []
    
    def _create_migrated_unit_wrapper(self, content: str, metadata: Dict[str, Any], doc_type: str) -> NormalizedUnit:
        """
        Создает обертку NormalizedUnit для мигрированных сегментов и кластеров.
        
        Args:
            content: Текстовое содержимое (например, "Сегмент: ...")
            metadata: Метаданные документа
            doc_type: Тип документа ('segment' или 'cluster')
            
        Returns:
            NormalizedUnit обертка для мигрированного документа
        """
        # Создаем уникальный ID на основе метаданных
        if doc_type == 'segment':
            unit_id = metadata.get('segment_id', f"migrated_segment_{id(content)}")
        elif doc_type == 'cluster':
            unit_id = metadata.get('cluster_id', f"migrated_cluster_{id(content)}")
        else:
            unit_id = f"migrated_{doc_type}_{id(content)}"
        
        # Создаем минимальную NormalizedUnit обертку
        from datetime import datetime
        
        unit_data = {
            "id": unit_id,
            "aggregate_id": f"migrated_{doc_type}_{unit_id}",
            "group_id": metadata.get('group_id', 'migrated'),
            "text_repr": content,  # Используем полный текст как text_repr
            "created_at": metadata.get('created_at', datetime.utcnow().isoformat()),
            "entity_metadata": {},
            "classifications": [],
            "archetype": doc_type,  # Маркируем как segment или cluster
            "source": metadata.get('source', 'migrated'),
            "importance_score": 0.5,
            "custom_metadata": {
                "migrated_type": doc_type,
                "original_content": content[:100] + "..." if len(content) > 100 else content
            }
        }
        
        return NormalizedUnit(**unit_data)

    async def list_group_ids(self) -> Set[str]:
        """
        Возвращает множество всех group_id в хранилище.
        
        Returns:
            Set[str]: Множество уникальных group_id
        """
        group_ids = set()
        
        try:
            # Получаем все записи из коллекции
            result = self.collection.get(
                include=["metadatas"]
            )
            
            # Извлекаем group_id из метаданных
            if result and "metadatas" in result:
                for metadata in result["metadatas"]:
                    if metadata and "group_id" in metadata:
                        group_ids.add(metadata["group_id"])
            
            logger.debug(f"Found {len(group_ids)} unique group IDs in ChromaDB")
            return group_ids
            
        except Exception as e:
            logger.error(f"Failed to list group IDs from ChromaDB: {e}", exc_info=True)
            return set()
    
    async def list_by_group(self, group_id: str) -> List[NormalizedUnit]:
        """
        Возвращает список нормализованных единиц для указанной группы.
        
        Args:
            group_id: Идентификатор группы
            
        Returns:
            Список нормализованных единиц группы
        """
        try:
            # Запрашиваем все документы группы
            results = self.collection.get(
                where={"group_id": group_id},
                include=["documents", "metadatas"]
            )
            
            units = []
            if results and results['documents']:
                metadatas = results.get('metadatas', [])
                for i, doc_json in enumerate(results['documents']):
                    if doc_json:
                        # Получаем метаданные для документа
                        metadata = metadatas[i] if i < len(metadatas) else {}
                        doc_type = metadata.get('doc_type', 'unit')  # по умолчанию считаем unit
                        
                        # Обрабатываем только units, пропускаем segments и другие типы
                        if doc_type == 'unit' or doc_type is None:
                            try:
                                unit = NormalizedUnit.model_validate_json(doc_json)
                                units.append(unit)
                            except Exception as e:
                                logger.error(f"Error deserializing unit from group {group_id}: {e}")
                                # Не прерываем выполнение, просто пропускаем проблемный документ
                                continue
                        else:
                            logger.debug(f"Skipping document with doc_type '{doc_type}' in group {group_id}")
            
            logger.info(f"Found {len(units)} units for group {group_id} in ChromaDB")
            return units
            
        except Exception as e:
            logger.error(f"Error listing units by group from ChromaDB: {e}", exc_info=True)
            return []
    
    async def list_unprocessed_groups(self, min_units: int = 10) -> List[str]:
        """
        Возвращает список групп с необработанными юнитами (без сегментов).
        
        Args:
            min_units: Минимальное количество юнитов в группе для обработки
            
        Returns:
            Список идентификаторов групп
        """
        try:
            # Получаем все group_id и подсчитываем юниты
            group_ids = await self.list_group_ids()
            qualified_groups = []
            
            for group_id in group_ids:
                # Получаем количество юнитов в группе
                units = await self.list_by_group(group_id)
                if len(units) >= min_units:
                    # Проверяем, есть ли сегменты для этой группы
                    segments = await self.list_segments_by_group(group_id)
                    if not segments:
                        qualified_groups.append(group_id)
            
            logger.info(f"Found {len(qualified_groups)} groups with >= {min_units} units and no segments")
            return qualified_groups
            
        except Exception as e:
            logger.error(f"Failed to list unprocessed groups: {e}", exc_info=True)
            return []
    
    async def store_aggregate(self, aggregate_id: str, aggregate_data: Dict[str, Any]) -> str:
        """
        Сохраняет агрегат в ChromaDB.
        
        Args:
            aggregate_id: ID агрегата
            aggregate_data: Данные агрегата (словарь)
            
        Returns:
            ID сохраненного агрегата
        """
        try:
            # Идентификатор для ChromaDB
            doc_id = f"aggregate_{aggregate_id}"
            
            # Сохраняем как JSON документ
            import json
            document = json.dumps(aggregate_data, ensure_ascii=False)
            
            # Метаданные для фильтрации
            metadata = {
                "doc_type": "aggregate",
                "aggregate_id": aggregate_id,
                "group_id": aggregate_data.get("group_id", "unknown"),
                "created_at": aggregate_data.get("aggregated_at", ""),
            }
            
            # Добавляем в коллекцию без эмбеддинга (агрегаты не нуждаются в семантическом поиске)
            self.collection.add(
                ids=[doc_id],
                documents=[document],
                metadatas=[metadata]
            )
            
            logger.debug(f"Stored aggregate {aggregate_id} in ChromaDB")
            return aggregate_id
            
        except Exception as e:
            logger.error(f"Error storing aggregate in ChromaDB: {e}", exc_info=True)
            raise

    async def get_aggregate(self, aggregate_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает агрегат из ChromaDB.
        
        Args:
            aggregate_id: ID агрегата
            
        Returns:
            Агрегат или None, если не найден
        """
        try:
            doc_id = f"aggregate_{aggregate_id}"
            result = self.collection.get(ids=[doc_id], include=["documents"])
            
            if not result or not result['documents'] or not result['documents'][0]:
                logger.debug(f"Aggregate with ID {aggregate_id} not found in ChromaDB")
                return None
            
            # Десериализуем JSON
            try:
                import json
                aggregate_json = result['documents'][0]
                aggregate_data = json.loads(aggregate_json)
                return aggregate_data
            except Exception as e:
                logger.error(f"Error deserializing aggregate from ChromaDB: {e}", exc_info=True)
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving aggregate from ChromaDB: {e}", exc_info=True)
            return None

    async def get_original_aggregate(self, unit_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает оригинальный агрегат для нормализованной единицы.
        
        Args:
            unit_id: ID нормализованной единицы (unit.id)
            
        Returns:
            Агрегат или None, если не найден
        """
        try:
            # Сначала получаем нормализованную единицу
            unit = await self.get(unit_id)
            if not unit:
                logger.debug(f"Unit {unit_id} not found (normal for migrated segments/clusters)")
                return None
            
            # Пытаемся получить агрегат из ChromaDB
            aggregate_data = await self.get_aggregate(unit.aggregate_id)
            if aggregate_data:
                return aggregate_data
            
            # Фолбэк к JSONL backend если агрегат не найден в ChromaDB
            logger.debug(f"Aggregate {unit.aggregate_id} not found in ChromaDB, trying JSONL backend")
            from mindbank_poc.api.backends import jsonl_backend
            aggregate = await jsonl_backend.load_aggregate_by_id(unit.aggregate_id)
            
            if aggregate:
                # Преобразуем модель AggregateInput в словарь
                return aggregate.model_dump(mode="json")
            else:
                logger.warning(f"Original aggregate {unit.aggregate_id} not found for unit {unit_id}")
                return None
        except Exception as e:
            logger.error(f"Error loading original aggregate for unit {unit_id}: {e}")
            return None
    
    # Методы для работы с сегментами
    async def store_segment(self, segment: SegmentModel) -> str:
        """
        Сохраняет сегмент в хранилище.
        
        Args:
            segment: Сегмент для сохранения
            
        Returns:
            Идентификатор сохраненного сегмента
        """
        try:
            # Идентификатор для ChromaDB
            doc_id = f"segment_{segment.id}"
            
            # Текстовое представление для поиска (заголовок + резюме)
            document = f"{segment.title}\n\n{segment.summary}"
            
            # Векторное представление (если есть)
            embedding = segment.vector_repr
            
            # Метаданные для хранения и фильтрации
            metadata = {
                "doc_type": "segment",  # Тип документа
                "segment_id": segment.id,
                "group_id": segment.group_id,
                "created_at": segment.created_at.isoformat(),
                "entity_count": len(segment.entities),
                "unit_count": len(segment.raw_unit_ids),
                # Сохраняем первые 10 сущностей для фильтрации
                **{f"entity_{i}": entity for i, entity in enumerate(segment.entities[:10])}
            }
            
            # Сохраняем полный объект как JSON
            full_segment_json = segment.model_dump_json()
            
            # Используем upsert для обновления существующих документов
            if embedding:
                self.collection.upsert(
                    ids=[doc_id],
                    embeddings=[embedding],
                    documents=[full_segment_json],
                    metadatas=[metadata]
                )
            else:
                self.collection.upsert(
                    ids=[doc_id],
                    documents=[full_segment_json],
                    metadatas=[metadata]
                )
            
            logger.info(f"Stored segment {segment.id} in ChromaDB")
            return segment.id
            
        except Exception as e:
            logger.error(f"Error storing segment in ChromaDB: {e}", exc_info=True)
            raise
    
    async def get_segment(self, segment_id: str) -> Optional[SegmentModel]:
        """
        Получает сегмент из хранилища.
        
        Args:
            segment_id: Идентификатор сегмента
            
        Returns:
            Сегмент или None, если не найден
        """
        try:
            doc_id = f"segment_{segment_id}"
            result = self.collection.get(ids=[doc_id], include=["documents"])
            
            if not result or not result['documents'] or not result['documents'][0]:
                logger.warning(f"Segment with ID {segment_id} not found in ChromaDB")
                return None
            
            # Десериализуем JSON в объект SegmentModel
            try:
                segment_json = result['documents'][0]
                segment = SegmentModel.model_validate_json(segment_json)
                return segment
            except Exception as e:
                logger.error(f"Error deserializing segment from ChromaDB: {e}", exc_info=True)
                return None
                
        except Exception as e:
            logger.error(f"Error retrieving segment from ChromaDB: {e}", exc_info=True)
            return None
    
    async def list_segments_by_group(self, group_id: str) -> List[SegmentModel]:
        """
        Получает все сегменты для указанной группы.
        
        Args:
            group_id: Идентификатор группы
            
        Returns:
            Список сегментов группы
        """
        try:
            # Запрашиваем все сегменты группы
            results = self.collection.get(
                where={
                    "$and": [
                        {"doc_type": "segment"},
                        {"group_id": group_id}
                    ]
                },
                include=["documents"]
            )
            
            segments = []
            if results and results['documents']:
                for doc_json in results['documents']:
                    if doc_json:
                        try:
                            segment = SegmentModel.model_validate_json(doc_json)
                            segments.append(segment)
                        except Exception as e:
                            logger.error(f"Error deserializing segment: {e}")
            
            logger.info(f"Found {len(segments)} segments for group {group_id} in ChromaDB")
            return segments
            
        except Exception as e:
            logger.error(f"Error listing segments by group from ChromaDB: {e}", exc_info=True)
            return []
    
    async def get_segments_for_unit(self, unit_id: str) -> List[SegmentModel]:
        """
        Получает все сегменты, в которые входит указанный юнит.
        
        Args:
            unit_id: Идентификатор юнита (unit.id)
            
        Returns:
            Список сегментов, содержащих данный юнит
        """
        try:
            # В ChromaDB нет прямого способа искать по массиву raw_unit_ids,
            # поэтому загружаем все сегменты и фильтруем
            results = self.collection.get(
                where={"doc_type": "segment"},
                include=["documents"]
            )
            
            segments = []
            if results and results['documents']:
                for doc_json in results['documents']:
                    if doc_json:
                        try:
                            segment = SegmentModel.model_validate_json(doc_json)
                            # Проверяем, содержит ли сегмент данный юнит
                            if unit_id in segment.raw_unit_ids:
                                segments.append(segment)
                        except Exception as e:
                            logger.error(f"Error deserializing segment: {e}")
            
            logger.debug(f"Found {len(segments)} segments containing unit {unit_id}")
            return segments
            
        except Exception as e:
            logger.error(f"Error getting segments for unit from ChromaDB: {e}", exc_info=True)
            return []

    # Методы для работы с кластерами
    async def store_cluster(self, cluster: ClusterModel) -> str:
        """
        Сохраняет кластер в хранилище.
        
        Args:
            cluster: Кластер для сохранения
            
        Returns:
            Идентификатор сохраненного кластера
        """
        try:
            # Идентификатор для ChromaDB
            doc_id = f"cluster_{cluster.id}"
            
            # Текстовое представление для поиска (заголовок + резюме + ключевые слова)
            keywords_text = ", ".join(cluster.keywords) if cluster.keywords else ""
            document = f"{cluster.title}\n\n{cluster.summary}\n\nКлючевые слова: {keywords_text}"
            
            # Векторное представление (центроид кластера)
            embedding = cluster.centroid if cluster.centroid else None
            
            # Метаданные для хранения и фильтрации
            metadata = {
                "doc_type": "cluster",  # Тип документа
                "cluster_id": cluster.id,
                "cluster_size": cluster.cluster_size,
                "created_at": cluster.created_at.isoformat(),
                "keyword_count": len(cluster.keywords),
                # Сохраняем первые 10 ключевых слов для фильтрации
                **{f"keyword_{i}": keyword for i, keyword in enumerate(cluster.keywords[:10])}
            }
            
            # Сохраняем полный объект как JSON
            full_cluster_json = cluster.model_dump_json()
            
            # Используем upsert для обновления существующих документов
            if embedding:
                self.collection.upsert(
                    ids=[doc_id],
                    embeddings=[embedding],
                    documents=[full_cluster_json],
                    metadatas=[metadata]
                )
            else:
                # Сохраняем без эмбеддинга если центроида нет
                self.collection.upsert(
                    ids=[doc_id],
                    documents=[full_cluster_json],
                    metadatas=[metadata]
                )
            
            logger.info(f"Stored cluster {cluster.id} with {cluster.cluster_size} segments in ChromaDB")
            return cluster.id
            
        except Exception as e:
            logger.error(f"Error storing cluster in ChromaDB: {e}", exc_info=True)
            raise
    
    async def get_cluster(self, cluster_id: str) -> Optional[ClusterModel]:
        """
        Получает кластер из хранилища.
        
        Args:
            cluster_id: Идентификатор кластера
            
        Returns:
            Кластер или None, если не найден
        """
        try:
            doc_id = f"cluster_{cluster_id}"
            result = self.collection.get(ids=[doc_id], include=["documents", "metadatas"])
            
            if not result or not result['documents'] or not result['documents'][0]:
                logger.warning(f"Cluster with ID {cluster_id} not found in ChromaDB")
                return None
            
            # Десериализуем JSON в объект ClusterModel
            try:
                cluster_json = result['documents'][0]
                cluster = ClusterModel.model_validate_json(cluster_json)
                return cluster
            except Exception as json_error:
                # Если JSON не получился, это мигрированный кластер как строка
                # Создаем фиктивный ClusterModel из метаданных
                try:
                    metadata = result['metadatas'][0] if result['metadatas'] else {}
                    
                    cluster = ClusterModel(
                        id=cluster_id,
                        title=metadata.get('title', 'Migrated Cluster'),
                        summary=metadata.get('summary', ''),
                        keywords=metadata.get('keywords', '').split(',') if metadata.get('keywords') else [],
                        segment_ids=[],  # Не можем восстановить из строки
                        cluster_size=int(metadata.get('cluster_size', 0)),
                        centroid=[],  # Не можем восстановить из строки
                        created_at=metadata.get('created_at', ''),
                        updated_at=metadata.get('created_at', '')
                    )
                    logger.debug(f"Recovered migrated cluster {cluster_id} from metadata")
                    return cluster
                except Exception as e:
                    logger.error(f"Could not recover migrated cluster {cluster_id}: {e}")
                    return None
                
        except Exception as e:
            logger.error(f"Error retrieving cluster from ChromaDB: {e}", exc_info=True)
            return None
    
    async def list_clusters(self) -> List[ClusterModel]:
        """
        Получает все кластеры из хранилища.
        
        Returns:
            Список всех кластеров
        """
        try:
            # Запрашиваем все кластеры
            results = self.collection.get(
                where={"doc_type": "cluster"},
                include=["documents", "metadatas"]
            )
            
            clusters = []
            if results and results['documents']:
                for i, doc_content in enumerate(results['documents']):
                    if doc_content:
                        try:
                            # Попробуем сначала десериализовать как JSON
                            cluster = ClusterModel.model_validate_json(doc_content)
                            clusters.append(cluster)
                        except Exception as json_error:
                            # Если JSON не получился, это мигрированный кластер как строка
                            # Создаем фиктивный ClusterModel из метаданных
                            try:
                                metadata = results['metadatas'][i] if results['metadatas'] and i < len(results['metadatas']) else {}
                                
                                # Создаем минимальный ClusterModel для мигрированных данных
                                cluster_id = metadata.get('cluster_id', f'unknown_{i}')
                                cluster = ClusterModel(
                                    id=cluster_id,
                                    title=metadata.get('title', 'Migrated Cluster'),
                                    summary=metadata.get('summary', ''),
                                    keywords=metadata.get('keywords', '').split(',') if metadata.get('keywords') else [],
                                    segment_ids=[],  # Не можем восстановить из строки
                                    cluster_size=int(metadata.get('cluster_size', 0)),
                                    centroid=[],  # Не можем восстановить из строки
                                    created_at=metadata.get('created_at', ''),
                                    updated_at=metadata.get('created_at', '')
                                )
                                clusters.append(cluster)
                                logger.debug(f"Recovered migrated cluster {cluster_id} from metadata")
                            except Exception as e:
                                logger.warning(f"Could not recover migrated cluster {i}: {e}")
            
            logger.info(f"Found {len(clusters)} clusters in ChromaDB")
            return clusters
            
        except Exception as e:
            logger.error(f"Error listing clusters from ChromaDB: {e}", exc_info=True)
            return []
    
    async def get_clusters_for_segment(self, segment_id: str) -> List[ClusterModel]:
        """
        Получает все кластеры, в которые входит указанный сегмент.
        
        Args:
            segment_id: Идентификатор сегмента
            
        Returns:
            Список кластеров, содержащих данный сегмент
        """
        try:
            # В ChromaDB нет прямого способа искать по массиву segment_ids,
            # поэтому загружаем все кластеры и фильтруем
            results = self.collection.get(
                where={"doc_type": "cluster"},
                include=["documents"]
            )
            
            clusters = []
            if results and results['documents']:
                for doc_json in results['documents']:
                    if doc_json:
                        try:
                            cluster = ClusterModel.model_validate_json(doc_json)
                            # Проверяем, содержит ли кластер данный сегмент
                            if segment_id in cluster.segment_ids:
                                clusters.append(cluster)
                        except Exception as e:
                            logger.error(f"Error deserializing cluster: {e}")
            
            logger.debug(f"Found {len(clusters)} clusters containing segment {segment_id}")
            return clusters
            
        except Exception as e:
            logger.error(f"Error getting clusters for segment from ChromaDB: {e}", exc_info=True)
            return []

    # New method: segments for cluster
    async def list_segments_by_cluster(self, cluster_id: str) -> List[SegmentModel]:
        """Возвращает все сегменты, относящиеся к кластеру."""
        try:
            cluster = await self.get_cluster(cluster_id)
            if not cluster or not cluster.segment_ids:
                return []

            segment_ids_set = set(cluster.segment_ids)

            # Быстрый путь: если segment_ids не слишком много, запрашиваем по id
            segments: List[SegmentModel] = []
            for sid in segment_ids_set:
                seg = await self.get_segment(sid)
                if seg:
                    segments.append(seg)
            return segments
        except Exception as e:
            logger.error(f"Error listing segments by cluster from ChromaDB: {e}", exc_info=True)
            return []

    def _group_meta_file(self):
        return self.data_dir / "group_segmentation_meta.json"

    async def get_group_segmentation_meta(self, group_id: str) -> dict:
        """Возвращает метаинформацию по сегментации для группы (или пустой dict)."""
        meta_file = self._group_meta_file()
        if not meta_file.exists():
            return {}
        async with aiofiles.open(meta_file, 'r', encoding='utf-8') as f:
            content = await f.read()
            if not content.strip():
                return {}
            try:
                meta = json.loads(content)
                return meta.get(group_id, {})
            except Exception:
                return {}

    async def set_group_segmentation_meta(self, group_id: str, last_segmented_at: str, last_segmented_unit_id: str):
        """Обновляет метаинформацию по сегментации для группы."""
        meta_file = self._group_meta_file()
        meta = {}
        if meta_file.exists():
            async with aiofiles.open(meta_file, 'r', encoding='utf-8') as f:
                content = await f.read()
                if content.strip():
                    try:
                        meta = json.loads(content)
                    except Exception:
                        meta = {}
        meta[group_id] = {
            "last_segmented_at": last_segmented_at,
            "last_segmented_unit_id": last_segmented_unit_id
        }
        async with aiofiles.open(meta_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(meta, ensure_ascii=False, indent=2))

    async def get_groups_with_new_units_for_segmentation(self, min_units: int = 10) -> list:
        """Возвращает группы, где есть новые юниты после последней сегментации."""
        group_ids = await self.list_group_ids()
        result = []
        for group_id in group_ids:
            units = await self.list_by_group(group_id)
            if not units:
                continue
            units_sorted = sorted(units, key=lambda u: (u.normalized_at or getattr(u, 'stored_at', "")))
            last_unit = units_sorted[-1]
            meta = await self.get_group_segmentation_meta(group_id)
            last_segmented_unit_id = meta.get("last_segmented_unit_id")
            # Если сегментации не было или есть новые юниты
            if not last_segmented_unit_id or any(u.id > last_segmented_unit_id for u in units_sorted):
                if len(units) >= min_units:
                    result.append(group_id)
        return result 

    async def filter_segments(
        self,
        group_id: Optional[str] = None,
        source: Optional[str] = None,
        source_name: Optional[str] = None,
        title_contains: Optional[str] = None,
        summary_contains: Optional[str] = None,
        entity_contains: Optional[str] = None,
        min_unit_count: Optional[int] = None,
        max_unit_count: Optional[int] = None,
        date_from: Optional[str] = None,
        date_to: Optional[str] = None,
        limit: int = 50,
        sort_by: str = "created_at",
        sort_order: str = "desc"
    ) -> List[SegmentModel]:
        """
        Фильтрует сегменты по заданным критериям.
        
        Args:
            group_id: Фильтр по группе
            source: Фильтр по источнику данных (source_metadata.source)
            source_name: Фильтр по названию источника (source_metadata.source_name)
            title_contains: Поиск в заголовках (частичное совпадение)
            summary_contains: Поиск в резюме (частичное совпадение)
            entity_contains: Фильтр по наличию сущности
            min_unit_count: Минимальное количество юнитов
            max_unit_count: Максимальное количество юнитов
            date_from: Дата создания от (ISO строка)
            date_to: Дата создания до (ISO строка)
            limit: Максимальное количество результатов
            sort_by: Поле для сортировки
            sort_order: Порядок сортировки (asc/desc)
            
        Returns:
            Список отфильтрованных сегментов
        """
        try:
            # Используем простую загрузку всех сегментов
            # и фильтруем на уровне приложения
            if group_id:
                # Если указана группа - используем оптимизированный метод
                segments = await self.list_segments_by_group(group_id)
            else:
                # Загружаем все сегменты
                try:
                    # Получаем все документы с типом segment
                    results = self.collection.get(include=["documents", "metadatas"])
                    
                    segments = []
                    if results and results['documents']:
                        metadatas = results.get('metadatas', [])
                        
                        for i, doc_json in enumerate(results['documents']):
                            if doc_json:
                                # Проверяем тип документа через метаданные
                                metadata = metadatas[i] if i < len(metadatas) else {}
                                doc_type = metadata.get('doc_type', 'unit')
                                
                                if doc_type == 'segment':
                                    try:
                                        segment = SegmentModel.model_validate_json(doc_json)
                                        segments.append(segment)
                                    except Exception as e:
                                        logger.error(f"Error deserializing segment: {e}")
                                        continue
                except Exception as e:
                    logger.error(f"Error loading segments from ChromaDB: {e}")
                    return []
            
            # Применяем фильтры на уровне приложения
            filtered_segments = []
            for segment in segments:
                # Фильтр по источнику
                if source:
                    segment_source = segment.metadata.get('source_metadata', {}).get('source', '')
                    if source.lower() not in segment_source.lower():
                        continue
                
                # Фильтр по названию источника
                if source_name:
                    segment_source_name = segment.metadata.get('source_metadata', {}).get('source_name', '')
                    if source_name.lower() not in segment_source_name.lower():
                        continue
                
                # Фильтр по заголовку
                if title_contains and title_contains.lower() not in segment.title.lower():
                    continue
                
                # Фильтр по резюме
                if summary_contains and summary_contains.lower() not in segment.summary.lower():
                    continue
                
                # Фильтр по сущности
                if entity_contains:
                    if not any(entity_contains.lower() in entity.lower() for entity in segment.entities):
                        continue
                
                # Фильтр по количеству юнитов
                unit_count = len(segment.raw_unit_ids)
                if min_unit_count is not None and unit_count < min_unit_count:
                    continue
                if max_unit_count is not None and unit_count > max_unit_count:
                    continue
                
                # Фильтр по дате
                if date_from:
                    try:
                        from datetime import datetime
                        date_from_dt = datetime.fromisoformat(date_from.replace('Z', '+00:00'))
                        if segment.created_at < date_from_dt:
                            continue
                    except ValueError:
                        logger.warning(f"Invalid date_from format: {date_from}")
                
                if date_to:
                    try:
                        from datetime import datetime
                        date_to_dt = datetime.fromisoformat(date_to.replace('Z', '+00:00'))
                        if segment.created_at > date_to_dt:
                            continue
                    except ValueError:
                        logger.warning(f"Invalid date_to format: {date_to}")
                
                filtered_segments.append(segment)
            
            # Сортировка
            if sort_by == "created_at":
                filtered_segments.sort(key=lambda s: s.created_at, reverse=(sort_order == "desc"))
            elif sort_by == "title":
                filtered_segments.sort(key=lambda s: s.title.lower(), reverse=(sort_order == "desc"))
            elif sort_by == "unit_count":
                filtered_segments.sort(key=lambda s: len(s.raw_unit_ids), reverse=(sort_order == "desc"))
            else:
                # Сортировка по умолчанию
                filtered_segments.sort(key=lambda s: s.created_at, reverse=(sort_order == "desc"))
            
            # Ограничиваем количество результатов
            result = filtered_segments[:limit]
            
            logger.info(f"Filtered segments: found {len(result)} of {len(segments)} total")
            return result
            
        except Exception as e:
            logger.error(f"Error filtering segments: {e}", exc_info=True)
            return [] 