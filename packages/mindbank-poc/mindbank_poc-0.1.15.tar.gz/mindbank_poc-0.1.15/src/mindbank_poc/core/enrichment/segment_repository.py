"""
Репозиторий для хранения и управления сегментами.
"""
import json
from pathlib import Path
from typing import List, Optional, Union
from datetime import datetime

import aiofiles

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings
from .models import SegmentModel

logger = get_logger(__name__)


class SegmentRepository:
    """
    Репозиторий для работы с сегментами.
    Использует JSONL формат для хранения.
    """
    
    def __init__(self, data_dir: Optional[Union[str, Path]] = None):
        """
        Инициализация репозитория.
        
        Args:
            data_dir: Директория для хранения данных (строка или Path)
        """
        # Преобразуем data_dir в Path объект
        if data_dir is None:
            self.data_dir = Path(settings.storage.knowledge_dir) / "segments"
        else:
            self.data_dir = Path(data_dir) if isinstance(data_dir, str) else data_dir
        
        # Создаем директорию если не существует
        self.data_dir.mkdir(parents=True, exist_ok=True)
        
        # Путь к файлу с сегментами
        self.segments_file = self.data_dir / "segments.jsonl"
        
        logger.info(f"SegmentRepository initialized with file: {self.segments_file}")
    
    async def save(self, segment: SegmentModel) -> str:
        """
        Сохраняет сегмент в хранилище.
        
        Args:
            segment: Сегмент для сохранения
            
        Returns:
            ID сохраненного сегмента
        """
        try:
            segment_dict = segment.model_dump(mode="json")
            segment_dict["stored_at"] = datetime.utcnow().isoformat()
            
            async with aiofiles.open(self.segments_file, 'a', encoding='utf-8') as f:
                await f.write(json.dumps(segment_dict, ensure_ascii=False) + "\n")
            
            logger.info(f"Saved segment {segment.id} for group {segment.group_id}")
            return segment.id
            
        except Exception as e:
            logger.error(f"Failed to save segment: {e}", exc_info=True)
            raise
    
    async def get_by_id(self, segment_id: str) -> Optional[SegmentModel]:
        """
        Получает сегмент по ID.
        
        Args:
            segment_id: Идентификатор сегмента
            
        Returns:
            Сегмент или None
        """
        if not self.segments_file.exists():
            return None
            
        try:
            async with aiofiles.open(self.segments_file, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    segment_dict = json.loads(line)
                    if segment_dict.get("id") == segment_id:
                        # Удаляем служебные поля
                        segment_dict.pop("stored_at", None)
                        return SegmentModel(**segment_dict)
            
            return None
            
        except Exception as e:
            logger.error(f"Failed to get segment by id: {e}", exc_info=True)
            return None
    
    async def list_by_group(self, group_id: str) -> List[SegmentModel]:
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
                    
                    segment_dict = json.loads(line)
                    if segment_dict.get("group_id") == group_id:
                        # Удаляем служебные поля
                        segment_dict.pop("stored_at", None)
                        segments.append(SegmentModel(**segment_dict))
            
            logger.info(f"Found {len(segments)} segments for group {group_id}")
            return segments
            
        except Exception as e:
            logger.error(f"Failed to list segments by group: {e}", exc_info=True)
            return []
    
    async def list_all(self) -> List[SegmentModel]:
        """
        Получает все сегменты.
        
        Returns:
            Список всех сегментов
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
                    
                    segment_dict = json.loads(line)
                    # Удаляем служебные поля
                    segment_dict.pop("stored_at", None)
                    segments.append(SegmentModel(**segment_dict))
            
            logger.info(f"Loaded {len(segments)} segments total")
            return segments
            
        except Exception as e:
            logger.error(f"Failed to list all segments: {e}", exc_info=True)
            return []
    
    async def delete_by_group(self, group_id: str) -> int:
        """
        Удаляет все сегменты указанной группы.
        
        Args:
            group_id: Идентификатор группы
            
        Returns:
            Количество удаленных сегментов
        """
        if not self.segments_file.exists():
            return 0
            
        try:
            # Читаем все сегменты
            segments_to_keep = []
            deleted_count = 0
            
            async with aiofiles.open(self.segments_file, 'r', encoding='utf-8') as f:
                async for line in f:
                    line = line.strip()
                    if not line:
                        continue
                    
                    segment_dict = json.loads(line)
                    if segment_dict.get("group_id") != group_id:
                        segments_to_keep.append(segment_dict)
                    else:
                        deleted_count += 1
            
            # Перезаписываем файл без удаленных сегментов
            async with aiofiles.open(self.segments_file, 'w', encoding='utf-8') as f:
                for segment_dict in segments_to_keep:
                    await f.write(json.dumps(segment_dict, ensure_ascii=False) + "\n")
            
            logger.info(f"Deleted {deleted_count} segments for group {group_id}")
            return deleted_count
            
        except Exception as e:
            logger.error(f"Failed to delete segments by group: {e}", exc_info=True)
            return 0
