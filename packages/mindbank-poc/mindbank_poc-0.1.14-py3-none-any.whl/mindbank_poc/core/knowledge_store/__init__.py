"""
Модуль для работы с хранилищем знаний (Knowledge Store).
""" 

from typing import Dict, Any, Optional

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings
from .base import KnowledgeStore

logger = get_logger(__name__)

# Переменная для хранения единственного экземпляра хранилища (singleton)
_knowledge_store_instance: Optional[KnowledgeStore] = None

def get_knowledge_store(config: Optional[Dict[str, Any]] = None) -> KnowledgeStore:
    """
    Фабрика для создания или получения хранилища знаний.
    
    Если хранилище уже было создано, возвращает существующий экземпляр (singleton).
    По умолчанию создает хранилище на основе настроек в конфигурации.
    
    Args:
        config: Конфигурация хранилища, если нужны особые параметры
        
    Returns:
        Экземпляр хранилища знаний (KnowledgeStore)
    """
    global _knowledge_store_instance
    
    # Если уже есть экземпляр, возвращаем его
    if _knowledge_store_instance is not None:
        logger.debug("Returning existing knowledge store instance")
        return _knowledge_store_instance
    
    # Если нет, создаем новый
    config = config or {}
    
    # Определяем тип хранилища
    if "store_type" in config:
        store_type = config["store_type"]
    elif hasattr(settings.storage, "store_type"):
        store_type = settings.storage.store_type
    else:
        # По умолчанию используем JSONL для простоты
        store_type = "jsonl"
    
    logger.info(f"Creating knowledge store of type: {store_type}")
    
    # Создаем хранилище в зависимости от типа с ленивой загрузкой
    if store_type == "jsonl":
        logger.info("Using JSONLKnowledgeStore (JSONL file-based storage)")
        from .jsonl_store import JSONLKnowledgeStore
        _knowledge_store_instance = JSONLKnowledgeStore(config)
    elif store_type == "chroma":
        logger.info("Using ChromaKnowledgeStore (ChromaDB vector storage)")
        from .chroma_store import ChromaKnowledgeStore
        _knowledge_store_instance = ChromaKnowledgeStore(config)
    else:
        # Если указан неизвестный тип, выдаем ошибку
        raise ValueError(
            f"Unknown knowledge store type: {store_type}. "
            f"Supported types are: 'jsonl', 'chroma'"
        )
    
    logger.info(f"Knowledge store instance created successfully (type: {store_type})")
    return _knowledge_store_instance 