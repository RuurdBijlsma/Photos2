from typing import Protocol

from PIL.Image import Image

from media_analyzer.data.interfaces.ml_types import OCRBox


class OCRProtocol(Protocol):
    def has_legible_text(self, image: Image) -> bool:
        """Check if an image has legible text."""

    def get_text(self, image: Image, languages: tuple[str, ...]) -> str:
        """Extract text from an image using OCR."""

    def get_boxes(self, image: Image, languages: tuple[str, ...]) -> list[OCRBox]:
        """Get bounding boxes of text."""
