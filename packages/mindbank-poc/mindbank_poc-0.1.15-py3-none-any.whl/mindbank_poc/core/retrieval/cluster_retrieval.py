"""ClusterRetrievalService
~~~~~~~~~~~~~~~~~~~~~~~~~
Поиск TOP-K кластеров по косинусному сходству вектора запроса и центроида кластера.
Используется на шаге 1 схемы «кластер → сегменты».
"""
from __future__ import annotations

import math
import asyncio
from typing import List, Tuple, Optional, Dict, Any

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.enrichment.models import ClusterModel
from mindbank_poc.core.knowledge_store import get_knowledge_store
from mindbank_poc.core.knowledge_store.base import KnowledgeStore
from mindbank_poc.api.normalizers.config import load_config
from mindbank_poc.core.normalizer.normalizer import Normalizer

logger = get_logger(__name__)


def _cosine_similarity(v1: List[float], v2: List[float]) -> float:
    """Вычисляет косинусное сходство двух векторов."""
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


class ClusterRetrievalService:
    """Сервис поиска кластеров (этап 1)."""

    def __init__(self, knowledge_store: Optional[KnowledgeStore] = None):
        self.knowledge_store = knowledge_store or get_knowledge_store()
        # Получаем embed-provider через Normalizer (упрощённо, как в RetrievalService)
        normalizer = Normalizer(load_config())
        self.embed_provider = normalizer.embed_provider
        # lock для кеширования кластеров
        self._clusters_cache: Optional[List[ClusterModel]] = None
        self._cache_expires_at: Optional[float] = None

    async def _get_clusters(self, force_refresh: bool = False) -> List[ClusterModel]:
        """Загружает кластеры из хранилища (с простым кешем 5 мин)."""
        from datetime import datetime
        now_ts = datetime.utcnow().timestamp()
        if force_refresh or self._clusters_cache is None or (self._cache_expires_at and now_ts > self._cache_expires_at):
            self._clusters_cache = await self.knowledge_store.list_clusters()
            self._cache_expires_at = now_ts + 300  # 5 минут
            logger.info(f"ClusterRetrievalService: loaded {len(self._clusters_cache)} clusters from store")
        return self._clusters_cache or []

    async def search_clusters(
        self,
        query_text: str,
        k: int = 5,
        metadata_filters: Optional[Dict[str, Any]] = None,
    ) -> List[Tuple[ClusterModel, float]]:
        """Возвращает TOP-K кластеров по косинусному сходству.

        Args:
            query_text: текст запроса пользователя.
            k: сколько кластеров вернуть.
            metadata_filters: пока не используется, резерв.
        """
        if not query_text:
            logger.warning("search_clusters called with empty query_text")
            return []

        # Получаем эмбеддинг запроса
        try:
            query_vec = await self.embed_provider.embed_text(query_text)
        except Exception as e:
            logger.error(f"Error embedding query: {e}")
            return []

        clusters = await self._get_clusters()
        scored: List[Tuple[ClusterModel, float]] = []
        for cl in clusters:
            if not cl.centroid:
                continue  # пропускаем кластеры без вектора
            score = _cosine_similarity(query_vec, cl.centroid)
            scored.append((cl, score))

        # Сортировка по score убыв.
        scored.sort(key=lambda t: t[1], reverse=True)
        return scored[:k]


# --- singleton helper ---
_cluster_service_instance: Optional[ClusterRetrievalService] = None
_cluster_lock = asyncio.Lock()


async def get_cluster_retrieval_service() -> ClusterRetrievalService:
    global _cluster_service_instance
    if _cluster_service_instance is None:
        async with _cluster_lock:
            if _cluster_service_instance is None:
                _cluster_service_instance = ClusterRetrievalService()
    return _cluster_service_instance 