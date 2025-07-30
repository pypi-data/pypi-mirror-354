"""SegmentRetrievalService
~~~~~~~~~~~~~~~~~~~~~~~~
Поиск TOP-M сегментов в рамках выбранных кластеров.
Использует косинусное сходство векторов сегментов и запроса.
"""
from __future__ import annotations

import math
import asyncio
from typing import List, Tuple, Optional, Dict, Any, Set

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.enrichment.models import SegmentModel
from mindbank_poc.core.knowledge_store import get_knowledge_store
from mindbank_poc.core.knowledge_store.base import KnowledgeStore
from mindbank_poc.api.normalizers.config import load_config
from mindbank_poc.core.normalizer.normalizer import Normalizer

logger = get_logger(__name__)


def _cosine_similarity(v1: List[float], v2: List[float]) -> float:
    if not v1 or not v2 or len(v1) != len(v2):
        return 0.0
    dot = sum(a * b for a, b in zip(v1, v2))
    norm1 = math.sqrt(sum(a * a for a in v1))
    norm2 = math.sqrt(sum(b * b for b in v2))
    if norm1 == 0 or norm2 == 0:
        return 0.0
    return dot / (norm1 * norm2)


class SegmentRetrievalService:
    """Сервис поиска сегментов в рамках выбранных кластеров."""

    def __init__(self, knowledge_store: Optional[KnowledgeStore] = None):
        self.knowledge_store = knowledge_store or get_knowledge_store()
        normalizer = Normalizer(load_config())
        self.embed_provider = normalizer.embed_provider
        # Простой кеш сегментов по кластеру
        self._cluster_segment_cache: Dict[str, List[SegmentModel]] = {}

    async def _get_segments_for_clusters(self, cluster_ids: Set[str]) -> List[SegmentModel]:
        segments: List[SegmentModel] = []
        for cid in cluster_ids:
            if cid in self._cluster_segment_cache:
                segments.extend(self._cluster_segment_cache[cid])
                continue
            segs = await self.knowledge_store.list_segments_by_cluster(cid)
            self._cluster_segment_cache[cid] = segs
            segments.extend(segs)
        return segments

    async def search_segments(
        self,
        query_text: str,
        cluster_ids: List[str],
        m: int = 20,
    ) -> List[Tuple[SegmentModel, float]]:
        """Возвращает TOP-M сегментов в рамках cluster_ids."""
        if not query_text or not cluster_ids:
            logger.warning("search_segments called with empty params")
            return []

        try:
            query_vec = await self.embed_provider.embed_text(query_text)
        except Exception as e:
            logger.error(f"Error embedding query in SegmentRetrieval: {e}")
            return []

        cluster_set = set(cluster_ids)
        segments = await self._get_segments_for_clusters(cluster_set)
        scored: List[Tuple[SegmentModel, float]] = []
        for seg in segments:
            if not seg.vector_repr:
                continue
            score = _cosine_similarity(query_vec, seg.vector_repr)
            scored.append((seg, score))

        scored.sort(key=lambda t: t[1], reverse=True)
        return scored[:m]


# singleton helper
_segment_service_instance: Optional[SegmentRetrievalService] = None
_segment_lock = asyncio.Lock()


async def get_segment_retrieval_service() -> SegmentRetrievalService:
    global _segment_service_instance
    if _segment_service_instance is None:
        async with _segment_lock:
            if _segment_service_instance is None:
                _segment_service_instance = SegmentRetrievalService()
    return _segment_service_instance 