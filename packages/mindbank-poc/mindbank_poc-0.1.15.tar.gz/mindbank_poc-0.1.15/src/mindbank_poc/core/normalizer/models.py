"""
Модели данных для нормализованных единиц.
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
import uuid

from pydantic import BaseModel, Field


class NormalizedUnit(BaseModel):
    """
    Модель нормализованной единицы знаний.
    Представляет собой результат обработки агрегата в единую единицу,
    готовую для сохранения в базу знаний.
    """
    id: str = Field(
        default_factory=lambda: str(uuid.uuid4()),
        description="Уникальный идентификатор нормализованной единицы"
    )
    aggregate_id: str = Field(
        ..., 
        description="ID исходного агрегата, из которого создан юнит"
    )
    group_id: Optional[str] = Field(
        default=None, 
        description="ID долговечной группы (чат, митинг, переписка и т.д.)"
    )
    text_repr: str = Field(
        description="Текстовое представление содержимого"
    )
    vector_repr: Optional[List[float]] = Field(
        default=None,
        description="Векторное представление для поиска по семантике"
    )
    archetype: Optional[str] = Field(
        default=None,
        description="Семантический тип (архитип) контента"
    )
    classification: Dict[str, Any] = Field(
        default_factory=dict,
        description="Классификация контента по типу, теме и другим параметрам"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Метаданные единицы знаний"
    )
    
    # ВРЕМЕННЫЕ ПОЛЯ
    created_at: Optional[datetime] = Field(
        default=None,
        description="Время создания оригинального контента (из entry.metadata.date)"
    )
    normalized_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Время нормализации"
    )
    
    # НОВЫЕ ПОЛЯ для временной информации контента
    content_timestamp: Optional[datetime] = Field(
        default=None,
        description="Оригинальное время контента (для одиночной записи) или начало временного диапазона"
    )
    content_end_timestamp: Optional[datetime] = Field(
        default=None,
        description="Конец временного диапазона контента (для агрегатов с несколькими записями)"
    )
    content_duration_seconds: Optional[float] = Field(
        default=None,
        description="Длительность контента в секундах (для медиафайлов, встреч, диалогов)"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "aggregate_id": "agg-12345",
                "group_id": "group-67890",
                "text_repr": "Текстовое представление контента, возможно получено через транскрипцию или описание",
                "vector_repr": [0.1, 0.2, 0.3, 0.4, 0.5],  # Может быть null
                "classification": {"type": "text", "topic": "business"},
                "metadata": {
                    "source": "slack",
                    "channel": "general",
                    "author": "user123",
                    "content_temporal_range": {
                        "start": "2023-07-01T09:00:00Z",
                        "end": "2023-07-01T10:30:00Z",
                        "duration_seconds": 5400
                    }
                },
                "normalized_at": "2023-07-01T12:34:56.789Z",
                "content_timestamp": "2023-07-01T09:00:00Z",
                "content_end_timestamp": "2023-07-01T10:30:00Z",
                "content_duration_seconds": 5400.0
            }
        }


class ProviderConfig(BaseModel):
    """Конфигурация для провайдера нормализации."""
    name: str = Field(
        description="Имя провайдера"
    )
    enabled: bool = Field(
        default=False,
        description="Включен ли провайдер"
    )
    params: Dict[str, Any] = Field(
        default_factory=dict,
        description="Дополнительные параметры провайдера"
    )
    
    
class NormalizerConfig(BaseModel):
    """Конфигурация нормализатора."""
    transcript: ProviderConfig = Field(
        default_factory=lambda: ProviderConfig(name="fallback", enabled=True),
        description="Провайдер для транскрипции аудио/видео"
    )
    caption: ProviderConfig = Field(
        default_factory=lambda: ProviderConfig(name="fallback", enabled=True),
        description="Провайдер для генерации описаний изображений"
    )
    embed: ProviderConfig = Field(
        default_factory=lambda: ProviderConfig(name="fallback", enabled=True),
        description="Провайдер для векторизации текста"
    )
    classifier: ProviderConfig = Field(
        default_factory=lambda: ProviderConfig(name="fallback", enabled=True),
        description="Провайдер для классификации контента"
    )
