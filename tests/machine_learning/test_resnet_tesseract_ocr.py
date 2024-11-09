from pathlib import Path

from PIL import Image

from photos.machine_learning.ocr.ResnetTesseractOCR import ResnetTesseractOCR


def test_resnet_tesseract_ocr(tests_folder: Path) -> None:
    image = Image.open(tests_folder / "assets/ocr.jpg")
    ocr = ResnetTesseractOCR()
    has_text = ocr.has_legible_text(image)
    assert has_text

    extracted_text = ocr.get_text(image)
    assert "SPAGHETTI" in extracted_text.upper()