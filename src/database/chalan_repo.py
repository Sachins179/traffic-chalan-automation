"""
Repository for chalan_db — violations + chalan_log.
"""
from typing import Optional

from src.database.connection import chalan_conn
from src.utils.logger import get_logger

log = get_logger("db.chalan")


def get_fine(violation_name: str) -> Optional[dict]:
    """Return {'violation_name', 'fine'} for the given violation."""
    with chalan_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "SELECT violation_name, fine FROM violations "
            "WHERE LOWER(violation_name) = LOWER(%s);",
            (violation_name,),
        )
        return cur.fetchone()


def log_chalan(
    *,
    plate_number: str,
    violation_name: str,
    fine: int,
    image_path: str,
    user_id: Optional[int] = None,
    whatsapp_status: str = "PENDING",
) -> int:
    """Insert a chalan_log row and return its id."""
    with chalan_conn() as conn, conn.cursor() as cur:
        cur.execute(
            """
            INSERT INTO chalan_log
                (user_id, plate_number, violation_name, fine,
                 image_path, whatsapp_status)
            VALUES (%s, %s, %s, %s, %s, %s)
            RETURNING id;
            """,
            (user_id, plate_number, violation_name, fine,
             image_path, whatsapp_status),
        )
        chalan_id = cur.fetchone()["id"]
        conn.commit()
    log.info("Logged chalan #%s (%s, Rs.%s)", chalan_id, violation_name, fine)
    return chalan_id


def update_whatsapp_status(chalan_id: int, status: str) -> None:
    """Update WhatsApp delivery status for a chalan."""
    with chalan_conn() as conn, conn.cursor() as cur:
        cur.execute(
            "UPDATE chalan_log SET whatsapp_status = %s WHERE id = %s;",
            (status, chalan_id),
        )
        conn.commit()
    log.info("Chalan #%s WhatsApp status -> %s", chalan_id, status)