"""
Фоновый воркер для автоматической сегментации нормализованных юнитов.
"""
import asyncio
from typing import Dict, List, Set, Optional
from datetime import datetime
import time

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings
from mindbank_poc.core.enrichment import SegmentationService
from mindbank_poc.core.knowledge_store import get_knowledge_store
from mindbank_poc.core.knowledge_store.base import KnowledgeStore
from mindbank_poc.core.providers.segmentation import register_segmentation_providers

logger = get_logger(__name__)


class SegmentationWorker:
    """
    Фоновый воркер, который периодически проверяет наличие несегментированных
    нормализованных юнитов и запускает процесс сегментации.
    """
    
    def __init__(
        self, 
        knowledge_store: Optional[KnowledgeStore] = None
    ):
        """
        Инициализация воркера сегментации.
        
        Args:
            knowledge_store: Хранилище знаний для получения нормализованных единиц и сохранения сегментов
        """
        self.knowledge_store = knowledge_store or get_knowledge_store()
        
        self.segmentation_service = SegmentationService(
            knowledge_store=self.knowledge_store
        )
        
        # Настройки из конфигурации
        self.enabled = settings.enrichment.enabled
        self.threshold = settings.enrichment.segmentation_threshold
        self.segmentation_timeout_sec = settings.enrichment.segmentation_timeout_sec
        self.check_interval = settings.enrichment.check_interval_seconds
        self.batch_size = settings.enrichment.batch_size
        
        # Внутреннее состояние
        self._running = False
        self._task: Optional[asyncio.Task] = None
        self._processed_units: Set[str] = set()  # Отслеживаем обработанные юниты
        self._group_last_change: Dict[str, float] = {}  # Время последнего изменения каждой группы
        self._group_unit_counts: Dict[str, int] = {}  # Количество юнитов в каждой группе для отслеживания изменений
        
        logger.info(
            f"SegmentationWorker initialized: "
            f"enabled={self.enabled}, threshold={self.threshold}, "
            f"timeout={self.segmentation_timeout_sec}s, "
            f"check_interval={self.check_interval}s"
        )
    
    async def start(self):
        """Запускает фоновый воркер."""
        if not self.enabled:
            logger.info("SegmentationWorker is disabled in settings")
            return
            
        if self._running:
            logger.warning("SegmentationWorker is already running")
            return
        
        # Регистрируем провайдеры сегментации
        register_segmentation_providers()
        
        # Регистрируем провайдеры кластеризации
        from mindbank_poc.core.providers.clustering import register_clustering_providers
        register_clustering_providers()
        
        self._running = True
        self._task = asyncio.create_task(self._run_worker())
        logger.info("SegmentationWorker started")
    
    async def stop(self):
        """Останавливает фоновый воркер."""
        if not self._running:
            return
            
        self._running = False
        
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        logger.info("SegmentationWorker stopped")
    
    async def _run_worker(self):
        """Основной цикл воркера."""
        logger.info("SegmentationWorker main loop started")
        
        while self._running:
            try:
                # Проверяем и обрабатываем несегментированные юниты
                await self._check_and_process()
                
                # Ждем перед следующей проверкой
                await asyncio.sleep(self.check_interval)
                
            except asyncio.CancelledError:
                logger.info("SegmentationWorker loop cancelled")
                break
            except Exception as e:
                logger.error(f"Error in SegmentationWorker loop: {e}", exc_info=True)
                # Продолжаем работу после ошибки
                await asyncio.sleep(self.check_interval)
    
    async def _check_and_process(self):
        """Проверяет наличие групп с новыми юнитами и запускает сегментацию."""
        try:
            # Новый способ: ищем группы с новыми юнитами после последней сегментации
            if hasattr(self.knowledge_store, 'get_groups_with_new_units_for_segmentation'):
                groups_to_process = await self.knowledge_store.get_groups_with_new_units_for_segmentation(self.threshold)
            else:
                # Fallback: старая логика
                groups_to_process = []
                if hasattr(self.knowledge_store, 'list_unprocessed_groups'):
                    groups_to_process = await self.knowledge_store.list_unprocessed_groups(self.threshold)
                else:
                    groups_to_process = await self._get_unprocessed_groups_fallback()

            if not groups_to_process:
                logger.debug("No groups qualifying for segmentation (new units)")
                return

            logger.info(f"📋 Processing {len(groups_to_process)} groups with new units for segmentation")

            for group_id in groups_to_process:
                try:
                    await self._process_group(group_id)
                except Exception as e:
                    logger.error(f"Error processing group {group_id}: {e}", exc_info=True)
        except Exception as e:
            logger.error(f"Error in check_and_process: {e}", exc_info=True)
    
    async def _process_group(self, group_id: str):
        """
        Обрабатывает группу для сегментации и обновляет метаинформацию после успешной сегментации.
        """
        logger.info(f"Processing group {group_id} for segmentation")
        try:
            # Получаем все юниты группы
            if hasattr(self.knowledge_store, 'list_by_group'):
                units = await self.knowledge_store.list_by_group(group_id)
            else:
                all_units = await self.knowledge_store.list_all()
                units = [u for u in all_units if u.group_id == group_id]

            if not units:
                logger.warning(f"No units found for group {group_id}")
                return

            # Сортируем по дате
            units_sorted = sorted(units, key=lambda u: u.normalized_at or getattr(u, 'stored_at', ""))
            last_unit = units_sorted[-1]

            # Запускаем сегментацию
            segments = await self.segmentation_service.segment_group(group_id)

            if segments:
                logger.info(f"Created {len(segments)} segments for group {group_id}")
                # Обновляем метаинформацию о сегментации группы
                if hasattr(self.knowledge_store, 'set_group_segmentation_meta'):
                    await self.knowledge_store.set_group_segmentation_meta(
                        group_id,
                        last_segmented_at=datetime.utcnow().isoformat(),
                        last_segmented_unit_id=last_unit.id
                    )
            else:
                logger.warning(f"No segments created for group {group_id}")
        except Exception as e:
            logger.error(f"Error processing group {group_id}: {e}", exc_info=True)
            raise
    
    def get_stats(self) -> Dict[str, any]:
        """
        Возвращает статистику работы воркера.
        
        Returns:
            Словарь со статистикой
        """
        return {
            "running": self._running,
            "enabled": self.enabled,
            "threshold": self.threshold,
            "timeout": self.segmentation_timeout_sec,
            "check_interval": self.check_interval,
            "processed_units_count": len(self._processed_units),
            "batch_size": self.batch_size
        } 