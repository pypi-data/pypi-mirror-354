"""
Провайдеры для сегментации контента.
"""
import json
from contextlib import contextmanager
from typing import Any, Dict, List, Optional

import dspy
from openai import AsyncOpenAI

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings
from mindbank_poc.core.enrichment.models import SegmentExtractionResult
from .base import BaseProvider

logger = get_logger(__name__)


class SegmentationProvider(BaseProvider):
    """Базовый класс для провайдеров сегментации."""
    
    async def extract_segments(self, units_text: str, group_metadata: Dict[str, Any]) -> SegmentExtractionResult:
        """
        Извлекает сегменты из текста нормализованных юнитов.
        
        Args:
            units_text: Объединенный текст юнитов группы
            group_metadata: Метаданные группы
            
        Returns:
            Результат извлечения сегментов
        """
        raise NotImplementedError


class SegmentExtractionSig(dspy.Signature):
    """
    Extract semantic segments from a window of normalized content units.
    
    Analyze the content and identify coherent thematic segments.
    Return ONLY a JSON array of segments:
    [{"start": 1, "end": 14, "title": "Topic Title", "summary": "Brief description of the segment content"}]
    
    Guidelines:
    - Indices are 1-based within the WHOLE group
    - Each segment should cover 3-40 units typically
    - Title should be descriptive and in English
    - Summary should capture the main points discussed/covered
    - Segments should be coherent and thematically unified
    """
    content_window: str = dspy.InputField(desc="Window of content from normalized units")
    group_context: str = dspy.InputField(desc="Context about the content group (type, source, participants, etc.)")
    segments: str = dspy.OutputField(desc="JSON array of semantic segments with start, end, title, and summary")


class OpenAICompatibleSegmentProvider(SegmentationProvider):
    """
    Провайдер сегментации на основе OpenAI-compatible API.
    Использует DSPy для структурированного извлечения сегментов.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Инициализация провайдера.
        
        Args:
            config: Конфигурация провайдера (model, api_key, base_url)
        """
        super().__init__(config)
        
        # Получаем только необходимые параметры
        self.api_key = config.get("api_key") if config else None
        self.model = config.get("model", "gpt-4o-mini") if config else "gpt-4o-mini"
        self.base_url = config.get("base_url") if config else None
        
        # Если API ключ не указан, это не критично - просто не будем работать
        if not self.api_key:
            logger.warning("API key not provided for OpenAICompatibleSegmentProvider - provider will be non-functional")
            self.lm = None
            self.segment_extractor = None
            return
        
        try:
            # Создаем LM instance
            self.lm = self._create_lm_instance()
            
            # Создаем модуль для извлечения сегментов
            self.segment_extractor = dspy.Predict(SegmentExtractionSig)
            
            logger.info(f"OpenAICompatibleSegmentProvider initialized with model: {self.model}")
        except Exception as e:
            logger.error(f"Failed to initialize OpenAI segmentation provider: {e}")
            self.lm = None
            self.segment_extractor = None
    
    def _create_lm_instance(self):
        """Создает экземпляр языковой модели DSPy."""
        if self.base_url:
            # Для кастомных OpenAI-compatible endpoints
            return dspy.LM(
                model=self.model,
                base_url=self.base_url,
                api_key=self.api_key,
                model_type="chat"
            )
        else:
            # Для стандартного OpenAI API
            return dspy.LM(
                model=self.model,
                api_key=self.api_key,
                model_type="chat"
            )
    
    @contextmanager
    def _with_dspy_context(self):
        """Context manager для изолированной DSPy конфигурации."""
        # Используем потокобезопасный способ через dspy.settings.context
        with dspy.settings.context(lm=self.lm, cache="no_cache"):
            yield

    async def extract_segments(self, units_text: str, group_metadata: Dict[str, Any]) -> SegmentExtractionResult:
        """
        Извлекает сегменты из текста нормализованных юнитов.
        
        Args:
            units_text: Объединенный текст юнитов группы
            group_metadata: Метаданные группы
            
        Returns:
            Результат извлечения сегментов
        """
        # Проверяем, инициализирован ли провайдер
        if not self.lm or not self.segment_extractor:
            logger.error("OpenAI segmentation provider is not properly initialized (missing API key or configuration)")
            return SegmentExtractionResult(segments=[])
        
        try:
            # Формируем информацию о группе
            group_info = self._format_group_info(group_metadata)
            
            # Вызываем DSPy для извлечения сегментов в изолированном контексте
            # DSPy работает синхронно, поэтому используем run_in_executor
            import asyncio
            loop = asyncio.get_event_loop()
            
            result = await loop.run_in_executor(
                None,
                self._extract_segments_sync,
                units_text,
                group_info
            )
            
            # Парсим JSON результат
            try:
                segments_data = json.loads(result.segments)
                
                # Валидируем структуру сегментов
                validated_segments = []
                for segment in segments_data:
                    if isinstance(segment, dict) and all(
                        key in segment for key in ["title", "summary"]
                    ):
                        # Для совместимости с текущей моделью добавляем unit_indices
                        # В будущем это будет заменено на raw_unit_ids на основе start/end
                        if "start" in segment and "end" in segment:
                            segment["unit_indices"] = list(range(segment["start"]-1, segment["end"]))
                        else:
                            segment.setdefault("unit_indices", [])
                        
                        # Добавляем дефолтные значения для опциональных полей
                        segment.setdefault("entities", [])
                        segment.setdefault("timeline", {})
                        validated_segments.append(segment)
                
                logger.info(f"Successfully extracted {len(validated_segments)} segments using OpenAI provider")
                return SegmentExtractionResult(segments=validated_segments)
                
            except json.JSONDecodeError as e:
                logger.error(f"Failed to parse segments JSON from OpenAI response: {e}")
                logger.debug(f"Raw response: {result.segments}")
                # Возвращаем пустой результат при ошибке парсинга
                return SegmentExtractionResult(segments=[])
                
        except Exception as e:
            logger.error(f"Failed to extract segments with OpenAI provider: {e}", exc_info=True)
            # Возвращаем пустой результат при ошибке
            return SegmentExtractionResult(segments=[])
    
    def _extract_segments_sync(self, units_text: str, group_info: str) -> Any:
        """
        Синхронная версия извлечения сегментов для использования с DSPy.
        
        Args:
            units_text: Текст юнитов
            group_info: Информация о группе
            
        Returns:
            Результат от DSPy
        """
        # Еще одна проверка на всякий случай
        if not self.lm or not self.segment_extractor:
            raise RuntimeError("Provider not properly initialized")
        
        # Используем контекстный менеджер для изолированной конфигурации
        with self._with_dspy_context():
            return self.segment_extractor(
                content_window=units_text,
                group_context=group_info
            )
    
    def _format_group_info(self, metadata: Dict[str, Any]) -> str:
        """
        Форматирует метаданные группы в текстовое описание.
        
        Args:
            metadata: Метаданные группы
            
        Returns:
            Текстовое описание группы
        """
        info_parts = []
        
        # Тип источника и контента
        source_type = metadata.get("source_type", "unknown")
        info_parts.append(f"Content type: {source_type}")
        
        # Количество юнитов для понимания объема
        units_count = metadata.get("units_count", 0)
        if units_count > 0:
            info_parts.append(f"Total units: {units_count}")
        
        # Участники (для чатов, митингов, etc.)
        participants = metadata.get("participants", [])
        if participants:
            participant_list = ", ".join(str(p) for p in participants[:5])  # Первые 5
            if len(participants) > 5:
                participant_list += f" and {len(participants) - 5} others"
            info_parts.append(f"Participants: {participant_list}")
        
        # Источники (для агрегированного контента)
        sources = metadata.get("sources", [])
        if sources and sources != [source_type]:
            sources_list = ", ".join(str(s) for s in sources[:3])  # Первые 3
            if len(sources) > 3:
                sources_list += f" and {len(sources) - 3} others"
            info_parts.append(f"Sources: {sources_list}")
        
        # Временной диапазон
        date_range = metadata.get("date_range", "")
        if date_range:
            info_parts.append(f"Time span: {date_range}")
        
        # Дополнительный контекст (если есть)
        context = metadata.get("context", "")
        if context:
            info_parts.append(f"Context: {context}")
        
        # Если нет метаданных, даем базовую информацию
        if not info_parts:
            return "Generic content group for segmentation"
        
        return " | ".join(info_parts)


