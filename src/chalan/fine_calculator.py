"""
Fine calculator.
Maps violations to fines and computes totals.
"""
from src.database.chalan_repo import get_fine
from src.utils.logger import get_logger

log = get_logger("chalan.fine")


def calculate_total_fine(violation_names: list[str]) -> tuple[dict, int]:
    """
    Calculate fines for multiple violations and their total.

    Args:
        violation_names: List of violation names.

    Returns:
        Tuple of (breakdown_dict, total_fine).
        breakdown_dict = {violation_name: fine}
    """
    breakdown: dict[str, int] = {}
    total = 0

    for name in violation_names:
        row = get_fine(name)
        if row:
            breakdown[name] = row["fine"]
            total += row["fine"]
        else:
            log.warning("Violation not found in DB: %s", name)

    log.info("Fine breakdown: %s | Total: Rs.%s", breakdown, total)
    return breakdown, total