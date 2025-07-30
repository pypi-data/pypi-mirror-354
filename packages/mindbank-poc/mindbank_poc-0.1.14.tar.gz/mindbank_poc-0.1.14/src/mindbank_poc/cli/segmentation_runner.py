"""
CLI утилита для запуска сегментации нормализованных юнитов.
"""
import asyncio
import argparse
from pathlib import Path
import sys
from typing import Optional

from mindbank_poc.common.logging import setup_logging, get_logger
from mindbank_poc.core.knowledge_store import get_knowledge_store
from mindbank_poc.core.enrichment import SegmentationService
from mindbank_poc.core.providers.segmentation import register_segmentation_providers

# Настройка логирования
setup_logging("segmentation")
logger = get_logger(__name__)


async def segment_group(group_id: str, dry_run: bool = False):
    """Выполняет сегментацию для указанной группы."""
    logger.info(f"Starting segmentation for group: {group_id}")
    
    # Инициализируем хранилище знаний
    knowledge_store = get_knowledge_store()
    
    # Создаем сервис сегментации
    segmentation_service = SegmentationService(knowledge_store)
    
    if dry_run:
        logger.info("DRY RUN MODE - no actual segmentation will be performed")
        # Получаем юниты группы для предпросмотра
        if hasattr(knowledge_store, 'list_by_group'):
            units = await knowledge_store.list_by_group(group_id)
        else:
            all_units = await knowledge_store.list_all()
            units = [u for u in all_units if u.group_id == group_id]
        
        logger.info(f"Found {len(units)} units in group {group_id}")
        for i, unit in enumerate(units[:5]):  # Показываем первые 5
            logger.info(f"  Unit {i+1}: {unit.text_repr[:100]}...")
        
        if len(units) > 5:
            logger.info(f"  ... and {len(units) - 5} more units")
        return
    
    # Выполняем сегментацию только новых юнитов
    segments = await segmentation_service.segment_group(group_id)
    
    if segments:
        logger.info(f"Successfully created {len(segments)} segments for group {group_id}")
        for segment in segments:
            logger.info(f"  - {segment.title}: {segment.summary[:100]}...")
    else:
        logger.warning(f"No new segments created for group {group_id} (no new units or segmentation skipped)")


async def segment_all(dry_run: bool = False):
    """Выполняет сегментацию для всех групп."""
    logger.info("Starting segmentation for all groups")
    
    # Инициализируем хранилище знаний
    knowledge_store = get_knowledge_store()
    
    # Создаем сервис сегментации
    segmentation_service = SegmentationService(knowledge_store)
    
    if dry_run:
        logger.info("DRY RUN MODE - listing groups only")
        # Получаем все группы
        if hasattr(knowledge_store, 'list_group_ids'):
            group_ids = await knowledge_store.list_group_ids()
        else:
            all_units = await knowledge_store.list_all()
            group_ids = set(u.group_id for u in all_units if u.group_id)
        
        logger.info(f"Found {len(group_ids)} groups total")
        for group_id in list(group_ids)[:10]:  # Показываем первые 10
            logger.info(f"  - {group_id}")
        
        if len(group_ids) > 10:
            logger.info(f"  ... and {len(group_ids) - 10} more groups")
        return
    
    # Выполняем сегментацию
    results = await segmentation_service.segment_all_groups()
    
    total_segments = sum(len(segments) for segments in results.values())
    logger.info(f"Successfully created {total_segments} segments across {len(results)} groups")


