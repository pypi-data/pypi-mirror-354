"""
Сервис для кластеризации сегментов знаний.
"""
import time
from typing import List, Optional, Dict, Any
from datetime import datetime

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings
from mindbank_poc.core.knowledge_store.base import KnowledgeStore
from mindbank_poc.core.enrichment.models import SegmentModel, ClusterModel
from mindbank_poc.core.services.provider_service import get_provider_service
from mindbank_poc.core.providers.selector import ProviderSelector
from mindbank_poc.core.common.types import ProviderType

logger = get_logger(__name__)


class ClusterizationService:
    """Сервис для выполнения кластеризации сегментов знаний."""
    
    def __init__(self, knowledge_store: KnowledgeStore):
        """
        Инициализация сервиса кластеризации.
        
        Args:
            knowledge_store: Хранилище знаний для работы с сегментами
        """
        self.knowledge_store = knowledge_store
        self.provider_service = get_provider_service()
        
        # Параметры кластеризации из настроек
        self.cluster_min_pending = getattr(settings.enrichment, 'cluster_min_pending', 500)
        self.cluster_timeout_sec = getattr(settings.enrichment, 'cluster_timeout_sec', 3600)
        
        # Время последнего запуска кластеризации
        self.last_run_timestamp = 0
        
        logger.info(f"ClusterizationService initialized with min_pending={self.cluster_min_pending}, "
                   f"timeout={self.cluster_timeout_sec}s")
    
    async def get_unclustered_segments(self) -> List[SegmentModel]:
        """
        Получает список сегментов, которые еще не были кластеризованы.
        
        Returns:
            Список некластеризованных сегментов
        """
        try:
            # Получаем все сегменты
            all_segments = []
            
            # Если есть метод для получения всех сегментов
            if hasattr(self.knowledge_store, 'list_all_segments'):
                all_segments = await self.knowledge_store.list_all_segments()
                logger.info(f"📊 Retrieved {len(all_segments)} total segments via list_all_segments()")
            else:
                # Fallback: получаем через группы
                group_ids = await self._get_all_group_ids()
                logger.info(f"📊 Found {len(group_ids)} groups, getting segments...")
                for group_id in group_ids:
                    segments = await self.knowledge_store.list_segments_by_group(group_id)
                    all_segments.extend(segments)
                    logger.debug(f"  Group {group_id}: {len(segments)} segments")
                logger.info(f"📊 Retrieved {len(all_segments)} total segments via groups")
            
            # Получаем все кластеры и собираем ID кластеризованных сегментов
            clustered_segment_ids = set()
            try:
                all_clusters = await self.knowledge_store.list_clusters()
                logger.info(f"📊 Found {len(all_clusters)} existing clusters")
                
                for cluster in all_clusters:
                    clustered_segment_ids.update(cluster.segment_ids)
                    logger.debug(f"  Cluster {cluster.id[:8]}... contains {len(cluster.segment_ids)} segments")
                
                logger.info(f"📊 Total clustered segment IDs: {len(clustered_segment_ids)}")
            except Exception as e:
                logger.warning(f"⚠️ Could not retrieve clusters (maybe none exist yet): {e}")
                clustered_segment_ids = set()
            
            # Фильтруем некластеризованные сегменты
            unclustered = []
            clustered_count = 0
            
            for segment in all_segments:
                if segment.id not in clustered_segment_ids:
                    unclustered.append(segment)
                    logger.debug(f"  Unclustered: {segment.id[:8]}...")
                else:
                    clustered_count += 1
                    logger.debug(f"  Clustered: {segment.id[:8]}...")
            
            logger.info(f"📊 Segments status: {len(unclustered)} unclustered, {clustered_count} already clustered")
            return unclustered
            
        except Exception as e:
            logger.error(f"❌ Error getting unclustered segments: {e}")
            return []
    
    async def _get_all_group_ids(self) -> List[str]:
        """
        Получает все уникальные ID групп из хранилища.
        
        Returns:
            Список уникальных group_id
        """
        try:
            if hasattr(self.knowledge_store, 'list_group_ids'):
                return list(await self.knowledge_store.list_group_ids())
            
            # Fallback: получаем через все юниты
            if hasattr(self.knowledge_store, 'list_all'):
                all_units = await self.knowledge_store.list_all()
                group_ids = set()
                for unit in all_units:
                    if unit.group_id:
                        group_ids.add(unit.group_id)
                return list(group_ids)
            
            return []
        except Exception as e:
            logger.error(f"Error getting group IDs: {e}")
            return []
    
    def should_run_clustering(self, pending_count: int) -> bool:
        """
        Определяет, нужно ли запускать кластеризацию сейчас.
        
        Args:
            pending_count: Количество некластеризованных сегментов
            
        Returns:
            True если нужно запустить кластеризацию
        """
        current_time = time.time()
        time_since_last_run = current_time - self.last_run_timestamp
        
        # Проверяем условия запуска
        min_count_reached = pending_count >= self.cluster_min_pending
        timeout_reached = time_since_last_run >= self.cluster_timeout_sec
        
        # Детальное логирование условий
        logger.info(f"📊 Clustering conditions check:")
        logger.info(f"  • Pending segments: {pending_count} (min required: {self.cluster_min_pending}) → {'✅' if min_count_reached else '❌'}")
        logger.info(f"  • Time since last run: {time_since_last_run:.0f}s (timeout: {self.cluster_timeout_sec}s) → {'✅' if timeout_reached else '❌'}")
        logger.info(f"  • Last run timestamp: {self.last_run_timestamp} ({datetime.fromtimestamp(self.last_run_timestamp) if self.last_run_timestamp > 0 else 'Never'})")
        
        should_run = min_count_reached or timeout_reached
        logger.info(f"  • Result: {'🚀 WILL RUN clustering' if should_run else '⏸️ WILL SKIP clustering'}")
        
        return should_run
    
    async def _select_clustering_provider(self, segments: List[SegmentModel]) -> Optional[Any]:
        """
        Выбирает провайдер кластеризации на основе контекста сегментов.
        
        Args:
            segments: Список сегментов для кластеризации
            
        Returns:
            Экземпляр провайдера кластеризации или None
        """
        try:
            # Получаем все провайдеры кластеризации
            providers = self.provider_service.get_all_providers()
            clustering_providers = [
                p for p in providers 
                if p.provider_type == ProviderType.CLUSTERING
            ]
            
            if not clustering_providers:
                logger.warning("No clustering providers found in system")
                return self._create_fallback_provider()
            
            # Используем метаданные первого сегмента для контекста
            first_segment = segments[0] if segments else None
            metadata = {}
            archetype = "generic"
            source = "unknown"
            
            if first_segment and first_segment.metadata:
                metadata = first_segment.metadata.get("source_metadata", {})
                source = metadata.get("source", "unknown")
                # TODO: можно добавить логику определения архетипа на основе сегментов
            
            # Выбираем провайдер через селектор
            provider_model = ProviderSelector.select_provider(
                providers=[p.dict(exclude={"instance"}) for p in clustering_providers],
                provider_type=ProviderType.CLUSTERING.value,
                archetype=archetype,
                source=source,
                metadata=metadata
            )
            
            if not provider_model:
                logger.warning("No clustering provider selected by ProviderSelector, using fallback")
                return self._create_fallback_provider()
            
            # Создаем экземпляр провайдера
            provider_class = self._get_provider_class(provider_model.get('id'))
            if not provider_class:
                logger.error(f"Provider class not found for {provider_model.get('id')}, using fallback")
                return self._create_fallback_provider()
            
            try:
                provider_instance = provider_class(provider_model.get('current_config', {}))
                logger.info(f"Successfully created clustering provider: {provider_model.get('id')}")
                return provider_instance
            except Exception as e:
                logger.error(f"Failed to create provider instance for {provider_model.get('id')}: {e}, using fallback")
                return self._create_fallback_provider()
                
        except Exception as e:
            logger.error(f"Error in clustering provider selection: {e}, using fallback provider")
            return self._create_fallback_provider()
    
    def _get_provider_class(self, provider_id: str):
        """
        Получает класс провайдера кластеризации по его ID.
        
        Args:
            provider_id: ID провайдера
            
        Returns:
            Класс провайдера или None
        """
        try:
            from mindbank_poc.core.providers.clustering import (
                KMeansClusterProvider,
                MockClusterProvider
            )
            
            provider_classes = {
                "kmeans-clustering": KMeansClusterProvider,
                "mock-clustering": MockClusterProvider
            }
            
            return provider_classes.get(provider_id, MockClusterProvider)
        except ImportError as e:
            logger.error(f"Failed to import clustering providers: {e}")
            return None
    
    def _create_fallback_provider(self) -> Optional[Any]:
        """
        Создает fallback провайдер (Mock) в случае недоступности основных провайдеров.
        
        Returns:
            Экземпляр mock провайдера или None
        """
        try:
            from mindbank_poc.core.providers.clustering import MockClusterProvider
            logger.info("Using MockClusterProvider as fallback")
            return MockClusterProvider({})
        except Exception as e:
            logger.error(f"Failed to create fallback clustering provider: {e}")
            return None
    
    async def run_clustering_if_needed(self) -> Dict[str, Any]:
        """
        Запускает кластеризацию если выполнены условия.
        
        Returns:
            Словарь с результатами кластеризации
        """
        try:
            # Получаем некластеризованные сегменты
            unclustered_segments = await self.get_unclustered_segments()
            
            # Проверяем, нужно ли запускать кластеризацию
            if not self.should_run_clustering(len(unclustered_segments)):
                return {
                    "action": "skipped",
                    "reason": f"Not enough segments ({len(unclustered_segments)}) or timeout not reached",
                    "unclustered_count": len(unclustered_segments)
                }
            
            if not unclustered_segments:
                self.last_run_timestamp = time.time()
                return {
                    "action": "skipped",
                    "reason": "No unclustered segments found",
                    "unclustered_count": 0
                }
            
            logger.info(f"Starting clustering of {len(unclustered_segments)} segments")
            
            # Выбираем провайдер кластеризации
            provider = await self._select_clustering_provider(unclustered_segments)
            if not provider:
                return {
                    "action": "failed",
                    "reason": "No clustering provider available",
                    "unclustered_count": len(unclustered_segments)
                }
            
            # Сохраняем информацию о провайдере для использования в metadata
            provider_class_name = provider.__class__.__name__
            self._current_provider_name = provider_class_name
            self._current_provider_type = "clustering"
            logger.info(f"🔧 Using clustering provider: {provider_class_name}")
            
            # Выполняем кластеризацию
            cluster_results = await provider.cluster(unclustered_segments)
            
            if not cluster_results:
                logger.info("Clustering provider returned empty results (clustering disabled or failed)")
                self.last_run_timestamp = time.time()
                return {
                    "action": "completed",
                    "reason": "Clustering disabled or returned empty results",
                    "unclustered_count": len(unclustered_segments),
                    "clusters_created": 0
                }
            
            # Создаем кластеры как отдельные сущности
            created_count = await self._update_segments_with_clusters(cluster_results)
            
            # Проверяем, что кластеры действительно сохранились
            try:
                stored_clusters = await self.knowledge_store.list_clusters()
                logger.info(f"🔍 Verification: Found {len(stored_clusters)} total clusters in storage")
                
                # Проверяем свежесозданные кластеры
                recent_clusters = [
                    c for c in stored_clusters 
                    if c.metadata.get('clustering_provider') == self._current_provider_name
                ]
                logger.info(f"📊 Of which {len(recent_clusters)} were created by {self._current_provider_name}")
                
            except Exception as e:
                logger.warning(f"⚠️ Could not verify cluster storage: {e}")
            
            # Обновляем время последнего запуска
            self.last_run_timestamp = time.time()
            
            logger.info(f"🎯 Clustering completed successfully: {len(cluster_results)} clusters created, "
                       f"covering {sum(len(info.get('segment_ids', [])) for info in cluster_results.values())} segments")
            
            return {
                "action": "completed",
                "reason": "Clustering completed successfully",
                "unclustered_count": len(unclustered_segments),
                "clusters_created": len(cluster_results),
                "clusters_stored": created_count,
                "cluster_info": {
                    cluster_id: {
                        "title": info.get("title", ""),
                        "size": len(info.get("segment_ids", [])),
                        "keywords": info.get("keywords", [])[:5]  # Первые 5 ключевых слов
                    }
                    for cluster_id, info in cluster_results.items()
                }
            }
            
        except Exception as e:
            logger.error(f"Error during clustering: {e}", exc_info=True)
            return {
                "action": "failed",
                "reason": f"Error during clustering: {str(e)}",
                "unclustered_count": len(unclustered_segments) if 'unclustered_segments' in locals() else 0
            }
    
    async def _update_segments_with_clusters(self, cluster_results: Dict[int, Dict[str, Any]]) -> int:
        """
        Создает кластеры как отдельные сущности на основе результатов кластеризации.
        
        Args:
            cluster_results: Результаты кластеризации
            
        Returns:
            Количество созданных кластеров
        """
        created_count = 0
        
        try:
            for cluster_id, cluster_info in cluster_results.items():
                try:
                    # Получаем информацию о провайдере (если доступна)
                    provider_name = getattr(self, '_current_provider_name', 'unknown')
                    provider_type = getattr(self, '_current_provider_type', 'clustering')
                    
                    # Создаем объект ClusterModel с правильными данными
                    cluster = ClusterModel(
                        title=cluster_info.get("title", f"Кластер {cluster_id}"),
                        summary=cluster_info.get("summary", ""),
                        keywords=cluster_info.get("keywords", []),
                        segment_ids=cluster_info.get("segment_ids", []),
                        centroid=cluster_info.get("centroid"),
                        cluster_size=cluster_info.get("size", len(cluster_info.get("segment_ids", []))),  # Используем size если есть
                        metadata={
                            "clustering_provider": provider_name,
                            "clustering_algorithm": f"{provider_type}_algorithm",
                            "cluster_original_id": cluster_id,  # Сохраняем оригинальный ID из провайдера
                            "cluster_stats": {
                                "original_size": cluster_info.get("size", 0),
                                "has_centroid": cluster_info.get("centroid") is not None,
                                "keywords_count": len(cluster_info.get("keywords", []))
                            }
                        }
                    )
                    
                    logger.info(f"🔧 Creating cluster {cluster_id} with {cluster.cluster_size} segments")
                    logger.debug(f"  Title: {cluster.title}")
                    logger.debug(f"  Keywords: {cluster.keywords[:3]}...")
                    logger.debug(f"  Provider: {provider_name}")
                    
                    # Сохраняем кластер в хранилище
                    await self.knowledge_store.store_cluster(cluster)
                    created_count += 1
                    
                    logger.info(f"✅ Successfully created and stored cluster {cluster.id} with {cluster.cluster_size} segments")
                    
                except Exception as e:
                    logger.error(f"❌ Error creating cluster {cluster_id}: {e}", exc_info=True)
                    continue
            
            logger.info(f"🎯 Created {created_count} clusters successfully out of {len(cluster_results)} total")
            return created_count
            
        except Exception as e:
            logger.error(f"❌ Error creating clusters from results: {e}", exc_info=True)
            return created_count 