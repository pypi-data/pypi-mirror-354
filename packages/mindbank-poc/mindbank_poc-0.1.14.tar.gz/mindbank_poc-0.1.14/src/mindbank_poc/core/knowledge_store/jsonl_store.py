"""
Реализация хранилища знаний на основе JSONL файлов.
"""
import os
import json
import aiofiles
from datetime import datetime
from pathlib import Path
from typing import Any, Dict, Optional, List, Set, Tuple
import asyncio

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings
from .base import BaseKnowledgeStore
from ..normalizer.models import NormalizedUnit
from ..enrichment.models import SegmentModel, ClusterModel

# Получаем логгер
logger = get_logger(__name__)


class JSONLKnowledgeStore(BaseKnowledgeStore):
    """
    Реализация хранилища знаний на основе JSONL файлов.
    Простая реализация для MVP, которая сохраняет нормализованные единицы в JSONL-файл.
    """
    
    def __init__(self, config: Optional[Dict[str, Any]] = None):
        """
        Инициализация хранилища.
        
        Args:
            config: Конфигурация хранилища
        """
        super().__init__(config)
        
        # Получаем конфигурацию
        self.config = config or {}
        
        # Директория для хранения данных
        self.data_dir = Path(self.config.get("data_dir", settings.storage.knowledge_dir))
        self.data_dir.mkdir(exist_ok=True, parents=True)
        
        # Имя файла для хранения нормализованных единиц
        self.file_name = self.config.get("file_name", settings.storage.normalized_units_file)
        self.units_file = self.data_dir / self.file_name
        
        # Файл для хранения сегментов
        self.segments_file = self.data_dir / "segments.jsonl"
        
        # Файл для хранения кластеров
        self.clusters_file = self.data_dir / "clusters.jsonl"
        
        # Логирование инициализации
        logger.info(f"JSONLKnowledgeStore initialized. Data directory: {self.data_dir.resolve()}")
        logger.info(f"Units file: {self.units_file.resolve()}")
        logger.info(f"Segments file: {self.segments_file.resolve()}")
        logger.info(f"Clusters file: {self.clusters_file.resolve()}")
        
        # Если указан конкретный файл, выводим информацию
        if "file_name" in self.config:
            logger.info(f"Using custom units file: {self.units_file}")
        
    async def store(self, unit: NormalizedUnit) -> str:
        """
        Сохраняет нормализованную единицу в хранилище.
        
        Args:
            unit: Нормализованная единица для сохранения
            
        Returns:
            Идентификатор сохраненной единицы (unit.id)
        """
        # Добавляем время сохранения
        now = datetime.utcnow()
        unit_dict = unit.model_dump(mode="json")
        unit_dict["stored_at"] = now.isoformat()
        
        # Сохраняем единицу в JSONL-файл
        with open(self.units_file, "a") as f:
            f.write(json.dumps(unit_dict, ensure_ascii=False) + "\n")
            
        # Возвращаем идентификатор единицы (unit.id)
        return unit.id
    
    async def get(self, unit_id: str) -> Optional[NormalizedUnit]:
        """
        Получает нормализованную единицу из хранилища по идентификатору.
        
        Args:
            unit_id: Идентификатор единицы (unit.id)
            
        Returns:
            Нормализованная единица или None, если единица не найдена
        """
        # Проверяем существование файла
        if not self.units_file.exists():
            return None
            
        # Читаем файл и ищем единицу по идентификатору
        with open(self.units_file, "r") as f:
            for line in f:
                unit_dict = json.loads(line)
                if unit_dict.get("id") == unit_id:
                    # Удаляем служебные поля
                    if "stored_at" in unit_dict:
                        del unit_dict["stored_at"]
                        
                    # Создаем объект NormalizedUnit
                    return NormalizedUnit.model_validate(unit_dict)
                    
        # Если единица не найдена, возвращаем None
        return None

    async def load_all(self) -> List[NormalizedUnit]:
        """
        Загружает все нормализованные юниты из JSONL файла.
        Для PoC решение читает весь файл - для production нужен более эффективный вариант.
        """
        try:
            units_file = os.path.join(self.data_dir, self.file_name)
            logger.debug(f"Loading all normalized units from: {units_file}")
            
            if not os.path.exists(units_file):
                logger.warning(f"Units file not found at {units_file}, returning empty list")
                return []
            
            units: List[NormalizedUnit] = []
            async with aiofiles.open(units_file, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        unit_data = json.loads(line)
                        units.append(NormalizedUnit(**unit_data))
                    except Exception as e:
                        logger.error(f"Error loading normalized unit: {e}")
            
            logger.info(f"Successfully loaded {len(units)} normalized units from {units_file}")
            return units
        except Exception as e:
            logger.error(f"Failed to load normalized units: {e}", exc_info=True)
            return []
            
    async def list_all(self) -> List[NormalizedUnit]:
        """
        Возвращает список всех нормализованных единиц.
        
        Returns:
            Список нормализованных единиц
        """
        return await self.load_all()
        
    async def get_original_aggregate(self, unit_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает оригинальный агрегат для нормализованной единицы.
        
        Args:
            unit_id: ID нормализованной единицы (unit.id)
            
        Returns:
            Агрегат или None, если не найден
        """
        try:
            # Сначала получаем нормализованную единицу
            unit = await self.get(unit_id)
            if not unit:
                logger.warning(f"Unit {unit_id} not found")
                return None
            
            # Теперь загружаем агрегат по его ID
            from mindbank_poc.api.backends import jsonl_backend
            aggregate = await jsonl_backend.load_aggregate_by_id(unit.aggregate_id)
            
            if aggregate:
                # Преобразуем модель AggregateInput в словарь
                return aggregate.model_dump(mode="json")
            else:
                logger.warning(f"Original aggregate {unit.aggregate_id} not found for unit {unit_id}")
                return None
        except Exception as e:
            logger.error(f"Error loading original aggregate for unit {unit_id}: {e}")
            return None

    async def delete_all(self):
        """Удаляет все нормализованные единицы (очищает файл). Используется для тестов."""
        if self.units_file.exists():
            self.units_file.unlink()
            logger.info(f"Deleted all units from {self.units_file}")
    
    async def list_by_group(self, group_id: str) -> List[NormalizedUnit]:
        """
        Возвращает список нормализованных единиц для указанной группы.
        
        Args:
            group_id: Идентификатор группы
            
        Returns:
            Список нормализованных единиц группы
        """
        units = []
        
        if not self.units_file.exists():
            return units
            
        try:
            async with aiofiles.open(self.units_file, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        unit_data = json.loads(line)
                        if unit_data.get("group_id") == group_id:
                            units.append(NormalizedUnit(**unit_data))
                    except Exception as e:
                        logger.error(f"Error loading unit from line: {e}")
            
            logger.info(f"Found {len(units)} units for group {group_id}")
            return units
        except Exception as e:
            logger.error(f"Failed to load units by group: {e}", exc_info=True)
            return []
    
    async def list_unprocessed_groups(self, min_units: int = 10) -> List[str]:
        """
        Возвращает список групп с необработанными юнитами (без сегментов).
        
        Args:
            min_units: Минимальное количество юнитов в группе для обработки
            
        Returns:
            Список идентификаторов групп
        """
        group_counts = {}
        
        if not self.units_file.exists():
            return []
            
        try:
            # Сначала собираем все группы и количество юнитов в них
            async with aiofiles.open(self.units_file, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        unit_data = json.loads(line)
                        group_id = unit_data.get("group_id")
                        if group_id:
                            group_counts[group_id] = group_counts.get(group_id, 0) + 1
                    except Exception as e:
                        logger.error(f"Error processing unit: {e}")
            
            # Фильтруем группы по минимальному количеству юнитов
            qualified_groups = []
            for group_id, count in group_counts.items():
                if count >= min_units:
                    # Проверяем, есть ли уже сегменты для этой группы
                    segments = await self.list_segments_by_group(group_id)
                    if not segments:
                        qualified_groups.append(group_id)
            
            logger.info(f"Found {len(qualified_groups)} groups with >= {min_units} units and no segments")
            return qualified_groups
        except Exception as e:
            logger.error(f"Failed to list unprocessed groups: {e}", exc_info=True)
            return []
    
    async def list_group_ids(self) -> Set[str]:
        """
        Возвращает множество всех group_id в хранилище.
        
        Returns:
            Set[str]: Множество уникальных group_id
        """
        group_ids = set()
        
        try:
            # Проверяем, существует ли файл
            if not os.path.exists(self.units_file):
                logger.warning(f"Units file {self.units_file} does not exist")
                return group_ids
            
            # Читаем файл и собираем все group_id
            async with aiofiles.open(self.units_file, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if line:
                        try:
                            unit_data = json.loads(line)
                            group_id = unit_data.get('group_id')
                            if group_id:
                                group_ids.add(group_id)
                        except json.JSONDecodeError as e:
                            logger.warning(f"Failed to parse line in units file: {e}")
                            continue
            
            logger.debug(f"Found {len(group_ids)} unique group IDs")
            return group_ids
            
        except Exception as e:
            logger.error(f"Failed to list group IDs: {e}", exc_info=True)
            return set()

    # Методы для работы с сегментами
    async def store_segment(self, segment: SegmentModel) -> str:
        """
        Сохраняет сегмент в хранилище.
        
        Args:
            segment: Сегмент для сохранения
            
        Returns:
            Идентификатор сохраненного сегмента
        """
        try:
            # Добавляем время сохранения
            segment_dict = segment.model_dump(mode="json")
            segment_dict["stored_at"] = datetime.utcnow().isoformat()
            
            # Сохраняем сегмент в JSONL-файл
            async with aiofiles.open(self.segments_file, 'a', encoding='utf-8') as f:
                await f.write(json.dumps(segment_dict, ensure_ascii=False) + "\n")
            
            logger.info(f"Stored segment {segment.id} for group {segment.group_id}")
            return segment.id
            
        except Exception as e:
            logger.error(f"Failed to store segment: {e}", exc_info=True)
            raise
    
    async def get_segment(self, segment_id: str) -> Optional[SegmentModel]:
        """
        Получает сегмент из хранилища.
        
        Args:
            segment_id: Идентификатор сегмента
            
        Returns:
            Сегмент или None, если не найден
        """
        if not self.segments_file.exists():
            return None
        
        try:
            async with aiofiles.open(self.segments_file, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        segment_dict = json.loads(line)
                        if segment_dict.get("id") == segment_id:
                            # Удаляем служебные поля
                            segment_dict.pop("stored_at", None)
                            return SegmentModel(**segment_dict)
                    except Exception as e:
                        logger.error(f"Error parsing segment line: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get segment: {e}", exc_info=True)
            return None
    
    async def list_segments_by_group(self, group_id: str) -> List[SegmentModel]:
        """
        Получает все сегменты для указанной группы.
        
        Args:
            group_id: Идентификатор группы
            
        Returns:
            Список сегментов группы
        """
        segments = []
        
        if not self.segments_file.exists():
            return segments
        
        try:
            async with aiofiles.open(self.segments_file, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        segment_dict = json.loads(line)
                        if segment_dict.get("group_id") == group_id:
                            # Удаляем служебные поля
                            segment_dict.pop("stored_at", None)
                            segments.append(SegmentModel(**segment_dict))
                    except Exception as e:
                        logger.error(f"Error parsing segment line: {e}")
            
            logger.info(f"Found {len(segments)} segments for group {group_id}")
            return segments
            
        except Exception as e:
            logger.error(f"Failed to list segments by group: {e}", exc_info=True)
            return []
    
    async def get_segments_for_unit(self, unit_id: str) -> List[SegmentModel]:
        """
        Получает все сегменты, в которые входит указанный юнит.
        
        Args:
            unit_id: Идентификатор юнита (unit.id)
            
        Returns:
            Список сегментов, содержащих данный юнит
        """
        segments = []
        
        if not self.segments_file.exists():
            return segments
        
        try:
            async with aiofiles.open(self.segments_file, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        segment_dict = json.loads(line)
                        # Проверяем, содержит ли сегмент данный юнит
                        if unit_id in segment_dict.get("raw_unit_ids", []):
                            # Удаляем служебные поля
                            segment_dict.pop("stored_at", None)
                            segments.append(SegmentModel(**segment_dict))
                    except Exception as e:
                        logger.error(f"Error parsing segment line: {e}")
            
            logger.debug(f"Found {len(segments)} segments containing unit {unit_id}")
            return segments
            
        except Exception as e:
            logger.error(f"Failed to get segments for unit: {e}", exc_info=True)
            return []

    # Методы для работы с кластерами
    async def store_cluster(self, cluster: ClusterModel) -> str:
        """
        Сохраняет кластер в хранилище.
        
        Args:
            cluster: Кластер для сохранения
            
        Returns:
            Идентификатор сохраненного кластера
        """
        try:
            # Добавляем время сохранения
            cluster_dict = cluster.model_dump(mode="json")
            cluster_dict["stored_at"] = datetime.utcnow().isoformat()
            
            # Сохраняем кластер в JSONL-файл
            async with aiofiles.open(self.clusters_file, 'a', encoding='utf-8') as f:
                await f.write(json.dumps(cluster_dict, ensure_ascii=False) + "\n")
            
            logger.info(f"Stored cluster {cluster.id} with {cluster.cluster_size} segments")
            return cluster.id
            
        except Exception as e:
            logger.error(f"Failed to store cluster: {e}", exc_info=True)
            raise
    
    async def get_cluster(self, cluster_id: str) -> Optional[ClusterModel]:
        """
        Получает кластер из хранилища.
        
        Args:
            cluster_id: Идентификатор кластера
            
        Returns:
            Кластер или None, если не найден
        """
        if not self.clusters_file.exists():
            return None
        
        try:
            async with aiofiles.open(self.clusters_file, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        cluster_dict = json.loads(line)
                        if cluster_dict.get("id") == cluster_id:
                            # Удаляем служебные поля
                            cluster_dict.pop("stored_at", None)
                            return ClusterModel(**cluster_dict)
                    except Exception as e:
                        logger.error(f"Error parsing cluster line: {e}")
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get cluster: {e}", exc_info=True)
            return None
    
    async def list_clusters(self) -> List[ClusterModel]:
        """
        Получает все кластеры из хранилища.
        
        Returns:
            Список всех кластеров
        """
        clusters = []
        
        if not self.clusters_file.exists():
            return clusters
        
        try:
            async with aiofiles.open(self.clusters_file, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        cluster_dict = json.loads(line)
                        # Удаляем служебные поля
                        cluster_dict.pop("stored_at", None)
                        clusters.append(ClusterModel(**cluster_dict))
                    except Exception as e:
                        logger.error(f"Error parsing cluster line: {e}")
            
            logger.info(f"Found {len(clusters)} clusters in storage")
            return clusters
            
        except Exception as e:
            logger.error(f"Failed to list clusters: {e}", exc_info=True)
            return []
    
    async def get_clusters_for_segment(self, segment_id: str) -> List[ClusterModel]:
        """
        Получает все кластеры, в которые входит указанный сегмент.
        
        Args:
            segment_id: Идентификатор сегмента
            
        Returns:
            Список кластеров, содержащих данный сегмент
        """
        clusters = []
        
        if not self.clusters_file.exists():
            return clusters
        
        try:
            async with aiofiles.open(self.clusters_file, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        cluster_dict = json.loads(line)
                        # Проверяем, содержит ли кластер данный сегмент
                        if segment_id in cluster_dict.get("segment_ids", []):
                            # Удаляем служебные поля
                            cluster_dict.pop("stored_at", None)
                            clusters.append(ClusterModel(**cluster_dict))
                    except Exception as e:
                        logger.error(f"Error parsing cluster line: {e}")
            
            logger.debug(f"Found {len(clusters)} clusters containing segment {segment_id}")
            return clusters
            
        except Exception as e:
            logger.error(f"Failed to get clusters for segment: {e}", exc_info=True)
            return []

    # New method: segments by cluster
    async def list_segments_by_cluster(self, cluster_id: str) -> List[SegmentModel]:
        """Возвращает список сегментов, принадлежащих кластеру."""
        segments: List[SegmentModel] = []
        # Получаем кластер
        cluster = await self.get_cluster(cluster_id)
        if not cluster or not cluster.segment_ids:
            return segments

        # Создаём set для быстрого поиска
        segment_ids_set = set(cluster.segment_ids)

        if not self.segments_file.exists():
            return segments

        try:
            async with aiofiles.open(self.segments_file, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    try:
                        segment_dict = json.loads(line)
                        sid = segment_dict.get("id")
                        if sid and sid in segment_ids_set:
                            segment_dict.pop("stored_at", None)
                            segments.append(SegmentModel(**segment_dict))
                            # Оптимизация: выходим, если собрали все
                            if len(segments) == len(segment_ids_set):
                                break
                    except Exception as e:
                        logger.error(f"Error parsing segment line: {e}")

            logger.debug(f"Found {len(segments)} segments for cluster {cluster_id}")
            return segments
        except Exception as e:
            logger.error(f"Failed to list segments by cluster: {e}", exc_info=True)
            return segments

    def _group_meta_file(self):
        return self.data_dir / "group_segmentation_meta.json"

    async def get_group_segmentation_meta(self, group_id: str) -> dict:
        """Возвращает метаинформацию по сегментации для группы (или пустой dict)."""
        meta_file = self._group_meta_file()
        if not meta_file.exists():
            return {}
        async with aiofiles.open(meta_file, 'r', encoding='utf-8') as f:
            content = await f.read()
            if not content.strip():
                return {}
            try:
                meta = json.loads(content)
                return meta.get(group_id, {})
            except Exception:
                return {}

    async def set_group_segmentation_meta(self, group_id: str, last_segmented_at: str, last_segmented_unit_id: str):
        """Обновляет метаинформацию по сегментации для группы."""
        meta_file = self._group_meta_file()
        meta = {}
        if meta_file.exists():
            async with aiofiles.open(meta_file, 'r', encoding='utf-8') as f:
                content = await f.read()
                if content.strip():
                    try:
                        meta = json.loads(content)
                    except Exception:
                        meta = {}
        meta[group_id] = {
            "last_segmented_at": last_segmented_at,
            "last_segmented_unit_id": last_segmented_unit_id
        }
        async with aiofiles.open(meta_file, 'w', encoding='utf-8') as f:
            await f.write(json.dumps(meta, ensure_ascii=False, indent=2))
    
    async def search(
        self,
        query_text: Optional[str] = None,
        where_filters: Optional[Dict[str, Any]] = None,
        limit: int = 10
    ) -> List[Tuple[NormalizedUnit, float]]:
        """
        Выполняет поиск в хранилище по тексту и/или фильтрам метаданных.
        
        Args:
            query_text: Текст запроса для семантического поиска  
            where_filters: Фильтры по метаданным
            limit: Максимальное количество результатов
            
        Returns:
            Список кортежей (unit, score) с найденными единицами и их релевантностью
        """
        # JSONL хранилище не поддерживает эффективный поиск
        # Этот метод добавлен для совместимости, но не должен использоваться
        # RetrievalService будет использовать собственную логику для JSONL
        logger.warning("Search method called on JSONLKnowledgeStore - this should use RetrievalService logic instead")
        return []

    async def get_groups_with_new_units_for_segmentation(self, min_units: int = 10) -> list:
        """Возвращает группы, где есть новые юниты после последней сегментации."""
        group_ids = await self.list_group_ids()
        result = []
        for group_id in group_ids:
            units = await self.list_by_group(group_id)
            if not units:
                continue
            units_sorted = sorted(units, key=lambda u: (u.normalized_at or u.stored_at or ""))
            last_unit = units_sorted[-1]
            meta = await self.get_group_segmentation_meta(group_id)
            last_segmented_unit_id = meta.get("last_segmented_unit_id")
            # Если сегментации не было или есть новые юниты
            if not last_segmented_unit_id or any(u.id > last_segmented_unit_id for u in units_sorted):
                if len(units) >= min_units:
                    result.append(group_id)
        return result
