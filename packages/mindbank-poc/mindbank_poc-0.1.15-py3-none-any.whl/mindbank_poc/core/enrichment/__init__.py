"""
Модуль обогащения данных.
"""
from .models import SegmentModel, SegmentExtractionResult
from .segmentation_service import SegmentationService
from .segment_utils import (
    merge_overlaps,
    merge_contiguous,
    validate_segments,
    crop_text,
)

__all__ = [
    "SegmentModel",
    "SegmentExtractionResult",
    "SegmentationService",
    "merge_overlaps",
    "merge_contiguous",
    "validate_segments",
    "crop_text",
]


def __getattr__(name):
    """Lazy loading for SegmentationService to avoid circular imports."""
    if name == "SegmentationService":
        from .segmentation_service import SegmentationService
        return SegmentationService
    raise AttributeError(f"module {__name__} has no attribute {name}")
