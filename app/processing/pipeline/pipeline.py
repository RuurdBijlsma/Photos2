import os
import uuid
from dataclasses import dataclass
from pathlib import Path

import PIL.Image
import pillow_avif  # noqa: F401

from app.config.app_config import app_config
from app.data.database.db_utils import rel_path
from app.data.interfaces.image_data import WeatherData, ImageData
from app.data.interfaces.visual_data import ObjectsData, VisualData
from app.processing.pipeline.base_module import ImageModule, VisualModule
from app.processing.pipeline.frame_based.caption_module import CaptionModule
from app.processing.pipeline.frame_based.classification_module import \
    ClassificationModule
from app.processing.pipeline.frame_based.embedding_module import EmbeddingModule
from app.processing.pipeline.frame_based.face_detection_module import FacesModule
from app.processing.pipeline.frame_based.object_detection_module import ObjectsModule
from app.processing.pipeline.frame_based.ocr_module import OCRModule
from app.processing.pipeline.frame_based.summary_module import SummaryModule
from app.processing.pipeline.image_based.data_url_module import DataUrlModule
from app.processing.pipeline.image_based.exif_module import ExifModule
from app.processing.pipeline.image_based.gps_module import GpsModule
from app.processing.pipeline.image_based.time_module import TimeModule
from app.processing.pipeline.image_based.weather_module import WeatherModule
from app.processing.processing.process_utils import pil_to_jpeg, \
    ImageThumbnails

max_thumb_height = max(app_config.thumbnail_heights)


@dataclass
class ScannableFrame:
    image_path: Path
    snapshot_time_ms: int = 0


image_pipeline: list[ImageModule] = [
    ExifModule(),
    DataUrlModule(),
    GpsModule(),
    TimeModule(),
    WeatherModule(),
]

visual_pipeline: list[VisualModule] = [
    EmbeddingModule(),
    ClassificationModule(),
    OCRModule(),
    FacesModule(),
    SummaryModule(),
    CaptionModule(),
    ObjectsModule(),
]


def run_metadata_pipeline(
    image_path: Path,
    image_hash: str,
    thumbnails: ImageThumbnails
) -> tuple[WeatherData, list[ObjectsData]]:
    print(f"{image_path.name.ljust(35)}")
    image_data = ImageData(
        id=uuid.uuid4().hex,
        relative_path=rel_path(image_path),
        filename=os.path.basename(image_path),
        hash=image_hash,
    )

    for image_module in image_pipeline:
        image_data = image_module.run(image_data)
    assert isinstance(image_data, WeatherData)

    visual_datas: list[ObjectsData] = []
    for frame_percentage, frame_image_path in thumbnails.frames.items():
        with PIL.Image.open(frame_image_path) as frame_image:
            jpeg_image = pil_to_jpeg(frame_image)

        visual_data = VisualData(frame_percentage=frame_percentage)
        for visual_module in visual_pipeline:
            visual_data = visual_module.run(visual_data, jpeg_image)
        assert isinstance(visual_data, ObjectsData)
        visual_datas.append(visual_data)
        jpeg_image.close()

    return image_data, visual_datas
