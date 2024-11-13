from typing import Protocol

from PIL.Image import Image

from data.interfaces.ml_types import FaceBox


class FacialRecognitionProtocol(Protocol):
    def get_faces(self, image: Image) -> list[FaceBox]: ...
