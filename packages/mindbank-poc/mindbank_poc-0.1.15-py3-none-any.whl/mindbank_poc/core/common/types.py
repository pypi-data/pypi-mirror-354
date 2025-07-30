from datetime import datetime
from typing import Any, Dict, List, Optional, Literal, Union
from pydantic import BaseModel, Field
from enum import Enum, auto
import uuid

class ProviderType(str, Enum):
    """Типы провайдеров обработки данных."""
    EMBEDDING = "embedding"
    CLASSIFICATION = "classification"
    TRANSCRIPTION = "transcription"
    CAPTION = "caption"
    LLM_CHAT = "llm_chat"
    SEGMENTATION = "segmentation"
    CLUSTERING = "clustering"

# Определяем литеральные типы для содержимого
ContentType = Literal["text", "image", "video", "audio", "link", "code", "file", "unknown"]

# Определяем литеральные типы для архитипов
ArchetypeType = str  # Упрощенный тип для архетипов - теперь любая строка может быть архетипом

# Предопределенные архетипы (для обратной совместимости и документации)
PREDEFINED_ARCHETYPES = [
    "document", "note", "meeting_notes", "transcription", 
    "code_snippet", "chat", "email", "task", "generic"
]

class RawEntry(BaseModel):
    """Сырая запись от коллектора данных."""
    collector_id: str = Field(
        description="Уникальный идентификатор коллектора"
    )
    group_id: str = Field(
        description="Идентификатор группы, к которой принадлежит запись"
    )
    entry_id: str = Field(
        description="Уникальный идентификатор записи"
    )
    type: ContentType = Field(
        description="Тип содержимого записи"
    )
    archetype: Optional[ArchetypeType] = Field(
        default=None,
        description="Семантический тип (архитип) контента"
    )
    payload: Dict[str, Any] = Field(
        description="Данные записи"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Метаданные записи (могут содержать 'is_last' и опционально 'group_timeout_seconds')"
    )
    timestamp: datetime = Field(
        default_factory=datetime.utcnow,
        description="Время создания записи"
    )

class Aggregate(BaseModel):
    """Агрегат - группа связанных записей."""
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Уникальный идентификатор агрегата"
    )
    group_id: str = Field(
        description="Уникальный идентификатор группы"
    )
    entries: List[RawEntry] = Field(
        description="Список записей в группе"
    )
    archetype: Optional[ArchetypeType] = Field(
        default=None,
        description="Семантический тип (архитип) агрегата"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Метаданные агрегата"
    )
    aggregated_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Время создания агрегата"
    )
    
    # НОВЫЕ ПОЛЯ для временной информации
    content_start_time: Optional[datetime] = Field(
        default=None,
        description="Время самой ранней записи в агрегате (оригинальное время контента)"
    )
    content_end_time: Optional[datetime] = Field(
        default=None,
        description="Время самой поздней записи в агрегате (оригинальное время контента)"
    )
    
    # УЛУЧШЕННЫЕ метаданные для сохранения контекста записей
    entries_metadata: List[Dict[str, Any]] = Field(
        default_factory=list,
        description="Метаданные всех записей для сохранения полного контекста"
    )
