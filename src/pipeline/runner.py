"""
End-to-end chalan pipeline.
Supports MULTIPLE violations per image.
"""
from pathlib import Path

from src.chalan.fine_calculator import calculate_total_fine
from src.chalan.pdf_generator import generate_chalan_pdf
from src.database import chalan_repo, user_repo
from src.llm.plate_reader import extract_plate_number
from src.llm.violation_detector import detect_violations
from src.notification.whatsapp_web import build_whatsapp_link
from src.utils.logger import get_logger
from src.vision.plate_detector import detect_number_plate

log = get_logger("pipeline")


def run_pipeline(image_path: str) -> dict | None:
    """
    Run the full chalan pipeline for an image.

    Args:
        image_path: Path to the traffic image.

    Returns:
        A dict with the result, or None if no violation was detected.
    """
    log.info("=" * 60)
    log.info("Processing image: %s", image_path)
    log.info("=" * 60)

    if not Path(image_path).exists():
        log.error("Image not found: %s", image_path)
        return None

    # ---------------- Step 1: Detect ALL violations ----------------
    log.info("[1/7] Detecting violations using Groq LLM...")
    violation_names = detect_violations(image_path)
    log.info("      -> Violations: %s", violation_names)

    if not violation_names:
        log.info("No violations detected. Stopping pipeline.")
        return None

    # ---------------- Step 2: Calculate total fine ----------------
    log.info("[2/7] Calculating total fine...")
    breakdown, total_fine = calculate_total_fine(violation_names)
    log.info("      -> Breakdown: %s", breakdown)
    log.info("      -> Total: Rs.%s", total_fine)

    if not breakdown:
        log.error("No valid fines found.")
        return None

    result: dict = {
        "image_path": image_path,
        "violations": violation_names,
        "fine_breakdown": breakdown,
        "total_fine": total_fine,
    }

    # ---------------- Step 3: Plate detection ----------------
    log.info("[3/7] Detecting number plate...")
    plate_crop_path = detect_number_plate(image_path)
    if plate_crop_path is None:
        log.warning("      -> Plate crop failed. Using full image for OCR.")
        plate_crop_path = image_path
    else:
        log.info("      -> Plate crop: %s", plate_crop_path)

    # ---------------- Step 4: Plate OCR with fallback ----------------
    log.info("[4/7] Extracting plate number using Groq LLM...")

    plate_number = ""
    if plate_crop_path != image_path:
        crop_plate = extract_plate_number(plate_crop_path)
        if crop_plate and crop_plate != "UNREADABLE":
            plate_number = crop_plate
            log.info("      -> Crop OCR succeeded: %s", plate_number)
        else:
            log.info(
                "      -> Crop OCR returned '%s'. Falling back to full image...",
                crop_plate or "<empty>",
            )

    if not plate_number:
        full_plate = extract_plate_number(image_path)
        if full_plate and full_plate != "UNREADABLE":
            plate_number = full_plate
            log.info("      -> Full image OCR succeeded: %s", plate_number)
        else:
            log.warning(
                "      -> Full image OCR also failed: %s",
                full_plate or "<empty>",
            )

    result["plate_number"] = plate_number
    log.info("      -> Plate: %s", plate_number or "<empty>")

    # ---------------- Step 5: Owner lookup ----------------
    log.info("[5/7] Looking up vehicle owner...")
    user_row = user_repo.get_user_by_plate(plate_number)
    fuzzy_matched = False

    if not user_row and plate_number:
        user_row, score = user_repo.get_user_by_plate_fuzzy(plate_number)
        if user_row:
            fuzzy_matched = True
            log.info(
                "      -> Fuzzy match: %s (%.0f%% similar)",
                user_row["vehicle_number"],
                score * 100,
            )

    if not user_row:
        log.warning("      -> No owner found for plate '%s'", plate_number)
        result["owner"] = None
        result["whatsapp_link"] = None
        return result

    result["owner"] = dict(user_row)
    log.info(
        "      -> Owner: %s | Mobile: %s",
        user_row["name"],
        user_row["mobile"],
    )

    display_plate = (
        user_row["vehicle_number"] if fuzzy_matched else plate_number
    )

    # ---------------- Step 6: Log + PDF ----------------
    log.info("[6/7] Logging chalan and generating PDF...")
    try:
        chalan_id = chalan_repo.log_chalan(
            plate_number=plate_number,
            violation_name=", ".join(violation_names),
            fine=total_fine,
            image_path=image_path,
            user_id=user_row["id"],
            whatsapp_status="PENDING",
        )
        result["chalan_id"] = chalan_id
    except Exception as exc:
        log.warning("      -> chalan_log insert failed: %s", exc)
        result["chalan_id"] = None

    pdf_path = generate_chalan_pdf(
        owner_name=user_row["name"],
        vehicle_number=display_plate,
        violation_names=violation_names,
        fine_breakdown=breakdown,
        total_fine=total_fine,
    )
    result["pdf_path"] = pdf_path
    log.info("      -> PDF: %s", pdf_path)

    # ---------------- Step 7: WhatsApp link ----------------
    log.info("[7/7] Building WhatsApp link...")
    wa_link = build_whatsapp_link(
        to_mobile=user_row["mobile"],
        name=user_row["name"],
        violation_names=violation_names,
        total_fine=total_fine,
        vehicle_number=display_plate,
    )
    result["whatsapp_link"] = wa_link
    log.info("      -> WhatsApp link ready (manual send).")

    log.info("=" * 60)
    log.info(
        "DONE | %s | Rs.%s | %s",
        violation_names, total_fine, display_plate,
    )
    log.info("=" * 60)

    return result