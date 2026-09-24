"""
Number plate OCR using Groq's vision LLM.
"""
import re

from src.llm.client import get_client
from src.utils.config_loader import config
from src.utils.logger import get_logger
from src.vision.image_utils import encode_image_base64

log = get_logger("llm.plate")

_PROMPT = (
    "You are an ANPR (Automatic Number Plate Recognition) system.\n"
    "Look at the image and find the vehicle's number plate.\n"
    "Read the registration number carefully.\n\n"
    "IMPORTANT:\n"
    "- IGNORE any text like 'SPEED: 78 km/h', 'OVERSPEEDING', "
    "or any violation labels.\n"
    "- Focus ONLY on the physical number plate mounted on the vehicle "
    "(usually white with black text).\n"
    "- Indian plates: 2 letters + 2 digits + 1-2 letters + 4 digits "
    "(e.g., TS09EA4321, MH01AB1234, AP12AB1234).\n\n"
    "Return ONLY the plate text. No spaces, no quotes, no explanation.\n"
    "If you cannot read the plate, return: UNREADABLE"
)


def _strip_reasoning(text: str) -> str:
    """Remove <think>...</think> blocks emitted by reasoning models."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return text.strip()


def extract_plate_number(image_path: str) -> str:
    """
    Extract the vehicle plate number from an image.

    Args:
        image_path: Path to the image (full or cropped plate).

    Returns:
        Uppercase alphanumeric plate text, or "" on failure.
    """
    client = get_client()
    if client is None:
        return ""

    b64 = encode_image_base64(image_path)

    try:
        response = client.chat.completions.create(
            model=config.env["GROQ_VISION_MODEL"],
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": _PROMPT},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                    },
                ],
            }],
            temperature=config.llm["temperature"],
            max_tokens=config.llm["max_tokens_plate"],
        )
    except Exception as exc:
        log.exception("Groq API error: %s", exc)
        return ""

    raw = response.choices[0].message.content or ""
    cleaned = _strip_reasoning(raw)
    plate = re.sub(r"[^A-Za-z0-9]", "", cleaned).upper()

    log.info("Plate OCR result: %s", plate or "<empty>")
    return plate