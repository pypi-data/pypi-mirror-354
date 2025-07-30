#!/usr/bin/env python3
"""
Миграционный скрипт для добавления уникальных ID к существующим агрегатам и нормализованным юнитам.
"""
import json
import uuid
import argparse
import shutil
from pathlib import Path
from datetime import datetime
from typing import Dict, List, Set

from mindbank_poc.common.logging import get_logger
from mindbank_poc.core.config.settings import settings

logger = get_logger(__name__)


def migrate_aggregates(aggregates_file: Path, backup: bool = True) -> Dict[str, str]:
    """
    Мигрирует файл агрегатов, добавляя уникальные ID.
    
    Args:
        aggregates_file: Путь к файлу агрегатов
        backup: Создавать ли резервную копию
        
    Returns:
        Словарь маппинга {group_id: aggregate_id}
    """
    if not aggregates_file.exists():
        logger.warning(f"Aggregates file {aggregates_file} not found")
        return {}
    
    # Создаем резервную копию
    if backup:
        backup_file = aggregates_file.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copy2(aggregates_file, backup_file)
        logger.info(f"Created backup: {backup_file}")
    
    # Маппинг для отслеживания ID
    group_to_aggregate_id: Dict[str, str] = {}
    
    # Читаем и обновляем агрегаты
    updated_lines = []
    with open(aggregates_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                aggregate = json.loads(line)
                
                # Если у агрегата уже есть id, используем его
                if "id" in aggregate:
                    aggregate_id = aggregate["id"]
                    logger.debug(f"Line {line_num}: Aggregate already has id: {aggregate_id}")
                else:
                    # Генерируем новый id
                    aggregate_id = str(uuid.uuid4())
                    aggregate["id"] = aggregate_id
                    logger.info(f"Line {line_num}: Added id {aggregate_id} to aggregate with group_id {aggregate.get('group_id')}")
                
                # Сохраняем маппинг
                group_id = aggregate.get("group_id")
                if group_id:
                    group_to_aggregate_id[group_id] = aggregate_id
                
                updated_lines.append(json.dumps(aggregate, ensure_ascii=False) + "\n")
                
            except json.JSONDecodeError as e:
                logger.error(f"Line {line_num}: Failed to parse JSON: {e}")
                # Сохраняем строку как есть
                updated_lines.append(line + "\n")
    
    # Записываем обновленные данные
    with open(aggregates_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)
    
    logger.info(f"Updated {len(group_to_aggregate_id)} aggregates with IDs")
    return group_to_aggregate_id


def migrate_normalized_units(units_file: Path, group_to_aggregate_id: Dict[str, str], backup: bool = True) -> Set[str]:
    """
    Мигрирует файл нормализованных юнитов, добавляя уникальные ID.
    
    Args:
        units_file: Путь к файлу юнитов
        group_to_aggregate_id: Маппинг group_id -> aggregate_id
        backup: Создавать ли резервную копию
        
    Returns:
        Множество ID юнитов
    """
    if not units_file.exists():
        logger.warning(f"Units file {units_file} not found")
        return set()
    
    # Создаем резервную копию
    if backup:
        backup_file = units_file.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copy2(units_file, backup_file)
        logger.info(f"Created backup: {backup_file}")
    
    unit_ids: Set[str] = set()
    
    # Читаем и обновляем юниты
    updated_lines = []
    with open(units_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                unit = json.loads(line)
                
                # Если у юнита уже есть id, используем его
                if "id" in unit:
                    unit_id = unit["id"]
                    logger.debug(f"Line {line_num}: Unit already has id: {unit_id}")
                else:
                    # Генерируем новый id
                    unit_id = str(uuid.uuid4())
                    unit["id"] = unit_id
                    logger.info(f"Line {line_num}: Added id {unit_id} to unit")
                
                unit_ids.add(unit_id)
                
                # Исправляем aggregate_id если он равен group_id
                current_aggregate_id = unit.get("aggregate_id")
                group_id = unit.get("group_id")
                
                if current_aggregate_id == group_id and group_id in group_to_aggregate_id:
                    # Заменяем на правильный aggregate_id
                    correct_aggregate_id = group_to_aggregate_id[group_id]
                    unit["aggregate_id"] = correct_aggregate_id
                    logger.info(f"Line {line_num}: Fixed aggregate_id from {current_aggregate_id} to {correct_aggregate_id}")
                
                updated_lines.append(json.dumps(unit, ensure_ascii=False) + "\n")
                
            except json.JSONDecodeError as e:
                logger.error(f"Line {line_num}: Failed to parse JSON: {e}")
                # Сохраняем строку как есть
                updated_lines.append(line + "\n")
    
    # Записываем обновленные данные
    with open(units_file, 'w', encoding='utf-8') as f:
        f.writelines(updated_lines)
    
    logger.info(f"Updated {len(unit_ids)} normalized units with IDs")
    return unit_ids


def migrate_segments(segments_file: Path, unit_ids: Set[str], backup: bool = True):
    """
    Мигрирует файл сегментов, обновляя ссылки на юниты.
    
    Args:
        segments_file: Путь к файлу сегментов
        unit_ids: Множество ID юнитов (для валидации)
        backup: Создавать ли резервную копию
    """
    if not segments_file.exists():
        logger.warning(f"Segments file {segments_file} not found")
        return
    
    # Создаем резервную копию
    if backup:
        backup_file = segments_file.with_suffix(f".backup_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
        shutil.copy2(segments_file, backup_file)
        logger.info(f"Created backup: {backup_file}")
    
    # На данный момент сегменты уже должны использовать правильные ID юнитов
    # Но проверим валидность ссылок
    
    valid_segments = 0
    invalid_segments = 0
    
    with open(segments_file, 'r', encoding='utf-8') as f:
        for line_num, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            
            try:
                segment = json.loads(line)
                raw_unit_ids = segment.get("raw_unit_ids", [])
                
                # Проверяем, что все ссылки валидны
                invalid_refs = [uid for uid in raw_unit_ids if uid not in unit_ids]
                
                if invalid_refs:
                    logger.warning(f"Line {line_num}: Segment {segment.get('id')} has invalid unit references: {invalid_refs}")
                    invalid_segments += 1
                else:
                    valid_segments += 1
                    
            except json.JSONDecodeError as e:
                logger.error(f"Line {line_num}: Failed to parse JSON: {e}")
    
    logger.info(f"Segments validation: {valid_segments} valid, {invalid_segments} with invalid references")


def main():
    parser = argparse.ArgumentParser(description="Migrate existing data to add unique IDs")
    parser.add_argument("--data-dir", type=Path, default=None, help="Data directory (default: from settings)")
    parser.add_argument("--no-backup", action="store_true", help="Skip creating backup files")
    parser.add_argument("--dry-run", action="store_true", help="Only analyze, don't modify files")
    
    args = parser.parse_args()
    
    # Определяем директорию с данными
    data_dir = args.data_dir or Path(settings.storage.data_dir)
    
    if not data_dir.exists():
        logger.error(f"Data directory {data_dir} not found")
        return 1
    
    logger.info(f"Starting migration in {data_dir}")
    
    # Пути к файлам
    aggregates_file = data_dir / "ingest_jsonl" / "aggregates.jsonl"
    units_file = data_dir / settings.storage.normalized_units_file
    segments_file = data_dir / "segments.jsonl"
    
    if args.dry_run:
        logger.info("DRY RUN MODE - no files will be modified")
        
        # Анализируем файлы
        if aggregates_file.exists():
            with open(aggregates_file, 'r') as f:
                total = missing_id = 0
                for line in f:
                    if line.strip():
                        total += 1
                        agg = json.loads(line)
                        if "id" not in agg:
                            missing_id += 1
                logger.info(f"Aggregates: {total} total, {missing_id} missing ID")
        
        if units_file.exists():
            with open(units_file, 'r') as f:
                total = missing_id = wrong_aggregate_id = 0
                for line in f:
                    if line.strip():
                        total += 1
                        unit = json.loads(line)
                        if "id" not in unit:
                            missing_id += 1
                        if unit.get("aggregate_id") == unit.get("group_id"):
                            wrong_aggregate_id += 1
                logger.info(f"Units: {total} total, {missing_id} missing ID, {wrong_aggregate_id} with wrong aggregate_id")
        
        return 0
    
    # Выполняем миграцию
    backup = not args.no_backup
    
    # 1. Мигрируем агрегаты
    logger.info("Step 1: Migrating aggregates...")
    group_to_aggregate_id = migrate_aggregates(aggregates_file, backup)
    
    # 2. Мигрируем нормализованные юниты
    logger.info("Step 2: Migrating normalized units...")
    unit_ids = migrate_normalized_units(units_file, group_to_aggregate_id, backup)
    
    # 3. Проверяем сегменты
    logger.info("Step 3: Validating segments...")
    migrate_segments(segments_file, unit_ids, backup)
    
    logger.info("Migration completed successfully!")
    return 0


if __name__ == "__main__":
    exit(main()) 