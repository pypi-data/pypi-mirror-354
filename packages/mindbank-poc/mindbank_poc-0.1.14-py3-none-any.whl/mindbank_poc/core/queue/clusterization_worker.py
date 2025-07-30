"""
Фоновый воркер для автоматической кластеризации сегментов.
"""
import asyncio
from typing import Dict, Optional
from datetime import datetime

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings
from mindbank_poc.core.enrichment.clusterization_service import ClusterizationService
from mindbank_poc.core.knowledge_store import get_knowledge_store
from mindbank_poc.core.knowledge_store.base import KnowledgeStore
from mindbank_poc.core.providers.clustering import register_clustering_providers

logger = get_logger(__name__)


class ClusterizationWorker:
    """
    Фоновый воркер, который периодически проверяет наличие некластеризованных
    сегментов и запускает процесс кластеризации.
    """
    
    def __init__(
        self, 
        knowledge_store: Optional[KnowledgeStore] = None
    ):
        """
        Инициализация воркера кластеризации.
        
        Args:
            knowledge_store: Хранилище знаний для получения сегментов и сохранения результатов кластеризации
        """
        self.knowledge_store = knowledge_store or get_knowledge_store()
        
        self.clusterization_service = ClusterizationService(
            knowledge_store=self.knowledge_store
        )
        
        # Настройки из конфигурации
        self.enabled = getattr(settings.enrichment, 'enabled', True)
        self.min_pending = getattr(settings.enrichment, 'cluster_min_pending', 500)
        self.timeout_sec = getattr(settings.enrichment, 'cluster_timeout_sec', 3600)
        self.check_interval = getattr(settings.enrichment, 'check_interval_seconds', 60)
        
        # Внутреннее состояние
        self._running = False
        self._task: Optional[asyncio.Task] = None
        
        logger.info(
            f"ClusterizationWorker initialized: "
            f"enabled={self.enabled}, min_pending={self.min_pending}, "
            f"timeout={self.timeout_sec}s, check_interval={self.check_interval}s"
        )
    
    async def start(self):
        """Запускает фоновый воркер кластеризации."""
        if not self.enabled:
            logger.info("ClusterizationWorker is disabled in settings")
            return
            
        if self._running:
            logger.warning("ClusterizationWorker is already running")
            return
        
        # Регистрируем провайдеры кластеризации
        register_clustering_providers()
        
        self._running = True
        self._task = asyncio.create_task(self._run_worker())
        logger.info("ClusterizationWorker started")
    
    async def stop(self):
        """Останавливает фоновый воркер кластеризации."""
        if not self._running:
            return
            
        self._running = False
        
        if self._task:
            self._task.cancel()
            try:
                await self._task
            except asyncio.CancelledError:
                pass
        
        logger.info("ClusterizationWorker stopped")
    
    async def _run_worker(self):
        """Основной цикл воркера кластеризации."""
        logger.info("ClusterizationWorker main loop started")
        
        while self._running:
            try:
                # Проверяем и запускаем кластеризацию если нужно
                await self._check_and_cluster()
                
                # Ждем перед следующей проверкой
                await asyncio.sleep(self.check_interval)
                
            except asyncio.CancelledError:
                logger.info("ClusterizationWorker loop cancelled")
                break
            except Exception as e:
                logger.error(f"Error in ClusterizationWorker loop: {e}", exc_info=True)
                # Продолжаем работу после ошибки
                await asyncio.sleep(self.check_interval)
    
    async def _check_and_cluster(self):
        """Проверяет условия и запускает кластеризацию если необходимо."""
        try:
            # Запускаем кластеризацию через сервис
            result = await self.clusterization_service.run_clustering_if_needed()
            
            # Логируем результат
            if result.get("action") == "completed":
                clusters_created = result.get("clusters_created", 0)
                segments_updated = result.get("segments_updated", 0)
                
                if clusters_created > 0:
                    logger.info(
                        f"Clustering completed: {clusters_created} clusters created, "
                        f"{segments_updated} segments updated"
                    )
                    
                    # Показываем информацию о кластерах
                    cluster_info = result.get("cluster_info", {})
                    for cluster_id, info in cluster_info.items():
                        logger.info(
                            f"  Cluster {cluster_id}: '{info.get('title', '')}' "
                            f"({info.get('size', 0)} segments, "
                            f"keywords: {', '.join(info.get('keywords', [])[:3])})"
                        )
                else:
                    logger.debug("Clustering completed but no clusters were created (disabled or failed)")
                    
            elif result.get("action") == "skipped":
                reason = result.get("reason", "unknown")
                logger.debug(f"Clustering skipped: {reason}")
                
            elif result.get("action") == "failed":
                reason = result.get("reason", "unknown error")
                logger.error(f"Clustering failed: {reason}")
                
        except Exception as e:
            logger.error(f"Error in check_and_cluster: {e}", exc_info=True)
    
    def get_stats(self) -> Dict[str, any]:
        """
        Возвращает статистику работы воркера кластеризации.
        
        Returns:
            Словарь со статистикой
        """
        return {
            "running": self._running,
            "enabled": self.enabled,
            "min_pending": self.min_pending,
            "timeout_sec": self.timeout_sec,
            "check_interval": self.check_interval,
            "service_stats": {
                "last_run_timestamp": self.clusterization_service.last_run_timestamp
            }
        } 