class MockSegmentProvider(SegmentationProvider):
    """
    Мок-провайдер для тестирования и отключения сегментации.
    Полностью отключает процесс сегментации.
    """
    
    async def extract_segments(self, units_text: str, group_metadata: Dict[str, Any]) -> SegmentExtractionResult:
        """
        Мок-реализация сегментации - полностью отключает сегментацию.
        
        Args:
            units_text: Объединенный текст юнитов группы (игнорируется)
            group_metadata: Метаданные группы (игнорируются)
            
        Returns:
            Пустой результат (сегментация отключена)
        """
        logger.info(f"MockSegmentProvider: segmentation disabled, skipping processing of {len(units_text)} characters")
        return SegmentExtractionResult(segments=[])


# Функция для регистрации провайдеров сегментации
def register_segmentation_providers():
    """Регистрирует доступные провайдеры сегментации."""
    from mindbank_poc.core.services.provider_service import get_provider_service
    from mindbank_poc.core.models.provider import ProviderModel
    from mindbank_poc.core.common.types import ProviderType
    
    provider_service = get_provider_service()
    
    # Проверяем существующие провайдеры сегментации
    existing_providers = {
        p.id: p for p in provider_service.get_providers_by_type(ProviderType.SEGMENTATION)
    }
    
    # OpenAI Compatible Segment Provider
    if "openai-segmentation" not in existing_providers:
        openai_provider = ProviderModel(
            id="openai-segmentation",
            name="OpenAI Segmentation",
            provider_type=ProviderType.SEGMENTATION,
            description="Segmentation provider using OpenAI-compatible API with DSPy",
            config_schema={
                "api_key": {
                    "type": "string",
                    "description": "API key for OpenAI-compatible service"
                },
                "model": {
                    "type": "string",
                    "description": "Model to use for segmentation",
                    "default": "gpt-4o-mini"
                },
                "base_url": {
                    "type": "string",
                    "description": "Base URL for custom API endpoint (optional)"
                }
            },
            current_config={
                "model": "gpt-4o-mini",
                "base_url": None,
                "api_key": None
            },
            priority=10
        )
        provider_service.register_provider(openai_provider)
        logger.info("Registered new OpenAI segmentation provider")
    else:
        logger.info("OpenAI segmentation provider already exists, keeping existing configuration")
    
    # Mock Segment Provider
    if "mock-segmentation" not in existing_providers:
        mock_provider = ProviderModel(
            id="mock-segmentation",
            name="Mock Segmentation",
            provider_type=ProviderType.SEGMENTATION,
            description="Simple mock segmentation provider for testing",
            config_schema={},
            current_config={},
            priority=1
        )
        provider_service.register_provider(mock_provider)
        logger.info("Registered new Mock segmentation provider")
    else:
        logger.info("Mock segmentation provider already exists, keeping existing configuration")
    
    logger.info(f"Segmentation providers registration completed. Total providers: {len(existing_providers) + (2 - len([p for p in ['openai-segmentation', 'mock-segmentation'] if p in existing_providers]))}")
