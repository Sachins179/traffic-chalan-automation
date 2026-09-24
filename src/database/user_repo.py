"""
Repository for user_db — users table + fuzzy fallback for OCR errors.
"""
from difflib import SequenceMatcher
from typing import Optional

from src.database.connection import user_conn
from src.utils.config_loader import config
from src.utils.logger import get_logger

log = get_logger("db.user")


def get_user_by_plate(plate_number: str) -> Optional[dict]:
    """Exact (case-insensitive) lookup by vehicle_number."""
    with user_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, vehicle_registration_number, "
            "       vehicle_type, vehicle_number, mobile "
            "FROM users WHERE LOWER(vehicle_number) = LOWER(%s);",
            (plate_number,),
        )
        return cur.fetchone()


def get_user_by_plate_fuzzy(
    plate_number: str,
    threshold: Optional[float] = None,
) -> tuple[Optional[dict], float]:
    """
    Fuzzy match — used when LLM OCR misreads characters.
    Returns (row, score) where score is in [0, 1].
    """
    if threshold is None:
        threshold = config.plate_detection["fuzzy_threshold"]

    with user_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT id, name, vehicle_registration_number, "
            "       vehicle_type, vehicle_number, mobile FROM users;"
        )
        rows = cur.fetchall()

    if not rows:
        return None, 0.0

    target = plate_number.lower()
    best_row, best_score = None, 0.0

    for row in rows:
        score = SequenceMatcher(
            None, target, row["vehicle_number"].lower()
        ).ratio()
        if score > best_score:
            best_row, best_score = row, score

    if best_score >= threshold:
        return best_row, best_score
    return None, best_score