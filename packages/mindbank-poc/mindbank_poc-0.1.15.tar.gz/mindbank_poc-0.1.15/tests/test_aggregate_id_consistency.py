"""
Интеграционный тест для проверки консистентности ID агрегатов через весь пайплайн.
Воспроизводит проблему потери связи между агрегатами и нормализованными юнитами.
"""
import pytest
import asyncio
import uuid
from pathlib import Path
from datetime import datetime

from mindbank_poc.core.common.types import Aggregate, RawEntry
from mindbank_poc.api.schemas import AggregateInput, RawEntryInput
from mindbank_poc.api.backends import jsonl_backend
from mindbank_poc.api.routers.ingest import _convert_aggregate_for_normalization, _process_aggregate
from mindbank_poc.core.normalizer.normalizer import Normalizer
from mindbank_poc.core.normalizer.models import NormalizerConfig, ProviderConfig
from mindbank_poc.core.knowledge_store import get_knowledge_store


@pytest.mark.asyncio
async def test_aggregate_id_consistency_full_pipeline():
    """
    Тест полного пайплайна: создание агрегата → сохранение → нормализация → поиск.
    Проверяет, что ID агрегата сохраняется на всех этапах.
    """
    # Шаг 1: Создаем агрегат как это делает коннектор (например, telegram)
    original_aggregate = Aggregate(
        group_id="test-chat-123",
        entries=[
            RawEntry(
                collector_id="telegram-001",
                group_id="test-chat-123", 
                entry_id=f"msg-{uuid.uuid4()}",
                type="text",
                payload={"content": "Test message content"},
                metadata={"author": "test_user"},
                timestamp=datetime.now()
            )
        ],
        metadata={"connector_type": "telegram"}
    )
    
    print(f"[TEST] Original Aggregate ID: {original_aggregate.id}")
    assert original_aggregate.id is not None
    assert len(original_aggregate.id) == 36  # UUID format
    
    # Шаг 2: Конвертируем в AggregateInput как в API endpoint
    aggregate_input = AggregateInput(
        id=original_aggregate.id,  # Явно передаем ID
        group_id=original_aggregate.group_id,
        entries=[
            RawEntryInput(
                collector_id=entry.collector_id,
                group_id=entry.group_id,
                entry_id=entry.entry_id,
                type=entry.type,
                payload=entry.payload,
                metadata=entry.metadata,
                timestamp=entry.timestamp
            )
            for entry in original_aggregate.entries
        ],
        metadata=original_aggregate.metadata
    )
    
    print(f"[TEST] AggregateInput ID: {aggregate_input.id}")
    assert aggregate_input.id == original_aggregate.id
    
    # Шаг 3: Сохраняем агрегат через JSONL backend
    await jsonl_backend.save_aggregate(aggregate_input)
    
    # Шаг 4: Загружаем агрегат обратно для проверки
    loaded_aggregate = await jsonl_backend.load_aggregate_by_id(original_aggregate.id)
    assert loaded_aggregate is not None
    assert loaded_aggregate.id == original_aggregate.id
    print(f"[TEST] Loaded Aggregate ID: {loaded_aggregate.id}")
    
    # Шаг 5: Конвертируем для нормализации
    aggregate_dict = _convert_aggregate_for_normalization(aggregate_input)
    print(f"[TEST] Normalized dict ID: {aggregate_dict.get('id')}")
    
    # Проверяем, что ID не потерялся при конвертации
    assert aggregate_dict.get("id") == original_aggregate.id
    
    # Шаг 6: Создаем нормализатор и обрабатываем агрегат
    normalizer_config = NormalizerConfig(
        transcript=ProviderConfig(name="fallback", enabled=True),
        caption=ProviderConfig(name="fallback", enabled=True),
        embed=ProviderConfig(name="fallback", enabled=True),
        classifier=ProviderConfig(name="fallback", enabled=True)
    )
    
    normalizer = Normalizer(normalizer_config)
    normalized_unit = await normalizer.process(aggregate_dict)
    
    print(f"[TEST] NormalizedUnit.aggregate_id: {normalized_unit.aggregate_id}")
    print(f"[TEST] NormalizedUnit.id: {normalized_unit.id}")
    
    # КРИТИЧЕСКАЯ ПРОВЕРКА: ID агрегата должен сохраниться в normalized unit
    assert normalized_unit.aggregate_id == original_aggregate.id, \
        f"ID потерялся! Expected: {original_aggregate.id}, Got: {normalized_unit.aggregate_id}"
    
    # Шаг 7: Сохраняем в knowledge store и проверяем обратную связь
    knowledge_store = get_knowledge_store()
    unit_id = await knowledge_store.store(normalized_unit)
    
    # Шаг 8: Пытаемся найти исходный агрегат через normalized unit
    original_aggregate_via_unit = await knowledge_store.get_original_aggregate(unit_id)
    
    assert original_aggregate_via_unit is not None, \
        "Не удалось найти исходный агрегат через normalized unit"
    
    assert original_aggregate_via_unit.get("id") == original_aggregate.id, \
        f"ID в найденном агрегате не совпадает! Expected: {original_aggregate.id}, Got: {original_aggregate_via_unit.get('id')}"
    
    print("[TEST] ✅ Тест пройден: ID агрегата сохранился через весь пайплайн")


