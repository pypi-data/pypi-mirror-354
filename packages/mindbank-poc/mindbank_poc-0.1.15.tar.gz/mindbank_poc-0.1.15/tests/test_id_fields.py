"""
Тесты для проверки новых ID полей в моделях данных.
"""
import pytest
from datetime import datetime
from mindbank_poc.core.common.types import Aggregate, RawEntry, ArchetypeType
from mindbank_poc.core.normalizer.models import NormalizedUnit


def test_aggregate_has_unique_id():
    """Проверяет, что Aggregate автоматически генерирует уникальный ID."""
    # Создаем два агрегата
    agg1 = Aggregate(
        group_id="test-group-1",
        entries=[
            RawEntry(
                collector_id="test-collector",
                group_id="test-group-1",
                entry_id="entry-1",
                type="text",
                payload={"text": "Test entry 1"},
                metadata={},
                timestamp=datetime.now()
            )
        ]
    )
    
    agg2 = Aggregate(
        group_id="test-group-1",
        entries=[
            RawEntry(
                collector_id="test-collector",
                group_id="test-group-1",
                entry_id="entry-2",
                type="text",
                payload={"text": "Test entry 2"},
                metadata={},
                timestamp=datetime.now()
            )
        ]
    )
    
    # Проверяем, что ID существуют
    assert agg1.id is not None
    assert agg2.id is not None
    
    # Проверяем, что ID уникальны
    assert agg1.id != agg2.id
    
    # Проверяем формат ID (должен быть UUID)
    assert len(agg1.id) == 36  # UUID с дефисами
    assert '-' in agg1.id


def test_normalized_unit_has_unique_id():
    """Проверяет, что NormalizedUnit автоматически генерирует уникальный ID."""
    # Создаем два нормализованных юнита
    unit1 = NormalizedUnit(
        aggregate_id="agg-123",
        text_repr="Test text 1",
        normalized_at=datetime.now()
    )
    
    unit2 = NormalizedUnit(
        aggregate_id="agg-456",
        text_repr="Test text 2",
        normalized_at=datetime.now()
    )
    
    # Проверяем, что ID существуют
    assert unit1.id is not None
    assert unit2.id is not None
    
    # Проверяем, что ID уникальны
    assert unit1.id != unit2.id
    
    # Проверяем формат ID
    assert len(unit1.id) == 36
    assert '-' in unit1.id


def test_aggregate_preserves_explicit_id():
    """Проверяет, что явно указанный ID сохраняется."""
    explicit_id = "custom-aggregate-id-123"
    
    agg = Aggregate(
        id=explicit_id,
        group_id="test-group",
        entries=[]
    )
    
    assert agg.id == explicit_id


def test_normalized_unit_preserves_explicit_id():
    """Проверяет, что явно указанный ID сохраняется."""
    explicit_id = "custom-unit-id-456"
    
    unit = NormalizedUnit(
        id=explicit_id,
        aggregate_id="agg-123",
        text_repr="Test text",
        normalized_at=datetime.now()
    )
    
    assert unit.id == explicit_id


def test_aggregate_serialization_includes_id():
    """Проверяет, что ID включается в сериализацию."""
    agg = Aggregate(
        group_id="test-group",
        entries=[]
    )
    
    # Сериализуем в dict
    agg_dict = agg.model_dump()
    
    # Проверяем, что ID присутствует
    assert "id" in agg_dict
    assert agg_dict["id"] == agg.id
    
    # Проверяем десериализацию
    agg_restored = Aggregate.model_validate(agg_dict)
    assert agg_restored.id == agg.id 