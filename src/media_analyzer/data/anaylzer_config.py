from dataclasses import dataclass, field

from media_analyzer.data.enums.config_types import CaptionerProvider, LLMProvider
from media_analyzer.machine_learning.caption.captioner_protocol import CaptionerProtocol
from media_analyzer.machine_learning.classifier.base_classifier import BaseClassifier
from media_analyzer.machine_learning.embedding.embedder_protocol import EmbedderProtocol
from media_analyzer.machine_learning.ocr.ocr_protocol import OCRProtocol
from media_analyzer.machine_learning.visual_llm.base_visual_llm import BaseVisualLLM


@dataclass
class AnalyzerSettings:
    """Configuration settings for the media analysis pipeline.

    This class contains various options for configuring how photo and video files
    are analyzed, including language settings for OCR, the selection of providers
    for captions and LLMs, and thresholds for different detection modules.

    Attributes:
        media_languages: The languages used for OCR.
        captions_provider: The provider to be used for generating captions.
        llm_provider: The provider for the large language model (LLM),
            which can be used for summaries and captions.
        enable_text_summary: Flag to enable or disable image summarization, uses LLM so is slow.
        enable_document_summary: Flag to enable or disable document summaries, uses LLM so is slow.
        document_detection_threshold: Threshold for detecting documents in images [0-100].
        face_detection_threshold: Threshold for face detection [0-1].
        enabled_file_modules: The set of modules used for file-based analysis.
        enabled_visual_modules: The set of modules for visual analysis.
    """

    media_languages: tuple[str, ...] = ("nld", "eng")
    captions_provider: CaptionerProvider = CaptionerProvider.BLIP
    llm_provider: LLMProvider = LLMProvider.MINICPM
    enable_text_summary: bool = False
    enable_document_summary: bool = False
    document_detection_threshold: int = 65
    face_detection_threshold: float = 0.7
    enabled_file_modules: set[str] = field(
        default_factory=lambda: {
            "DataUrlModule",
            "ExifModule",
            "GpsModule",
            "TimeModule",
            "WeatherModule",
        }
    )
    enabled_visual_modules: set[str] = field(
        default_factory=lambda: {
            "CaptionModule",
            "ClassificationModule",
            "EmbeddingModule",
            "FacesModule",
            "ObjectsModule",
            "OCRModule",
            "QualityDetectionModule",
            "SummaryModule",
        }
    )


@dataclass
class FullAnalyzerConfig:
    """A configuration class for the full analyzer.

    Attributes:
        llm: The language model.
        captioner: The captioning model.
        ocr: The OCR implementation.
        classifier: The classifier.
        embedder: The embedder implementation.
        settings: The analyzer settings.
    """

    llm: BaseVisualLLM
    captioner: CaptionerProtocol
    ocr: OCRProtocol
    classifier: BaseClassifier
    embedder: EmbedderProtocol
    settings: AnalyzerSettings
