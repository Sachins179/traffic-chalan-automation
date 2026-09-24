"""
Central logger setup.
Import `get_logger(__name__)` in every module.
"""
import logging
import sys
from pathlib import Path

from src.utils.config_loader import config

_CONFIGURED = False


def _configure() -> None:
    global _CONFIGURED
    if _CONFIGURED:
        return

    log_dir = config.abs_path("data_dir").parent / "logs"
    log_dir.mkdir(parents=True, exist_ok=True)

    formatter = logging.Formatter(
        fmt="%(asctime)s | %(levelname)-7s | %(name)-25s | %(message)s",
        datefmt="%Y-%m-%d %H:%M:%S",
    )

    # Console handler
    console = logging.StreamHandler(sys.stdout)
    console.setFormatter(formatter)

    # File handler
    file_handler = logging.FileHandler(
        log_dir / "app.log", encoding="utf-8"
    )
    file_handler.setFormatter(formatter)

    root = logging.getLogger("tca")
    root.setLevel(config.app["log_level"])
    root.addHandler(console)
    root.addHandler(file_handler)
    root.propagate = False

    _CONFIGURED = True


def get_logger(name: str) -> logging.Logger:
    """Return a namespaced logger under 'tca'."""
    _configure()
    return logging.getLogger(f"tca.{name}")