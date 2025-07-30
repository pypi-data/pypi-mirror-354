"""
Базовые интерфейсы и абстракции для хранилища знаний.
"""
from abc import ABC, abstractmethod
from typing import Any, Dict, List, Optional, Protocol, Set, Tuple, TYPE_CHECKING

from ..normalizer.models import NormalizedUnit

if TYPE_CHECKING:
    from ..enrichment.models import SegmentModel, ClusterModel


class KnowledgeStore(Protocol):
    """Протокол для хранилища знаний."""
    
    # Операции с NormalizedUnit
    async def store(self, unit: NormalizedUnit) -> str:
        """
        Сохраняет нормализованную единицу в хранилище.
        
        Args:
            unit: Нормализованная единица для сохранения
            
        Returns:
            Идентификатор сохраненной единицы
        """
        ...
        
    async def get(self, unit_id: str) -> Optional[NormalizedUnit]:
        """
        Получает нормализованную единицу из хранилища.
        
        Args:
            unit_id: Идентификатор единицы
            
        Returns:
            Нормализованная единица или None, если единица не найдена
        """
        ...
    
    # Операции с сегментами
    async def store_segment(self, segment: "SegmentModel") -> str:
        """
        Сохраняет сегмент в хранилище.
        
        Args:
            segment: Сегмент для сохранения
            
        Returns:
            Идентификатор сохраненного сегмента
        """
        ...
    
    async def get_segment(self, segment_id: str) -> Optional["SegmentModel"]:
        """
        Получает сегмент из хранилища.
        
        Args:
            segment_id: Идентификатор сегмента
            
        Returns:
            Сегмент или None, если не найден
        """
        ...
    
    async def list_segments_by_group(self, group_id: str) -> List["SegmentModel"]:
        """
        Получает все сегменты для указанной группы.
        
        Args:
            group_id: Идентификатор группы
            
        Returns:
            Список сегментов группы
        """
        ...
    
    async def get_segments_for_unit(self, unit_id: str) -> List["SegmentModel"]:
        """
        Получает все сегменты, в которые входит указанный юнит.
        
        Args:
            unit_id: Идентификатор юнита (unit.id)
            
        Returns:
            Список сегментов, содержащих данный юнит
        """
        ...

    # Операции с кластерами
    async def store_cluster(self, cluster: "ClusterModel") -> str:
        """
        Сохраняет кластер в хранилище.
        
        Args:
            cluster: Кластер для сохранения
            
        Returns:
            Идентификатор сохраненного кластера
        """
        ...
    
    async def get_cluster(self, cluster_id: str) -> Optional["ClusterModel"]:
        """
        Получает кластер из хранилища.
        
        Args:
            cluster_id: Идентификатор кластера
            
        Returns:
            Кластер или None, если не найден
        """
        ...
    
    async def list_clusters(self) -> List["ClusterModel"]:
        """
        Получает все кластеры из хранилища.
        
        Returns:
            Список всех кластеров
        """
        ...
    
    async def get_clusters_for_segment(self, segment_id: str) -> List["ClusterModel"]:
        """
        Получает все кластеры, в которые входит указанный сегмент.
        
        Args:
            segment_id: Идентификатор сегмента
            
        Returns:
            Список кластеров, содержащих данный сегмент
        """
        ...

    async def list_segments_by_cluster(self, cluster_id: str) -> List["SegmentModel"]:
        """
        Получает все сегменты, принадлежащие указанному кластеру.

        Args:
            cluster_id: Идентификатор кластера

        Returns:
            Список сегментов кластера
        """
        ...
    
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
        ...


