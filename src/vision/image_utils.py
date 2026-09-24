"""
Reusable image helpers.
"""
import base64
from pathlib import Path

import cv2
import numpy as np


def load_image(image_path: str | Path) -> np.ndarray | None:
    """
    Load an image via OpenCV.

    Args:
        image_path: Path to the image file.

    Returns:
        NumPy array (BGR) or None if loading fails.
    """
    path = Path(image_path)
    if not path.exists():
        return None
    return cv2.imread(str(path))


def save_image(image: np.ndarray, output_path: str | Path) -> bool:
    """
    Save an image, ensuring the parent directory exists.

    Args:
        image: NumPy array to save.
        output_path: Destination path.

    Returns:
        True on success, False otherwise.
    """
    path = Path(output_path)
    path.parent.mkdir(parents=True, exist_ok=True)
    return cv2.imwrite(str(path), image)


def encode_image_base64(image_path: str | Path) -> str:
    """
    Read an image file and return its base64-encoded string.

    Args:
        image_path: Path to the image file.

    Returns:
        Base64-encoded string.
    """
    with open(image_path, "rb") as f:
        return base64.b64encode(f.read()).decode("utf-8")