"""
Фоновый воркер для автоматической нормализации необработанных агрегатов.
"""
import asyncio
import time
from typing import Dict, List, Optional, Set
from datetime import datetime

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings
from mindbank_poc.core.knowledge_store import get_knowledge_store
from mindbank_poc.core.knowledge_store.base import KnowledgeStore
from mindbank_poc.api.normalizers.manager import get_normalization_manager
from mindbank_poc.api.schemas import AggregateInput

logger = get_logger(__name__)


class NormalizationWorker:
    """
    Фоновый воркер для автоматической нормализации необработанных агрегатов.
    Использует существующую инфраструктуру NormalizationManager.
    """
    
    def __init__(self, knowledge_store: Optional[KnowledgeStore] = None):
        """
        Инициализация воркера нормализации.
        
        Args:
            knowledge_store: Хранилище знаний для получения обработанных единиц
        """
        self.knowledge_store = knowledge_store or get_knowledge_store()
        
        # Настройки из конфигурации
        self.enabled = getattr(settings.enrichment, 'normalization_enabled', True)
        self.min_pending = getattr(settings.enrichment, 'normalization_min_pending', 5)
        self.timeout_sec = getattr(settings.enrichment, 'normalization_timeout_sec', 1800)  # 30 мин
        self.check_interval = settings.enrichment.check_interval_seconds
        
        # Время последнего запуска
        self.last_run_timestamp = 0
        
        # Внутреннее состояние
        self._running = False
        self._task: Optional[asyncio.Task] = None
        
        logger.info(
            f"NormalizationWorker initialized: "
            f"enabled={self.enabled}, min_pending={self.min_pending}, "
            f"timeout={self.timeout_sec}s, check_interval={self.check_interval}s"
        )
    
    async def start(self):
        """Запускает фоновый воркер нормализации."""
        if not self.enabled:
            logger.info("NormalizationWorker is disabled in settings")
            return
            
        if self._running:
            logger.warning("NormalizationWorker is already running")
            return
        
        self._running = True
        self._task = asyncio.create_task(self._run_worker())
        logger.info("NormalizationWorker started")
    
    async def stop(self):
        """Останавливает фоновый воркер нормализации."""
        if not self._running:
            return
            
        self._running = False
        
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        logger.info("NormalizationWorker stopped")
    
    async def _run_worker(self):
        """Основной цикл воркера."""
        logger.info("NormalizationWorker main loop started")
        
        while self._running:
            try:
                await self._check_and_process()
                await asyncio.sleep(self.check_interval)
            except asyncio.CancelledError:
                logger.info("NormalizationWorker loop cancelled")
                break
            except Exception as e:
                logger.error(f"Error in NormalizationWorker loop: {e}", exc_info=True)
                await asyncio.sleep(self.check_interval)
    
    async def _check_and_process(self):
        """Проверяет наличие необработанных агрегатов и добавляет их в очередь."""
        try:
            # Получаем необработанные агрегаты
            unprocessed_aggregates = await self._get_unprocessed_aggregates()
            
            # Проверяем условия запуска
            if not self._should_run_normalization(len(unprocessed_aggregates)):
                logger.debug(f"Normalization skipped: {len(unprocessed_aggregates)} pending aggregates")
                return
            
            if not unprocessed_aggregates:
                self.last_run_timestamp = time.time()
                logger.debug("No unprocessed aggregates found")
                return
            
            logger.info(f"🚀 Starting normalization of {len(unprocessed_aggregates)} unprocessed aggregates")
            
            # Добавляем агрегаты в существующую очередь через NormalizationManager
            normalization_manager = await get_normalization_manager()
            
            processed_count = 0
            for aggregate in unprocessed_aggregates:
                try:
                    aggregate_dict = aggregate.model_dump()
                    success = await normalization_manager.add_aggregate(aggregate_dict)
                    if success:
                        processed_count += 1
                    else:
                        logger.warning(f"Failed to add aggregate {aggregate.id} to normalization queue")
                except Exception as e:
                    logger.error(f"Error adding aggregate {aggregate.id} to queue: {e}")
            
            self.last_run_timestamp = time.time()
            logger.info(f"✅ Added {processed_count}/{len(unprocessed_aggregates)} aggregates to normalization queue")
            
        except Exception as e:
            logger.error(f"Error in check_and_process: {e}", exc_info=True)
    
    async def _get_unprocessed_aggregates(self) -> List[AggregateInput]:
        """Находит агрегаты без соответствующих NormalizedUnit."""
        from mindbank_poc.api.backends import jsonl_backend  # Используем существующий backend
        
        # 1. Загружаем все агрегаты
        all_aggregates = await jsonl_backend.load_all_aggregates()
        
        # 2. Получаем все обработанные aggregate_id
        processed_ids = await self._get_processed_aggregate_ids()
        
        # 3. Фильтруем необработанные
        unprocessed = [agg for agg in all_aggregates if agg.id not in processed_ids]
        
        logger.debug(f"Found {len(unprocessed)} unprocessed aggregates out of {len(all_aggregates)} total")
        return unprocessed
    
    async def _get_processed_aggregate_ids(self) -> Set[str]:
        """Получает множество обработанных aggregate_id из NormalizedUnits."""
        all_units = await self.knowledge_store.list_all()
        processed_ids = {unit.aggregate_id for unit in all_units if unit.aggregate_id}
        logger.debug(f"Found {len(processed_ids)} processed aggregate IDs")
        return processed_ids
    
    def _should_run_normalization(self, pending_count: int) -> bool:
        """Определяет нужно ли запускать нормализацию."""
        current_time = time.time()
        time_since_last_run = current_time - self.last_run_timestamp
        
        min_count_reached = pending_count >= self.min_pending
        timeout_reached = time_since_last_run >= self.timeout_sec
        
        # Детальное логирование условий
        logger.debug(f"📊 Normalization conditions check:")
        logger.debug(f"  • Pending aggregates: {pending_count} (min required: {self.min_pending}) → {'✅' if min_count_reached else '❌'}")
        logger.debug(f"  • Time since last run: {time_since_last_run:.0f}s (timeout: {self.timeout_sec}s) → {'✅' if timeout_reached else '❌'}")
        logger.debug(f"  • Last run timestamp: {self.last_run_timestamp} ({datetime.fromtimestamp(self.last_run_timestamp) if self.last_run_timestamp > 0 else 'Never'})")
        
        should_run = min_count_reached or timeout_reached
        if should_run:
            logger.info(f"🚀 WILL RUN normalization: pending={pending_count}, timeout_reached={timeout_reached}")
        
        return should_run
    
    def get_stats(self) -> Dict[str, any]:
        """
        Возвращает статистику работы воркера нормализации.
        
        Returns:
            Словарь со статистикой
        """
        return {
            "running": self._running,
            "enabled": self.enabled,
            "min_pending": self.min_pending,
            "timeout_sec": self.timeout_sec,
            "check_interval": self.check_interval,
            "last_run_timestamp": self.last_run_timestamp
        } 