async def list_groups():
    """Выводит список всех групп."""
    logger.info("Listing all groups")
    
    # Инициализируем хранилище знаний
    knowledge_store = get_knowledge_store()
    
    # Получаем все группы
    if hasattr(knowledge_store, 'list_group_ids'):
        group_ids = await knowledge_store.list_group_ids()
    else:
        all_units = await knowledge_store.list_all()
        group_ids = set(u.group_id for u in all_units if u.group_id)
    
    logger.info(f"Found {len(group_ids)} groups:")
    for group_id in sorted(group_ids):
        # Получаем количество юнитов в группе
        if hasattr(knowledge_store, 'list_by_group'):
            units = await knowledge_store.list_by_group(group_id)
        else:
            all_units = await knowledge_store.list_all()
            units = [u for u in all_units if u.group_id == group_id]
        
        # Проверяем наличие сегментов
        segments = await knowledge_store.list_segments_by_group(group_id)
        
        status = "✓" if segments else "✗"
        logger.info(f"  {status} {group_id} ({len(units)} units, {len(segments)} segments)")


async def list_segments(group_id: Optional[str] = None):
    """Выводит список сегментов."""
    # Инициализируем хранилище знаний
    knowledge_store = get_knowledge_store()
    
    if group_id:
        logger.info(f"Listing segments for group: {group_id}")
        segments = await knowledge_store.list_segments_by_group(group_id)
    else:
        logger.info("Listing all segments")
        # Получаем все группы и их сегменты
        segments = []
        if hasattr(knowledge_store, 'list_group_ids'):
            group_ids = await knowledge_store.list_group_ids()
        else:
            all_units = await knowledge_store.list_all()
            group_ids = set(u.group_id for u in all_units if u.group_id)
        
        for gid in group_ids:
            group_segments = await knowledge_store.list_segments_by_group(gid)
            segments.extend(group_segments)
    
    logger.info(f"Found {len(segments)} segments:")
    for segment in segments:
        logger.info(f"\n  Segment: {segment.title}")
        logger.info(f"  Group: {segment.group_id}")
        logger.info(f"  Summary: {segment.summary[:200]}...")
        logger.info(f"  Units: {len(segment.raw_unit_ids)}")
        logger.info(f"  Entities: {', '.join(segment.entities[:5])}")
        if len(segment.entities) > 5:
            logger.info(f"           ... and {len(segment.entities) - 5} more")


def main():
    parser = argparse.ArgumentParser(
        description="Утилита для сегментации нормализованных юнитов"
    )
    
    # Подкоманды
    subparsers = parser.add_subparsers(dest="command", help="Доступные команды")
    
    # segment-group - сегментация одной группы
    segment_group_parser = subparsers.add_parser(
        "segment-group",
        help="Сегментировать конкретную группу"
    )
    segment_group_parser.add_argument(
        "group_id",
        help="ID группы для сегментации"
    )
    segment_group_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Только показать, что будет сделано, без выполнения"
    )
    
    # segment-all - сегментация всех групп
    segment_all_parser = subparsers.add_parser(
        "segment-all",
        help="Сегментировать все группы"
    )
    segment_all_parser.add_argument(
        "--dry-run",
        action="store_true",
        help="Только показать список групп, без выполнения"
    )
    
    # list-groups - список групп
    list_groups_parser = subparsers.add_parser(
        "list-groups",
        help="Показать список всех групп"
    )
    
    # list-segments - список сегментов
    list_segments_parser = subparsers.add_parser(
        "list-segments",
        help="Показать список сегментов"
    )
    list_segments_parser.add_argument(
        "group_id",
        nargs="?",
        help="ID группы для фильтрации (опционально)"
    )
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    # Регистрируем провайдеры сегментации
    logger.info("Registering segmentation providers...")
    register_segmentation_providers()
    
    # Регистрируем провайдеры кластеризации
    logger.info("Registering clustering providers...")
    from mindbank_poc.core.providers.clustering import register_clustering_providers
    register_clustering_providers()
    
    # Выполняем команду
    if args.command == "segment-group":
        asyncio.run(segment_group(args.group_id, args.dry_run))
    elif args.command == "segment-all":
        asyncio.run(segment_all(args.dry_run))
    elif args.command == "list-groups":
        asyncio.run(list_groups())
    elif args.command == "list-segments":
        asyncio.run(list_segments(args.group_id))
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()
