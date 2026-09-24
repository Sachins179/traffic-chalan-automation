"""
Violation classification using Groq's vision LLM.
Supports multiple violations per image.
"""
import re

from src.llm.client import get_client
from src.utils.config_loader import config
from src.utils.logger import get_logger
from src.vision.image_utils import encode_image_base64

log = get_logger("llm.violation")

_PROMPT_MULTI = (
    "You are a traffic violation detection assistant.\n"
    "Analyze this traffic image and identify ALL violations present.\n"
    "Possible violations: {violations}.\n\n"
    "If multiple violations are present, list them all.\n"
    "If no violation is visible, write: None\n\n"
    "Return ONLY the violation names, separated by commas.\n"
    "Example: No Helmet, Triple Ride\n"
    "No explanation, no extra text."
)


def _strip_reasoning(text: str) -> str:
    """Remove <think>...</think> blocks emitted by reasoning models."""
    text = re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL)
    text = re.sub(r"```.*?```", "", text, flags=re.DOTALL)
    return text.strip()


def detect_violations(image_path: str) -> list[str]:
    """
    Detect ALL traffic violations in an image.

    Args:
        image_path: Path to the input image.

    Returns:
        List of violation names (e.g., ["No Helmet", "Triple Ride"]).
        Empty list if none detected.
    """
    client = get_client()
    if client is None:
        return []

    violations = list(config.violations.keys())
    prompt = _PROMPT_MULTI.format(violations=", ".join(violations))

    b64 = encode_image_base64(image_path)

    try:
        response = client.chat.completions.create(
            model=config.env["GROQ_VISION_MODEL"],
            messages=[{
                "role": "user",
                "content": [
                    {"type": "text", "text": prompt},
                    {
                        "type": "image_url",
                        "image_url": {"url": f"data:image/jpeg;base64,{b64}"},
                    },
                ],
            }],
            temperature=config.llm["temperature"],
            max_tokens=config.llm["max_tokens_violation"],
        )
    except Exception as exc:
        log.exception("Groq API error: %s", exc)
        return []

    raw = response.choices[0].message.content or ""
    cleaned = _strip_reasoning(raw)
    log.info("Raw LLM response: %r", cleaned)

    if "none" in cleaned.lower():
        log.info("No violations detected.")
        return []

    detected = []
    for v in violations:
        if v.lower() in cleaned.lower():
            detected.append(v)

    log.info("Detected violations: %s", detected)
    return detected