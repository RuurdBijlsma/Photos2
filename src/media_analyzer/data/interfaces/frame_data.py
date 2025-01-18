from dataclasses import dataclass
from pathlib import Path

from PIL.Image import Image

from media_analyzer.data.enums.classification.activity_type import ActivityType
from media_analyzer.data.enums.classification.animal_type import AnimalType
from media_analyzer.data.enums.classification.document_type import DocumentType
from media_analyzer.data.enums.classification.event_type import EventType
from media_analyzer.data.enums.classification.object_type import ObjectType
from media_analyzer.data.enums.classification.people_type import PeopleType
from media_analyzer.data.enums.classification.scene_type import SceneType
from media_analyzer.data.enums.classification.weather_condition import WeatherCondition
from media_analyzer.data.interfaces.ml_types import FaceBox, ObjectBox, OCRBox


@dataclass
class ClassificationData:
    """Classification data for a frame.

    Attributes:
        scene_type: The type of scene.
        people_type: The type of people in the scene.
        animal_type: The type of animal in the scene.
        document_type: The type of document in the scene.
        object_type: The type of object in the scene.
        activity_type: The type of activity in the scene.
        event_type: The type of event in the scene.
        weather_condition: The weather condition in the scene.
        is_outside: Whether the scene is outside.
        is_landscape: Whether the scene is a landscape.
        is_cityscape: Whether the scene is a cityscape.
        is_travel: Whether the scene is a travel scene.
    """

    scene_type: SceneType
    people_type: PeopleType | None
    animal_type: AnimalType | None
    document_type: DocumentType | None
    object_type: ObjectType | None
    activity_type: ActivityType | None
    event_type: EventType | None
    weather_condition: WeatherCondition | None
    is_outside: bool
    is_landscape: bool
    is_cityscape: bool
    is_travel: bool


@dataclass
class OCRData:
    """OCR data for a frame.

    Attributes:
        has_legible_text: Whether the text is legible.
        ocr_text: The OCR text.
        document_summary: The document summary.
        ocr_boxes: The OCR boxes.
    """

    has_legible_text: bool
    ocr_text: str | None
    document_summary: str | None
    ocr_boxes: list[OCRBox]


@dataclass
class MeasuredQualityData:
    """Measured quality data for a frame.

    Attributes:
        measured_sharpness: The measured sharpness.
        measured_noise: The measured noise.
        measured_brightness: The measured brightness.
        measured_contrast: The measured contrast.
        measured_clipping: The measured clipping.
        measured_dynamic_range: The measured dynamic range.
        quality_score: The quality score.
    """

    measured_sharpness: float
    measured_noise: int
    measured_brightness: float
    measured_contrast: float
    measured_clipping: float
    measured_dynamic_range: float
    quality_score: float


@dataclass
class FrameData:
    """Data for a frame.

    Attributes:
        index: The frame index.
        path: The frame path.
        image: The frame image.
        ocr: The OCR data.
        embedding: The embedding data.
        faces: The face boxes.
        summary: The frame summary.
        caption: The frame caption.
        objects: The object boxes.
        classification: The classification data.
        measured_quality: The measured quality data.
    """

    index: int
    path: Path
    image: Image
    ocr: OCRData | None = None
    embedding: list[float] | None = None
    faces: list[FaceBox] | None = None
    summary: str | None = None
    caption: str | None = None
    objects: list[ObjectBox] | None = None
    classification: ClassificationData | None = None
    measured_quality: MeasuredQualityData | None = None