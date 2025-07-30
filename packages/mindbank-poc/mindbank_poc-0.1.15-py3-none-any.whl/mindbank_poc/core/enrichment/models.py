"""
Модели данных для системы обогащения (Enrichment/Segmentation).
"""
from datetime import datetime
from typing import Any, Dict, List, Optional
from uuid import uuid4

from pydantic import BaseModel, Field


class SegmentModel(BaseModel):
    """
    Модель сегмента знаний.
    Представляет собой осмысленную единицу, объединяющую несколько нормализованных юнитов.
    """
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Уникальный идентификатор сегмента"
    )
    group_id: str = Field(
        description="Идентификатор долговечной группы (чат, митинг, переписка)"
    )
    title: str = Field(
        description="Осмысленное название сегмента"
    )
    summary: str = Field(
        description="Краткое резюме содержимого сегмента"
    )
    raw_unit_ids: List[str] = Field(
        default_factory=list,
        description="Список идентификаторов нормализованных юнитов, входящих в сегмент"
    )
    vector_repr: Optional[List[float]] = Field(
        default=None,
        description="Векторное представление сегмента для поиска"
    )
    entities: List[str] = Field(
        default_factory=list,
        description="Извлеченные сущности (имена, организации, даты и т.д.)"
    )
    timeline: Dict[str, Any] = Field(
        default_factory=dict,
        description="Временные рамки сегмента (начало, конец, ключевые моменты)"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Дополнительные метаданные сегмента"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Время создания сегмента"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "seg-12345",
                "group_id": "group-67890",
                "title": "Обсуждение технических требований",
                "summary": "Команда обсудила требования к новому API, включая аутентификацию, форматы данных и производительность",
                "raw_unit_ids": ["unit-1", "unit-2", "unit-3"],
                "vector_repr": [0.1, 0.2, 0.3, 0.4, 0.5],
                "entities": ["API", "OAuth 2.0", "JSON", "REST"],
                "timeline": {
                    "start": "2025-05-30T10:00:00Z",
                    "end": "2025-05-30T10:30:00Z",
                    "key_moments": ["10:15 - решение об OAuth", "10:25 - выбор JSON"]
                },
                "metadata": {
                    "participants": ["john@example.com", "jane@example.com"],
                    "importance": "high"
                },
                "created_at": "2025-05-30T11:00:00Z"
            }
        }


class SegmentExtractionResult(BaseModel):
    """
    Результат извлечения сегментов из группы юнитов.
    """
    segments: List[Dict[str, Any]] = Field(
        description="Список извлеченных сегментов"
    )
    
    class Config:
        json_schema_extra = {
            "example": {
                "segments": [
                    {
                        "title": "Технические требования",
                        "summary": "Обсуждение API и форматов данных",
                        "unit_indices": [0, 1, 2],
                        "entities": ["API", "JSON", "REST"],
                        "timeline": {"start": 0, "end": 15}
                    },
                    {
                        "title": "Решения по безопасности",
                        "summary": "Выбор OAuth 2.0 для аутентификации",
                        "unit_indices": [3, 4],
                        "entities": ["OAuth 2.0", "JWT"],
                        "timeline": {"start": 15, "end": 25}
                    }
                ]
            }
        }


class ClusterModel(BaseModel):
    """
    Модель кластера знаний.
    Представляет собой тематическую группу, объединяющую несколько сегментов.
    """
    id: str = Field(
        default_factory=lambda: str(uuid4()),
        description="Уникальный идентификатор кластера"
    )
    title: str = Field(
        description="Осмысленное название кластера"
    )
    summary: str = Field(
        description="Краткое описание тематики кластера"
    )
    keywords: List[str] = Field(
        default_factory=list,
        description="Ключевые слова и термины, характеризующие кластер"
    )
    segment_ids: List[str] = Field(
        default_factory=list,
        description="Список идентификаторов сегментов, входящих в кластер"
    )
    centroid: Optional[List[float]] = Field(
        default=None,
        description="Центроид кластера в векторном пространстве"
    )
    cluster_size: Optional[int] = Field(
        default=None,
        description="Количество сегментов в кластере (автоматически вычисляется)"
    )
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        description="Время создания кластера"
    )
    metadata: Dict[str, Any] = Field(
        default_factory=dict,
        description="Дополнительные метаданные кластера"
    )
    
    def model_post_init(self, __context) -> None:
        """Автоматически вычисляем cluster_size если не задан."""
        if self.cluster_size is None:
            self.cluster_size = len(self.segment_ids)
    
    class Config:
        json_schema_extra = {
            "example": {
                "id": "cluster-98765",
                "title": "Техническая разработка API",
                "summary": "Кластер объединяет сегменты о планировании, дизайне и реализации API",
                "keywords": ["API", "REST", "разработка", "архитектура", "безопасность"],
                "segment_ids": ["seg-12345", "seg-23456", "seg-34567"],
                "centroid": [0.15, 0.25, 0.35, 0.45, 0.55],
                "cluster_size": 3,
                "created_at": "2025-06-04T12:00:00Z",
                "metadata": {
                    "clustering_provider": "KMeansClusterProvider",
                    "clustering_algorithm": "kmeans+umap",
                    "silhouette_score": 0.76
                }
            }
        }
