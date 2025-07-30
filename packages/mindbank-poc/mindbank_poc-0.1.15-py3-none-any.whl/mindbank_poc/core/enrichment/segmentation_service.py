"""
Сервис для сегментации нормализованных юнитов.
"""
from typing import List, Optional, Dict, Any, Tuple
from uuid import uuid4
from datetime import datetime

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings
from mindbank_poc.core.knowledge_store.base import KnowledgeStore
from mindbank_poc.core.normalizer.models import NormalizedUnit
from mindbank_poc.core.enrichment.models import SegmentModel
from mindbank_poc.core.enrichment.segment_utils import (
    merge_overlaps, 
    merge_contiguous, 
    validate_segments,
    crop_text
)
from mindbank_poc.core.providers.segmentation import SegmentationProvider
from mindbank_poc.core.services.provider_service import get_provider_service
from mindbank_poc.core.providers.selector import ProviderSelector
from mindbank_poc.core.common.types import ProviderType

logger = get_logger(__name__)


class SegmentationService:
    """Сервис для выполнения сегментации групп нормализованных юнитов."""
    
    def __init__(
        self,
        knowledge_store: KnowledgeStore
    ):
        """
        Инициализация сервиса сегментации.
        
        Args:
            knowledge_store: Хранилище знаний для работы с юнитами и сегментами
        """
        self.knowledge_store = knowledge_store
        self.provider_service = get_provider_service()
        
        # Параметры обработки окон из настроек
        self.window_size = getattr(settings.enrichment, 'window_size', 40)
        self.window_overlap = getattr(settings.enrichment, 'window_overlap', 10)
        self.crop_length = getattr(settings.enrichment, 'crop_length', 40)
        
        # Параметры эмбеддингов сегментов
        self.segment_embed_provider_id = getattr(settings.enrichment, 'segment_embed_provider', 'openai')
    
    def build_windows(
        self, 
        units: List[NormalizedUnit], 
        window_size: Optional[int] = None,
        overlap: Optional[int] = None
    ) -> List[Tuple[str, List[int]]]:
        """
        Разбивает юниты на окна для обработки.
        
        Args:
            units: Список нормализованных юнитов
            window_size: Размер окна (по умолчанию из настроек)
            overlap: Перекрытие окон (по умолчанию из настроек)
            
        Returns:
            Список кортежей (текст_окна, индексы_юнитов)
        """
        if window_size is None:
            window_size = self.window_size
        if overlap is None:
            overlap = self.window_overlap
        
        step = window_size - overlap if window_size > overlap else window_size
        windows = []
        
        for start_idx in range(0, len(units), step):
            end_idx = min(start_idx + window_size, len(units))
            window_units = units[start_idx:end_idx]
            
            # Определяем формат на основе типа контента
            is_conversational = self._is_conversational_content(window_units)
            
            # Формируем текст окна
            window_lines = []
            for i, unit in enumerate(window_units):
                global_idx = start_idx + i + 1  # 1-based индекс
                
                if is_conversational:
                    # Формат для чатов/разговоров: <№>. <author>: <content>
                    author = self._extract_author(unit)
                    content = crop_text(unit.text_repr or "", self.crop_length)
                    line = f"{global_idx}. {author}: {content}"
                else:
                    # Формат для документов/статей: <№>. <content>
                    content = crop_text(unit.text_repr or "", self.crop_length)
                    line = f"{global_idx}. {content}"
                
                window_lines.append(line)
            
            window_text = "\n".join(window_lines)
            window_indices = list(range(start_idx, end_idx))
            
            windows.append((window_text, window_indices))
        
        logger.debug(f"Built {len(windows)} windows from {len(units)} units (conversational: {is_conversational})")
        return windows
    
    def _is_conversational_content(self, units: List[NormalizedUnit]) -> bool:
        """
        Определяет, является ли контент разговорным (чат, митинг, интервью).
        
        Args:
            units: Список юнитов для анализа
            
        Returns:
            True если контент разговорный, False для документов/статей
        """
        if not units:
            return False
        
        # Проверяем типы источников
        conversational_sources = {
            "telegram", "discord", "slack", "whatsapp", "teams", 
            "zoom", "meet", "interview", "conversation", "chat"
        }
        
        # Проверяем архетипы
        conversational_archetypes = {
            "chat", "meeting", "interview", "conversation", "call"
        }
        
        for unit in units[:5]:  # Проверяем первые 5 юнитов
            # Проверяем архетип
            if unit.archetype and unit.archetype.lower() in conversational_archetypes:
                return True
            
            # Проверяем метаданные
            if unit.metadata:
                source_type = unit.metadata.get("source_type", "").lower()
                source = unit.metadata.get("source", "").lower()
                
                if any(conv_source in source_type for conv_source in conversational_sources):
                    return True
                if any(conv_source in source for conv_source in conversational_sources):
                    return True
                
                # Проверяем наличие автора/участника
                if "author" in unit.metadata or "user" in unit.metadata or "speaker" in unit.metadata:
                    return True
        
        return False
    
    def _extract_author(self, unit: NormalizedUnit) -> str:
        """
        Извлекает автора/участника из юнита.
        
        Args:
            unit: Нормализованный юнит
            
        Returns:
            Имя автора или пустая строка
        """
        if not unit.metadata:
            return ""
        
        # Проверяем различные поля для автора
        author_fields = ["author", "user", "speaker", "participant", "name", "from"]
        
        for field in author_fields:
            if field in unit.metadata:
                author = unit.metadata[field]
                if author and str(author).strip():
                    return str(author).strip()
        
        return ""
    
    async def segment_group(self, group_id: str) -> List[SegmentModel]:
        """
        Выполняет сегментацию для указанной группы.
        """
        try:
            # Получаем все юниты группы
            units = await self._get_units_by_group(group_id)
            if not units:
                logger.warning(f"No units found for group {group_id}")
                return []
            
            # Получаем last_segmented_unit_id из метаинформации
            last_segmented_unit_id = None
            if hasattr(self.knowledge_store, 'get_group_segmentation_meta'):
                meta = await self.knowledge_store.get_group_segmentation_meta(group_id)
                last_segmented_unit_id = meta.get("last_segmented_unit_id")

            # Сортируем юниты по дате/ID
            units_sorted = sorted(units, key=lambda u: u.normalized_at or getattr(u, 'stored_at', ""))

            # Фильтруем только новые юниты (после last_segmented_unit_id)
            if last_segmented_unit_id:
                new_units = []
                found = False
                for u in units_sorted:
                    if found:
                        new_units.append(u)
                    elif u.id == last_segmented_unit_id:
                        found = True
                # Если last_segmented_unit_id не найден — сегментируем все
                if not found:
                    new_units = units_sorted
            else:
                new_units = units_sorted

            if not new_units:
                logger.info(f"No new units to segment for group {group_id}")
                return []
            
            logger.info(f"Segmenting {len(new_units)} new units for group {group_id}")
            
            # Выбираем провайдера сегментации
            first_unit = new_units[0]
            provider = await self._select_segmentation_provider(
                archetype=first_unit.archetype,
                metadata=first_unit.metadata
            )
            
            if not provider:
                logger.error("No segmentation provider available")
                return []
            
            # Подготавливаем метаданные группы
            group_metadata = self._extract_group_metadata(units)
            
            # Разбиваем на окна только новые юниты
            windows = self.build_windows(new_units)
            
            # Обрабатываем каждое окно
            all_segments = []
            for i, (window_text, window_indices) in enumerate(windows):
                logger.debug(f"Processing window {i+1}/{len(windows)} with {len(window_indices)} units")
                try:
                    result = await provider.extract_segments(window_text, group_metadata)
                    for segment in result.segments:
                        if "start" in segment and "end" in segment:
                            pass
                        else:
                            if "unit_indices" in segment:
                                segment["unit_indices"] = [window_indices[idx] for idx in segment["unit_indices"] if idx < len(window_indices)]
                        all_segments.append(segment)
                except Exception as e:
                    logger.error(f"Failed to process window {i+1}: {e}")
                    continue
            
            logger.info(f"Collected {len(all_segments)} segments from {len(windows)} windows")
            
            clean_segments = merge_overlaps(all_segments)
            final_segments = merge_contiguous(clean_segments)
            
            logger.info(f"After post-processing: {len(final_segments)} segments")
            
            segments = []
            for seg_data in final_segments:
                if "start" in seg_data and "end" in seg_data:
                    start_idx = seg_data["start"] - 1
                    end_idx = seg_data["end"]
                    raw_unit_ids = [new_units[i].id for i in range(start_idx, end_idx) if i < len(new_units)]
                else:
                    unit_indices = seg_data.get("unit_indices", [])
                    raw_unit_ids = [new_units[i].id for i in unit_indices if i < len(new_units)]
                
                # Создаем timeline на основе временных меток юнитов
                timeline = self._create_segment_timeline(
                    raw_unit_ids, 
                    new_units if "start" in seg_data else [new_units[i] for i in seg_data.get("unit_indices", [])]
                )
                
                segment = SegmentModel(
                    group_id=group_id,
                    title=seg_data.get("title", "Untitled Segment"),
                    summary=seg_data.get("summary", ""),
                    raw_unit_ids=raw_unit_ids,
                    entities=seg_data.get("entities", []),
                    timeline=timeline,  # Используем сгенерированный timeline
                    metadata={
                        "source_metadata": first_unit.metadata,
                        "segmentation_provider": provider.__class__.__name__,
                        "start_index": seg_data.get("start"),
                        "end_index": seg_data.get("end")
                    }
                )
                await self._generate_segment_embedding(segment)
                await self.knowledge_store.store_segment(segment)
                segments.append(segment)
            
            logger.info(f"Created {len(segments)} segments for group {group_id}")
            return segments
        except Exception as e:
            logger.error(f"Failed to segment group {group_id}: {e}", exc_info=True)
            return []
    
    def _extract_group_metadata(self, units: List[NormalizedUnit]) -> Dict[str, Any]:
        """
        Извлекает метаданные группы из списка юнитов.
        
        Args:
            units: Список нормализованных юнитов
            
        Returns:
            Метаданные группы
        """
        if not units:
            return {}
        
        # Собираем уникальные источники
        sources = set()
        participants = set()
        
        for unit in units:
            if unit.metadata:
                if "source" in unit.metadata:
                    sources.add(unit.metadata["source"])
                if "source_type" in unit.metadata:
                    sources.add(unit.metadata["source_type"])
                if "author" in unit.metadata:
                    participants.add(unit.metadata["author"])
                if "user" in unit.metadata:
                    participants.add(unit.metadata["user"])
        
        # Определяем временной диапазон
        dates = [u.normalized_at for u in units if u.normalized_at]
        date_range = ""
        if dates:
            min_date = min(dates)
            max_date = max(dates)
            date_range = f"{min_date.isoformat()} - {max_date.isoformat()}"
        
        return {
            "source_type": list(sources)[0] if sources else "unknown",
            "sources": list(sources),
            "participants": list(participants),
            "date_range": date_range,
            "units_count": len(units)
        }
    
    async def segment_all_groups(self) -> Dict[str, List[SegmentModel]]:
        """
        Выполняет сегментацию для всех групп в хранилище.
        
        Returns:
            Словарь с результатами сегментации по группам
        """
        try:
            # Получаем все уникальные group_id
            group_ids = await self._get_all_group_ids()
            
            logger.info(f"Found {len(group_ids)} groups for segmentation")
            
            results = {}
            for group_id in group_ids:
                segments = await self.segment_group(group_id)
                results[group_id] = segments
            
            return results
            
        except Exception as e:
            logger.error(f"Failed to segment all groups: {e}", exc_info=True)
            return {}
    
    async def _get_units_by_group(self, group_id: str) -> List[NormalizedUnit]:
        """
        Получает все нормализованные юниты для указанной группы.
        
        Args:
            group_id: ID группы
            
        Returns:
            Список нормализованных юнитов
        """
        # Используем метод list_by_group если он доступен
        if hasattr(self.knowledge_store, 'list_by_group'):
            return await self.knowledge_store.list_by_group(group_id)
        
        # Иначе получаем все юниты и фильтруем
        # TODO: Это неэффективно для больших объемов данных
        all_units = await self.knowledge_store.list_all()
        return [unit for unit in all_units if unit.group_id == group_id]
    
    async def _get_all_group_ids(self) -> List[str]:
        """
        Получает все уникальные ID групп из хранилища.
        
        Returns:
            Список уникальных group_id
        """
        # Используем метод list_group_ids если он доступен
        if hasattr(self.knowledge_store, 'list_group_ids'):
            return list(await self.knowledge_store.list_group_ids())
        
        # Иначе получаем все юниты и извлекаем уникальные group_id
        # TODO: Это неэффективно для больших объемов данных
        all_units = await self.knowledge_store.list_all()
        group_ids = set()
        for unit in all_units:
            if unit.group_id:
                group_ids.add(unit.group_id)
        
        return list(group_ids)
    
    async def _select_segmentation_provider(self, archetype: str, metadata: Dict[str, Any]) -> Optional[SegmentationProvider]:
        """
        Выбирает провайдер сегментации на основе архетипа и метаданных юнита.
        
        Args:
            archetype: Архетип юнита
            metadata: Метаданные юнита
            
        Returns:
            Экземпляр провайдера сегментации или None
        """
        try:
            # Получаем все провайдеры
            providers = self.provider_service.get_all_providers()
            
            # Фильтруем провайдеры сегментации
            segmentation_providers = [
                p for p in providers 
                if p.provider_type == ProviderType.SEGMENTATION
            ]
            
            if not segmentation_providers:
                logger.warning("No segmentation providers found in system")
                return self._create_fallback_provider()
            
            # Выбираем провайдер через селектор
            provider_model = ProviderSelector.select_provider(
                providers=[p.dict(exclude={"instance"}) for p in segmentation_providers],
                provider_type=ProviderType.SEGMENTATION.value,
                archetype=archetype,
                source=(metadata or {}).get('source'),
                metadata=metadata or {}
            )
            
            if not provider_model:
                logger.warning("No segmentation provider selected by ProviderSelector, using fallback")
                return self._create_fallback_provider()
            
            # Создаем экземпляр провайдера
            provider_class = self._get_provider_class(provider_model.get('id'))
            if not provider_class:
                logger.error(f"Provider class not found for {provider_model.get('id')}, using fallback")
                return self._create_fallback_provider()
            
            try:
                provider_instance = provider_class(provider_model.get('current_config', {}))
                logger.info(f"Successfully created segmentation provider: {provider_model.get('id')}")
                return provider_instance
            except Exception as e:
                logger.error(f"Failed to create provider instance for {provider_model.get('id')}: {e}, using fallback")
                return self._create_fallback_provider()
                
        except Exception as e:
            logger.error(f"Error in provider selection: {e}, using fallback provider")
            return self._create_fallback_provider()
    
    def _create_fallback_provider(self) -> Optional[SegmentationProvider]:
        """
        Создает fallback провайдер (Mock) в случае недоступности основных провайдеров.
        
        Returns:
            Экземпляр mock провайдера или None
        """
        try:
            from mindbank_poc.core.providers.segmentation import MockSegmentProvider
            logger.info("Using MockSegmentProvider as fallback")
            return MockSegmentProvider({})
        except Exception as e:
            logger.error(f"Failed to create fallback provider: {e}")
            return None
    
    def _get_provider_class(self, provider_id: str):
        """
        Получает класс провайдера по его ID.
        
        Args:
            provider_id: ID провайдера
            
        Returns:
            Класс провайдера или None
        """
        from mindbank_poc.core.providers.segmentation import (
            OpenAICompatibleSegmentProvider,
            MockSegmentProvider
        )
        
        # Маппинг ID провайдеров на классы
        provider_classes = {
            "openai-segmentation": OpenAICompatibleSegmentProvider,
            "mock-segmentation": MockSegmentProvider
        }
        
        return provider_classes.get(provider_id, MockSegmentProvider)
    
    async def _generate_segment_embedding(self, segment: SegmentModel) -> None:
        """
        Генерирует векторное представление для сегмента.
        
        Args:
            segment: Сегмент для которого нужно сгенерировать эмбеддинг
        """
        try:
            from mindbank_poc.core.normalizer.normalizer import ProviderRegistry
            
            # Получаем провайдер эмбеддингов
            embed_provider_class = ProviderRegistry.get_embed_provider(self.segment_embed_provider_id)
            if not embed_provider_class:
                logger.warning(f"Embed provider not found: {self.segment_embed_provider_id}")
                return
            
            # Создаем экземпляр провайдера
            embed_provider = embed_provider_class({})
            
            # Формируем текст для эмбеддинга
            text_for_embedding = f"{segment.title}. {segment.summary}"
            
            # Генерируем эмбеддинг
            vector = await embed_provider.embed_text(text_for_embedding)
            
            if vector:
                segment.vector_repr = vector
                logger.debug(f"Generated embedding for segment {segment.id} (dim: {len(vector)})")
            else:
                logger.warning(f"Failed to generate embedding for segment {segment.id}")
                
        except Exception as e:
            logger.error(f"Error generating embedding for segment {segment.id}: {e}")
            # Не прерываем процесс сегментации из-за ошибки эмбеддинга

    def _create_segment_timeline(self, unit_ids: List[str], units: List[NormalizedUnit]) -> Dict[str, Any]:
        """
        Создает timeline для сегмента на основе временных меток юнитов.
        
        Args:
            unit_ids: Список ID юнитов
            units: Список нормализованных юнитов
            
        Returns:
            Сгенерированный timeline со структурой start, end, key_moments
        """
        timestamps = []
        unit_timestamps = {}
        
        # Собираем временные метки юнитов (приоритет: created_at > content_timestamp > normalized_at)
        for unit_id in unit_ids:
            for unit in units:
                if unit.id == unit_id:
                    timestamp = None
                    
                    # Приоритет: оригинальное время создания контента
                    if hasattr(unit, 'created_at') and unit.created_at:
                        timestamp = unit.created_at
                    elif hasattr(unit, 'content_timestamp') and unit.content_timestamp:
                        timestamp = unit.content_timestamp
                    elif unit.normalized_at:
                        timestamp = unit.normalized_at
                    
                    if timestamp:
                        timestamps.append(timestamp)
                        unit_timestamps[unit_id] = timestamp.isoformat()
                    break
        
        # Создаем структурированный timeline
        timeline = {}
        
        if timestamps:
            timestamps.sort()
            timeline["start"] = timestamps[0].isoformat()
            timeline["end"] = timestamps[-1].isoformat()
            
            # Добавляем основные временные точки
            if len(timestamps) > 2:
                mid_idx = len(timestamps) // 2
                timeline["middle"] = timestamps[mid_idx].isoformat()
            
            # Добавляем детальную информацию по юнитам
            timeline["unit_timestamps"] = unit_timestamps
            timeline["duration_minutes"] = round((timestamps[-1] - timestamps[0]).total_seconds() / 60, 1) if len(timestamps) > 1 else 0
        else:
            # Fallback для юнитов без временных меток
            timeline["start"] = None
            timeline["end"] = None
            timeline["unit_timestamps"] = {}
            timeline["duration_minutes"] = 0
            
        return timeline
