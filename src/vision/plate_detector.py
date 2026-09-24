"""
Number plate localization.

Primary  : Canny edge detection + contour analysis
Fallback : Haar Cascade (haarcascade_russian_plate_number.xml)
"""
from pathlib import Path

import cv2
import numpy as np

from src.utils.config_loader import config
from src.utils.logger import get_logger
from src.vision.image_utils import load_image, save_image

log = get_logger("vision.plate")


def _contour_crop(image: np.ndarray) -> np.ndarray | None:
    """Detect plate via Canny edge + contour analysis."""
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    gray = cv2.bilateralFilter(gray, 11, 17, 17)
    edged = cv2.Canny(gray, 30, 200)

    contours, _ = cv2.findContours(
        edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE
    )
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:15]

    pd_config = config.plate_detection

    for contour in contours:
        peri = cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, 0.018 * peri, True)
        if len(approx) != 4:
            continue

        x, y, w, h = cv2.boundingRect(approx)
        if w < pd_config["min_width"] or h < pd_config["min_height"]:
            continue

        ratio = w / h
        if pd_config["aspect_ratio_min"] <= ratio <= pd_config["aspect_ratio_max"]:
            return image[y:y + h, x:x + w]
    return None


def _haar_crop(image: np.ndarray) -> np.ndarray | None:
    """Detect plate via Haar Cascade."""
    cascade_path = config.abs_path("plate_cascade")
    cascade = cv2.CascadeClassifier(str(cascade_path))
    if cascade.empty():
        log.error("Haar cascade file could not be loaded: %s", cascade_path)
        return None

    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    plates = cascade.detectMultiScale(
        gray,
        scaleFactor=1.05,
        minNeighbors=3,
        minSize=(60, 20),
    )
    if len(plates) == 0:
        return None

    x, y, w, h = max(plates, key=lambda p: p[2] * p[3])
    return image[y:y + h, x:x + w]


def detect_number_plate(image_path: str) -> str | None:
    """
    Locate and crop the number plate from an image.

    Args:
        image_path: Path to the input image.

    Returns:
        Path to the saved plate crop, or None if detection fails.
    """
    image = load_image(image_path)
    if image is None:
        log.error("Could not read image: %s", image_path)
        return None

    crop = _contour_crop(image)
    if crop is None:
        log.info("Contour method failed - trying Haar cascade...")
        crop = _haar_crop(image)

    if crop is None:
        log.warning("No plate found in %s", image_path)
        return None

    stem = Path(image_path).stem
    output_path = config.abs_path("output_dir") / f"{stem}_plate.jpg"
    save_image(crop, output_path)
    log.info("Plate crop saved: %s", output_path)
    return str(output_path)