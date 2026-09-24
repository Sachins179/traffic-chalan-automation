"""
Config loader.
Reads config.yaml and .env, provides a single source of truth.
"""
import os
from pathlib import Path
from typing import Any

import yaml
from dotenv import load_dotenv

# Load .env from project root
BASE_DIR = Path(__file__).resolve().parent.parent.parent
load_dotenv(BASE_DIR / ".env")


class Config:
    """Central configuration object."""

    def __init__(self, config_path: Path | None = None) -> None:
        self.base_dir = BASE_DIR
        path = config_path or (BASE_DIR / "config.yaml")
        with open(path, "r", encoding="utf-8") as f:
            self._data: dict[str, Any] = yaml.safe_load(f)

        # Merge environment variables (secrets)
        self._env = {
            "DB_HOST": os.getenv("DB_HOST", self._data["database"]["host"]),
            "DB_PORT": int(os.getenv("DB_PORT", self._data["database"]["port"])),
            "CHALAN_DB_NAME": os.getenv(
                "CHALAN_DB_NAME", self._data["database"]["chalan_db"]
            ),
            "USER_DB_NAME": os.getenv(
                "USER_DB_NAME", self._data["database"]["user_db"]
            ),
            "DB_USER": os.getenv("DB_USER", self._data["database"]["user"]),
            "DB_PASSWORD": os.getenv("DB_PASSWORD", ""),
            "GROQ_API_KEY": os.getenv("GROQ_API_KEY", ""),
            "GROQ_VISION_MODEL": os.getenv(
                "GROQ_VISION_MODEL", self._data["llm"]["vision_model"]
            ),
        }

    # ------------------------------------------------------------------
    # Shortcut properties
    # ------------------------------------------------------------------
    @property
    def app(self) -> dict:
        return self._data["app"]

    @property
    def paths(self) -> dict:
        return self._data["paths"]

    @property
    def database(self) -> dict:
        return self._data["database"]

    @property
    def llm(self) -> dict:
        return self._data["llm"]

    @property
    def plate_detection(self) -> dict:
        return self._data["plate_detection"]

    @property
    def violations(self) -> dict:
        return self._data["violations"]

    @property
    def env(self) -> dict:
        return self._env

    # ------------------------------------------------------------------
    # Path helpers (absolute)
    # ------------------------------------------------------------------
    def abs_path(self, key: str) -> Path:
        """Return absolute path for a key under `paths`."""
        return self.base_dir / self.paths[key]


# Singleton
config = Config()