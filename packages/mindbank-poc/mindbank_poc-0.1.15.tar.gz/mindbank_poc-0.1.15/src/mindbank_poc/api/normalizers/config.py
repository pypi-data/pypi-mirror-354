"""
Конфигурация нормализатора в API.
"""
from pathlib import Path
import os
from typing import Dict, Any, Optional

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.normalizer.models import NormalizerConfig, ProviderConfig
from mindbank_poc.core.config.settings import settings, settings_logger
from mindbank_poc.core.common.types import ProviderType
from mindbank_poc.core.services.provider_service import get_provider_service

logger = get_logger(__name__)


def load_config(config_path: Optional[Path] = None) -> NormalizerConfig:
    """
    Загружает конфигурацию нормализатора из настроек.
    
    Конфигурация берется из настроек окружения (.env файл).
    
    Args:
        config_path: Путь к конфигурационному файлу (игнорируется, оставлен для совместимости)
        
    Returns:
        Конфигурация нормализатора
    """    
    # Используем настройки из .env
    logger.info("Using normalizer config from environment variables")
    settings_logger.info(f"[load_config] Initial settings.normalizer.offline_mode: {settings.normalizer.offline_mode} (type: {type(settings.normalizer.offline_mode)})" )
    
    # Принудительная проверка для отладки
    # Проверяем переменную среды напрямую
    env_offline_mode = os.getenv("NORMALIZER_OFFLINE_MODE", "").lower()
    is_offline = env_offline_mode in ("true", "1", "yes", "y", "on") or settings.normalizer.offline_mode is True
    
    if is_offline:
        logger.info("Offline mode is enabled, using fallback providers regardless of provider settings")
        transcript_provider = "fallback"
        caption_provider = "fallback"
        embed_provider = "fallback"
        classifier_provider = "fallback"
    else:
        logger.info(f"Using configured providers: "
                  f"transcript={settings.normalizer.transcript_provider}, "
                  f"caption={settings.normalizer.caption_provider}, "
                  f"embed={settings.normalizer.embed_provider}, "
                  f"classifier={settings.normalizer.classifier_provider}")
        transcript_provider = settings.normalizer.transcript_provider
        caption_provider = settings.normalizer.caption_provider
        embed_provider = settings.normalizer.embed_provider
        classifier_provider = settings.normalizer.classifier_provider

    # Clear the cache to ensure we get fresh data from the repository
    get_provider_service.cache_clear()
    logger.debug("Provider service cache cleared before loading normalizer config")
    
    # Get provider service
    provider_service = get_provider_service()
    
    # Функция для поиска провайдера по типу и предпочтению
    def find_provider(provider_type: ProviderType, preferred_type: str):
        """Находит провайдер нужного типа с учетом предпочтений (openai/fallback)."""
        providers = provider_service.get_providers_by_type(provider_type)
        
        if not providers:
            logger.warning(f"No providers found for type {provider_type}")
            return None
            
        # Определяем префикс ID на основе предпочтения
        if preferred_type == "fallback":
            preferred_prefix = "fallback-"
        elif preferred_type == "openai":
            preferred_prefix = "openai-"
        else:
            logger.warning(f"Unknown provider type preference: {preferred_type}, using fallback")
            preferred_prefix = "fallback-"
        
        # Ищем провайдер с нужным префиксом
        for provider in providers:
            if provider.id.startswith(preferred_prefix):
                logger.info(f"Found {provider_type} provider: {provider.id}")
                return provider
        
        # Если предпочтительный не найден, ищем fallback
        for provider in providers:
            if provider.id.startswith("fallback-"):
                logger.warning(f"Preferred {preferred_prefix} provider not found for {provider_type}, using fallback: {provider.id}")
                return provider
        
        # Если вообще ничего не найдено, берем первый доступный
        logger.warning(f"No fallback provider found for {provider_type}, using first available: {providers[0].id}")
        return providers[0]

    # Находим нужные провайдеры
    transcript_provider_model = find_provider(ProviderType.TRANSCRIPTION, transcript_provider)
    caption_provider_model = find_provider(ProviderType.CAPTION, caption_provider)
    embed_provider_model = find_provider(ProviderType.EMBEDDING, embed_provider)
    classifier_provider_model = find_provider(ProviderType.CLASSIFICATION, classifier_provider)

    logger.debug(f"Selected providers: "
                f"transcript={transcript_provider_model.id if transcript_provider_model else 'None'}, "
                f"caption={caption_provider_model.id if caption_provider_model else 'None'}, "
                f"embed={embed_provider_model.id if embed_provider_model else 'None'}, "
                f"classifier={classifier_provider_model.id if classifier_provider_model else 'None'}")
    
    # Создаем конфигурацию нормализатора на основе найденных провайдеров
    normalizer_config = NormalizerConfig(
        transcript=ProviderConfig(
            name=transcript_provider_model.id if transcript_provider_model else "fallback",
            enabled=settings.normalizer.enable_transcript,
            params=transcript_provider_model.current_config if transcript_provider_model else {}
        ),
        caption=ProviderConfig(
            name=caption_provider_model.id if caption_provider_model else "fallback",
            enabled=settings.normalizer.enable_caption,
            params=caption_provider_model.current_config if caption_provider_model else {}
        ),
        embed=ProviderConfig(
            name=embed_provider_model.id if embed_provider_model else "fallback",
            enabled=settings.normalizer.enable_embed,
            params=embed_provider_model.current_config if embed_provider_model else {}
        ),
        classifier=ProviderConfig(
            name=classifier_provider_model.id if classifier_provider_model else "fallback",
            enabled=settings.normalizer.enable_classifier,
            params=classifier_provider_model.current_config if classifier_provider_model else {}
        )
    )
    
    settings_logger.info(f"[load_config] Created NormalizerConfig from provider service: {normalizer_config.model_dump_json(indent=2)}")
    return normalizer_config