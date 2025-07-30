"""
Fallback-провайдеры для нормализации контента в offline-режиме.
"""
from typing import Any, Dict, List, Optional
from mindbank_poc.common.logging import get_logger
from .base import (
    TranscriptProvider,
    CaptionProvider,
    EmbedProvider,
    ClassifierProvider,
    FilePreviewProvider
)

logger = get_logger(__name__)


class FallbackCaptionProvider(CaptionProvider):
    """Fallback-провайдер для описаний изображений."""
    async def generate_caption(self, image_data: Optional[bytes], metadata: Dict[str, Any]) -> str:
        filename = metadata.get("filename", "unknown file")
        width = metadata.get("width")
        height = metadata.get("height")
        size_bytes = metadata.get("size_bytes")
        
        parts = [f"Image file: {filename}"]
        if width and height:
            parts.append(f"dimensions: {width}x{height}")
        if size_bytes:
            parts.append(f"size: {size_bytes} bytes")
            
        return ", ".join(parts)


class FallbackTranscriptProvider(TranscriptProvider):
    """Fallback-провайдер для транскрипции аудио/видео."""
    async def transcribe(self, media_data: Optional[bytes], metadata: Dict[str, Any]) -> str:
        filename = metadata.get("filename", "unknown file")
        duration = metadata.get("duration")
        size_bytes = metadata.get("size_bytes")
        media_type = metadata.get("media_type", "Media") # Определить бы тип из payload/metadata

        parts = [f"{media_type.capitalize()} file: {filename}"]
        if duration:
            # Преобразуем секунды в минуты/секунды для читаемости
            minutes = int(duration // 60)
            seconds = int(duration % 60)
            parts.append(f"duration: {minutes}m {seconds}s")
        if size_bytes:
            parts.append(f"size: {size_bytes} bytes")

        return ", ".join(parts)


class FallbackEmbedProvider(EmbedProvider):
    """Fallback-провайдер для векторизации текста."""
    async def embed_text(self, text: str) -> Optional[List[float]]:
        # Возвращает None, так как в offline-режиме векторизация невозможна
        return None


class FallbackClassifierProvider(ClassifierProvider):
    """Fallback-провайдер для классификации контента."""
    async def classify(self, text: str, metadata: Dict[str, Any]) -> Dict[str, Any]:
        # Возвращает базовую классификацию
        content_type = metadata.get("main_type", "unknown")
        return {
            "type": content_type,
            "topic": "general",
            "sentiment": "neutral",
            "language": "unknown",
            "complexity": "unknown"
        }


class FallbackFilePreviewProvider(FilePreviewProvider):
    """Fallback-провайдер для превью файлов."""
    async def get_preview(self, payload: Dict[str, Any]) -> str:
        text_preview = payload.get("text_preview")
        filename = payload.get("filename", "unknown file")
        size_bytes = payload.get("size_bytes")
        
        parts = []
        if text_preview:
            parts.append(f"File preview: {text_preview}")
        else:
            parts.append(f"File: {filename}")
            
        if size_bytes:
            parts.append(f"size: {size_bytes} bytes")
            
        return ", ".join(parts)


def register_fallback_providers():
    """Регистрирует Fallback провайдеры нормализации."""
    from mindbank_poc.core.services.provider_service import get_provider_service
    from mindbank_poc.core.models.provider import ProviderModel
    from mindbank_poc.core.common.types import ProviderType
    
    provider_service = get_provider_service()
    
    # Проверяем существующие провайдеры нормализации
    existing_providers = {
        p.id: p for p in provider_service.get_all_providers()
    }
    
    # Fallback Transcription Provider
    if "fallback-transcription" not in existing_providers:
        transcription_provider = ProviderModel(
            id="fallback-transcription",
            name="Fallback Transcription",
            provider_type=ProviderType.TRANSCRIPTION,
            description="Simple fallback transcription provider for offline mode",
            config_schema={},
            current_config={}
        )
        provider_service.register_provider(transcription_provider)
        logger.info("Registered new Fallback transcription provider")
    else:
        logger.info("Fallback transcription provider already exists, keeping existing configuration")
    
    # Fallback Caption Provider
    if "fallback-caption" not in existing_providers:
        caption_provider = ProviderModel(
            id="fallback-caption",
            name="Fallback Caption",
            provider_type=ProviderType.CAPTION,
            description="Simple fallback caption provider for offline mode",
            config_schema={},
            current_config={}
        )
        provider_service.register_provider(caption_provider)
        logger.info("Registered new Fallback caption provider")
    else:
        logger.info("Fallback caption provider already exists, keeping existing configuration")
    
    # Fallback Embedding Provider
    if "fallback-embedding" not in existing_providers:
        embedding_provider = ProviderModel(
            id="fallback-embedding",
            name="Fallback Embeddings",
            provider_type=ProviderType.EMBEDDING,
            description="Simple fallback embedding provider for offline mode",
            config_schema={},
            current_config={}
        )
        provider_service.register_provider(embedding_provider)
        logger.info("Registered new Fallback embedding provider")
    else:
        logger.info("Fallback embedding provider already exists, keeping existing configuration")
    
    # Fallback Classification Provider
    if "fallback-classifier" not in existing_providers:
        classifier_provider = ProviderModel(
            id="fallback-classifier",
            name="Fallback Classifier",
            provider_type=ProviderType.CLASSIFICATION,
            description="Simple fallback classification provider for offline mode",
            config_schema={},
            current_config={}
        )
        provider_service.register_provider(classifier_provider)
        logger.info("Registered new Fallback classifier provider")
    else:
        logger.info("Fallback classifier provider already exists, keeping existing configuration")
    
    logger.info(f"Fallback normalization providers registration completed. Total new providers: {4 - len([p for p in ['fallback-transcription', 'fallback-caption', 'fallback-embedding', 'fallback-classifier'] if p in existing_providers])}") 