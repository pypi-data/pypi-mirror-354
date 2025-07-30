"""
Утилиты для обработки и валидации сегментов.
"""
from typing import List, Dict, Any
import json

from mindbank_poc.common.logging import get_logger

logger = get_logger(__name__)


def merge_overlaps(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Удаляет перекрывающиеся сегменты.
    
    Оставляет только те сегменты, чей start > last_end.
    
    Args:
        segments: Список сегментов с полями start и end
        
    Returns:
        Список сегментов без перекрытий
    """
    if not segments:
        return []
    
    # Сортируем по start, затем по end
    sorted_segments = sorted(segments, key=lambda s: (s.get("start", 0), s.get("end", 0)))
    
    clean = []
    last_end = 0
    
    for segment in sorted_segments:
        start = segment.get("start", 0)
        end = segment.get("end", 0)
        
        # Пропускаем если начало <= последнего конца
        if start <= last_end:
            logger.debug(f"Skipping overlapping segment: start={start}, end={end}, last_end={last_end}")
            continue
            
        clean.append(segment)
        last_end = end
    
    logger.info(f"Merged overlaps: {len(segments)} -> {len(clean)} segments")
    return clean


def merge_contiguous(segments: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Объединяет соседние сегменты с похожими заголовками.
    
    Если два сегмента идут подряд (end+1 == start) и имеют похожие заголовки,
    они объединяются в один.
    
    Args:
        segments: Список сегментов
        
    Returns:
        Список сегментов после объединения
    """
    if not segments:
        return []
    
    merged = []
    
    for segment in segments:
        if not merged:
            merged.append(segment.copy())
            continue
        
        last = merged[-1]
        
        # Проверяем, идут ли подряд
        if last.get("end", 0) + 1 == segment.get("start", 0):
            # Проверяем похожесть заголовков
            last_title_root = last.get("title", "").split()[0].lower() if last.get("title") else ""
            curr_title_root = segment.get("title", "").split()[0].lower() if segment.get("title") else ""
            
            if last_title_root and last_title_root == curr_title_root:
                # Объединяем
                last["end"] = segment.get("end", last["end"])
                last["summary"] = last.get("summary", "") + " " + segment.get("summary", "")
                
                # Объединяем unit_indices если есть
                if "unit_indices" in last and "unit_indices" in segment:
                    last["unit_indices"].extend(segment["unit_indices"])
                
                # Объединяем entities если есть
                if "entities" in last and "entities" in segment:
                    # Добавляем уникальные entities
                    existing = set(tuple(e.items()) if isinstance(e, dict) else e for e in last["entities"])
                    for entity in segment["entities"]:
                        entity_tuple = tuple(entity.items()) if isinstance(entity, dict) else entity
                        if entity_tuple not in existing:
                            last["entities"].append(entity)
                
                logger.debug(f"Merged contiguous segments: {last_title_root}")
                continue
        
        merged.append(segment.copy())
    
    logger.info(f"Merged contiguous: {len(segments)} -> {len(merged)} segments")
    return merged


def validate_segments(segments_data: Any) -> List[Dict[str, Any]]:
    """
    Валидирует и нормализует данные сегментов.
    
    Args:
        segments_data: JSON данные сегментов (строка или уже распарсенные)
        
    Returns:
        Список валидных сегментов
    """
    # Парсим если это строка
    if isinstance(segments_data, str):
        try:
            segments_data = json.loads(segments_data)
        except json.JSONDecodeError as e:
            logger.error(f"Failed to parse segments JSON: {e}")
            return []
    
    # Проверяем что это список
    if not isinstance(segments_data, list):
        logger.error(f"Segments data is not a list: {type(segments_data)}")
        return []
    
    validated = []
    
    for i, segment in enumerate(segments_data):
        if not isinstance(segment, dict):
            logger.warning(f"Segment {i} is not a dict: {type(segment)}")
            continue
        
        # Проверяем обязательные поля
        if not all(key in segment for key in ["title", "summary"]):
            logger.warning(f"Segment {i} missing required fields: {segment.keys()}")
            continue
        
        # Копируем сегмент
        valid_segment = segment.copy()
        
        # Добавляем дефолтные значения
        valid_segment.setdefault("start", i + 1)
        valid_segment.setdefault("end", i + 1)
        valid_segment.setdefault("entities", [])
        valid_segment.setdefault("timeline", {})
        
        # Нормализуем типы
        valid_segment["start"] = int(valid_segment["start"])
        valid_segment["end"] = int(valid_segment["end"])
        
        validated.append(valid_segment)
    
    return validated


def crop_text(text: str, max_length: int = 40) -> str:
    """
    Обрезает текст до указанной длины с добавлением многоточия.
    
    Args:
        text: Исходный текст
        max_length: Максимальная длина
        
    Returns:
        Обрезанный текст
    """
    if len(text) <= max_length:
        return text
    return text[:max_length] + "…" 