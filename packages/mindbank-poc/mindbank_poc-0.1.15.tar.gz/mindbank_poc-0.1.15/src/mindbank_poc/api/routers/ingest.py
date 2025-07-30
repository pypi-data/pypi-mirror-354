import asyncio
from fastapi import APIRouter, HTTPException, status, Depends
from typing import Optional

from mindbank_poc.api.schemas import RawEntryInput, AggregateInput
from mindbank_poc.api.backends import jsonl_backend
from mindbank_poc.core.common.types import RawEntry, Aggregate, ContentType
from mindbank_poc.core.buffer.memory_buffer import InMemoryBuffer, BufferConfig
from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings
from mindbank_poc.core.services.archetype_service import get_archetype_service, ArchetypeService

router = APIRouter(
    prefix="/ingest",
    tags=["Ingest"],
)

# Create a global buffer instance
# In a real application, this would be managed by dependency injection
# or some other method to control its lifecycle
_buffer: Optional[InMemoryBuffer] = None

logger = get_logger(__name__)

async def get_buffer():
    """Returns the global buffer instance, initializing it if needed."""
    global _buffer
    
    if _buffer is None:
        # Создаем буфер с настройками из конфигурации
        _buffer = InMemoryBuffer(
            config=BufferConfig(
                timeout_seconds=settings.api.buffer_timeout_seconds,
                max_entries_per_group=settings.api.buffer_max_entries_per_group,
                check_interval_seconds=settings.api.buffer_check_interval_seconds,
            ),
            on_aggregate_callback=_process_aggregate
        )
        await _buffer.start()
        
    return _buffer

async def _process_aggregate(aggregate: Aggregate):
    """Callback to process an aggregate created by the buffer."""
    # Convert Aggregate to AggregateInput (for jsonl_backend)
    # This is a bit of a hack, in a real application we'd refactor the backend
    # to accept Aggregate directly
    aggregate_input = AggregateInput(
        id=aggregate.id,
        group_id=aggregate.group_id,
        entries=[
            RawEntryInput(
                collector_id=entry.collector_id,
                group_id=entry.group_id,
                entry_id=entry.entry_id,
                type=entry.type,
                archetype=entry.archetype,
                payload=entry.payload,
                metadata=entry.metadata,
                timestamp=entry.timestamp,
            )
            for entry in aggregate.entries
        ],
        archetype=aggregate.archetype,
        metadata=aggregate.metadata,
        content_start_time=aggregate.content_start_time,
        content_end_time=aggregate.content_end_time,
        entries_metadata=aggregate.entries_metadata,
    )
    
    # Если у агрегата есть архетип, регистрируем его использование
    if aggregate.archetype:
        archetype_service = get_archetype_service()
        archetype_service.register_usage(aggregate.archetype)
    
    try:
        # Сохраняем агрегат (нормализация теперь происходит через NormalizationWorker)
        await jsonl_backend.save_aggregate(aggregate_input)
        logger.info(f"✅ Aggregate {aggregate.id} saved, will be processed by NormalizationWorker")
    except Exception as e:
        # Log the error but don't raise, to avoid crashing the buffer
        logger.error(f"Error saving aggregate from buffer: {e}")



@router.post("/entry", status_code=status.HTTP_202_ACCEPTED)
async def submit_raw_entry(entry: RawEntryInput, buffer: InMemoryBuffer = Depends(get_buffer)):
    """
    Receives a single raw entry, adds it to the buffer, and eventually
    saves it using the configured backend.
    
    The buffer will flush entries based on timeout, max entries, or the 'is_last' flag
    in the entry's metadata.
    """
    try:
        # Convert RawEntryInput to RawEntry and add to buffer
        raw_entry = RawEntry(
            collector_id=entry.collector_id,
            group_id=entry.group_id,
            entry_id=entry.entry_id,
            type=entry.type,
            archetype=entry.archetype,
            payload=entry.payload,
            metadata=entry.metadata or {},
            timestamp=entry.timestamp,
        )
        
        # Also save the raw entry directly to the backend
        await jsonl_backend.save_raw_entry(entry)
        
        # Add to buffer (will be aggregated based on rules)
        await buffer.add_entry(raw_entry)
        
        return {"message": "Raw entry accepted"}
    except Exception as e:
        # Basic error handling
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to process raw entry: {e}"
        )

@router.post("/aggregate", status_code=status.HTTP_202_ACCEPTED)
async def submit_aggregate(
    aggregate: AggregateInput, 
    archetype_service: ArchetypeService = Depends(get_archetype_service)
):
    """
    Receives an aggregate and saves it using the configured backend.
    
    This endpoint bypasses the buffer and directly saves the aggregate.
    The aggregate will be processed by NormalizationWorker in the background.
    """
    try:
        # Если у агрегата есть архетип, регистрируем его использование
        if aggregate.archetype:
            archetype_service.register_usage(aggregate.archetype)
        
        # Сохраняем агрегат (нормализация теперь происходит через NormalizationWorker)
        await jsonl_backend.save_aggregate(aggregate)
        logger.info(f"✅ Aggregate {aggregate.id} saved, will be processed by NormalizationWorker")
        
        return {"message": "Aggregate accepted and queued for processing"}
    except Exception as e:
        # Basic error handling
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to save aggregate: {e}"
        )

# Optional: Add lifecycle event handlers to FastAPI

@router.on_event("startup")
async def startup_event():
    """Initialize the buffer when the API starts."""
    await get_buffer()

@router.on_event("shutdown")
async def shutdown_event():
    """Stop the buffer when the API is shutting down."""
    global _buffer
    if _buffer:
        await _buffer.stop()
        _buffer = None 