class BaseKnowledgeStore(ABC):
    """Базовый класс для хранилища знаний."""
    
    def __init__(self, config: Dict[str, Any]):
        """
        Инициализация хранилища.
        
        Args:
            config: Конфигурация хранилища
        """
        self.config = config
    
    # Абстрактные методы для NormalizedUnit
    @abstractmethod
    async def store(self, unit: NormalizedUnit) -> str:
        """
        Сохраняет нормализованную единицу в хранилище.
        
        Args:
            unit: Нормализованная единица для сохранения
            
        Returns:
            Идентификатор сохраненной единицы
        """
        pass
    
    @abstractmethod
    async def get(self, unit_id: str) -> Optional[NormalizedUnit]:
        """
        Получает нормализованную единицу из хранилища.
        
        Args:
            unit_id: Идентификатор единицы
            
        Returns:
            Нормализованная единица или None, если единица не найдена
        """
        pass
    
    # Абстрактные методы для сегментов
    @abstractmethod
    async def store_segment(self, segment: "SegmentModel") -> str:
        """
        Сохраняет сегмент в хранилище.
        
        Args:
            segment: Сегмент для сохранения
            
        Returns:
            Идентификатор сохраненного сегмента
        """
        pass
    
    @abstractmethod
    async def get_segment(self, segment_id: str) -> Optional["SegmentModel"]:
        """
        Получает сегмент из хранилища.
        
        Args:
            segment_id: Идентификатор сегмента
            
        Returns:
            Сегмент или None, если не найден
        """
        pass
    
    @abstractmethod
    async def list_segments_by_group(self, group_id: str) -> List["SegmentModel"]:
        """
        Получает все сегменты для указанной группы.
        
        Args:
            group_id: Идентификатор группы
            
        Returns:
            Список сегментов группы
        """
        pass
    
    @abstractmethod
    async def get_segments_for_unit(self, unit_id: str) -> List["SegmentModel"]:
        """
        Получает все сегменты, в которые входит указанный юнит.
        
        Args:
            unit_id: Идентификатор юнита (unit.id)
            
        Returns:
            Список сегментов, содержащих данный юнит
        """
        ...
    
    @abstractmethod
    async def list_segments_by_cluster(self, cluster_id: str) -> List["SegmentModel"]:
        """Получает все сегменты, принадлежащие указанному кластеру."""
        pass
    
    # Методы для работы с группами
    @abstractmethod
    async def list_group_ids(self) -> Set[str]:
        """
        Возвращает множество всех group_id в хранилище.
        
        Returns:
            Множество уникальных group_id
        """
        pass
    
    @abstractmethod
    async def list_by_group(self, group_id: str) -> List[NormalizedUnit]:
        """
        Возвращает список нормализованных единиц для указанной группы.
        
        Args:
            group_id: Идентификатор группы
            
        Returns:
            Список нормализованных единиц группы
        """
        pass
    
    @abstractmethod
    async def get_original_aggregate(self, unit_id: str) -> Optional[Dict[str, Any]]:
        """
        Получает оригинальный агрегат для нормализованной единицы.
        
        Args:
            unit_id: Идентификатор юнита (unit.id)
            
        Returns:
            Агрегат или None, если не найден
        """
        pass
    
    # Абстрактные методы для кластеров
    @abstractmethod
    async def store_cluster(self, cluster: "ClusterModel") -> str:
        """
        Сохраняет кластер в хранилище.
        
        Args:
            cluster: Кластер для сохранения
            
        Returns:
            Идентификатор сохраненного кластера
        """
        pass
    
    @abstractmethod
    async def get_cluster(self, cluster_id: str) -> Optional["ClusterModel"]:
        """
        Получает кластер из хранилища.
        
        Args:
            cluster_id: Идентификатор кластера
            
        Returns:
            Кластер или None, если не найден
        """
        pass
    
    @abstractmethod
    async def list_clusters(self) -> List["ClusterModel"]:
        """
        Получает все кластеры из хранилища.
        
        Returns:
            Список всех кластеров
        """
        pass
    
    @abstractmethod
    async def get_clusters_for_segment(self, segment_id: str) -> List["ClusterModel"]:
        """
        Получает все кластеры, в которые входит указанный сегмент.
        
        Args:
            segment_id: Идентификатор сегмента
            
        Returns:
            Список кластеров, содержащих данный сегмент
        """
        pass
    
    @abstractmethod
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
        pass 