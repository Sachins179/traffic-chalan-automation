"""
Traffic Chalan Automation — Entry Point
========================================
Run:
    python main.py <path_to_image>

Example:
    python main.py data/input/test3.jpg
"""
import sys

from src.pipeline.runner import run_pipeline
from src.utils.config_loader import config
from src.utils.logger import get_logger

log = get_logger("main")


def main() -> int:
    if len(sys.argv) < 2:
        log.error("Usage: python main.py <path_to_image>")
        return 1

    image_path = sys.argv[1]
    log.info("Project: %s v%s", config.app["name"], config.app["version"])
    log.info("Model: %s", config.env["GROQ_VISION_MODEL"])

    result = run_pipeline(image_path)

    if result is None:
        log.info("Pipeline finished: no violation detected.")
        return 0

    print("\n" + "=" * 60)
    print("RESULT")
    print("=" * 60)
    print(f"Violations  : {', '.join(result['violations'])}")
    print(f"Fine breakdown:")
    for violation, amount in result["fine_breakdown"].items():
        print(f"  • {violation}: Rs. {amount}")
    print(f"  ---------------------")
    print(f"  TOTAL: Rs. {result['total_fine']}")
    print(f"Plate       : {result.get('plate_number', '-')}")
    if result.get("owner"):
        print(f"Owner       : {result['owner']['name']}")
        print(f"Mobile      : {result['owner']['mobile']}")
    else:
        print("Owner       : NOT FOUND")
    if result.get("pdf_path"):
        print(f"PDF         : {result['pdf_path']}")
    if result.get("whatsapp_link"):
        print(f"WhatsApp    : {result['whatsapp_link'][:80]}...")
    print("=" * 60)

    return 0


if __name__ == "__main__":
    sys.exit(main())