from dataclasses import dataclass
from pathlib import Path

from media_analyzer.data.enums.config_types import CaptionerProvider, LLMProvider
from media_analyzer.machine_learning.caption.captioner_protocol import CaptionerProtocol
from media_analyzer.machine_learning.classifier.base_classifier import BaseClassifier
from media_analyzer.machine_learning.embedding.embedder_protocol import EmbedderProtocol
from media_analyzer.machine_learning.ocr.ocr_protocol import OCRProtocol
from media_analyzer.machine_learning.visual_llm.base_visual_llm import BaseVisualLLM


@dataclass
class AnalyzerSettings:
    media_languages: tuple[str, ...] = ("nld", "eng")
    captions_provider: CaptionerProvider = CaptionerProvider.BLIP
    llm_provider: LLMProvider = LLMProvider.MINICPM
    enable_text_summary: bool = False
    enable_document_summary: bool = False
    document_detection_threshold: int = 65
    face_detection_threshold: float = 0.7

    images_dir: Path = Path("media/images")
    thumbnails_dir: Path = Path("media/thumbnails")
    thumbnail_heights: tuple[int, ...] = (200, 250, 300, 400, 500, 750, 1080)
    video_screenshot_percentages: tuple[int, ...] = (1, 33, 66, 95)
    web_video_height_and_quality: tuple[tuple[int, int], ...] = ((360, 40), (1080, 35))
    photo_suffixes: tuple[str, ...] = (
        ".png",
        ".jpg",
        ".jpeg",
        ".bmp",
        ".gif",
        ".tiff",
        ".webp",
    )
    video_suffixes: tuple[str, ...] = (".mp4", ".mkv", ".webm")

    @property
    def image_suffixes(self) -> tuple[str, ...]:
        return self.photo_suffixes + self.video_suffixes

@dataclass
class FullAnalyzerConfig:
    llm: BaseVisualLLM
    captioner: CaptionerProtocol
    ocr: OCRProtocol
    classifier: BaseClassifier
    embedder: EmbedderProtocol
    settings: AnalyzerSettings