@pytest.mark.asyncio 
async def test_aggregate_id_loss_telegram_buffer_simulation():
    """
    Воспроизводит реальный сценарий отправки данных от telegram buffer.
    Показывает где именно теряется ID.
    """
    # Имитируем создание агрегата в telegram buffer
    telegram_aggregate = Aggregate(
        group_id="telegram-chat-456",
        entries=[],
        metadata={"connector_type": "telegram"}
    )
    
    original_id = telegram_aggregate.id
    print(f"[TELEGRAM_SIM] Original ID: {original_id}")
    
    # Имитируем отправку JSON на /ingest/aggregate endpoint
    # Telegram buffer использует model_dump(mode="json", exclude_none=True)
    json_payload = telegram_aggregate.model_dump(mode="json", exclude_none=True)
    print(f"[TELEGRAM_SIM] JSON payload ID: {json_payload.get('id')}")
    
    # Имитируем парсинг в FastAPI endpoint как AggregateInput
    try:
        received_aggregate = AggregateInput(**json_payload)
        print(f"[TELEGRAM_SIM] Received AggregateInput ID: {received_aggregate.id}")
        
        # Проверяем, сохранился ли ID
        if received_aggregate.id != original_id:
            print(f"[TELEGRAM_SIM] ❌ ID ПОТЕРЯЛСЯ! {original_id} → {received_aggregate.id}")
        else:
            print(f"[TELEGRAM_SIM] ✅ ID сохранился")
            
        # Проверяем что происходит при _convert_aggregate_for_normalization
        converted_dict = _convert_aggregate_for_normalization(received_aggregate)
        print(f"[TELEGRAM_SIM] After conversion ID: {converted_dict.get('id')}")
        
        if converted_dict.get('id') != original_id:
            print(f"[TELEGRAM_SIM] ❌ ID ПОТЕРЯЛСЯ НА КОНВЕРТАЦИИ! {original_id} → {converted_dict.get('id')}")
        
    except Exception as e:
        print(f"[TELEGRAM_SIM] ❌ Ошибка парсинга: {e}")


@pytest.mark.asyncio
async def test_aggregateinput_missing_id_behavior():
    """
    Тестирует поведение когда AggregateInput создается без ID.
    Проверяет fallback логику.
    """
    # Создаем AggregateInput без ID (как может прийти от некоторых коннекторов)
    aggregate_no_id = AggregateInput(
        group_id="test-group-no-id",
        entries=[],
        metadata={"test": "data"}
    )
    
    print(f"[NO_ID_TEST] AggregateInput без ID: {aggregate_no_id.id}")
    assert aggregate_no_id.id is None
    
    # Проверяем что происходит при конвертации
    converted_dict = _convert_aggregate_for_normalization(aggregate_no_id)
    print(f"[NO_ID_TEST] После конвертации ID: {converted_dict.get('id')}")
    
    # Fallback логика должна создать новый ID
    assert converted_dict.get('id') is not None
    assert len(converted_dict.get('id')) == 36  # UUID format
    
    # Сохраняем в JSONL
    await jsonl_backend.save_aggregate(aggregate_no_id)
    
    # При попытке загрузить по None ID должен быть сгенерированный ID
    # Это показывает проблему - мы не можем загрузить агрегат по его "реальному" ID


if __name__ == "__main__":
    # Запуск тестов напрямую для отладки
    asyncio.run(test_aggregate_id_consistency_full_pipeline())
    asyncio.run(test_aggregate_id_loss_telegram_buffer_simulation())
    asyncio.run(test_aggregateinput_missing_id_behavior()) 