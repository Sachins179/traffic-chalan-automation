"""
PostgreSQL connection factories.

Two separate databases:
  - chalan_db : violations + chalan_log
  - user_db   : users
"""
from contextlib import contextmanager
from typing import Iterator

import os
import psycopg2
import psycopg2.extras

from src.utils.config_loader import config


def _connect(dbname: str):
    """Create a raw PostgreSQL connection."""
    env = config.env
    return psycopg2.connect(
        host=env["DB_HOST"],
        port=env["DB_PORT"],
        dbname=dbname,
        user=env["DB_USER"],
        password=env["DB_PASSWORD"],
        sslmode=os.getenv("DB_SSLMODE", "prefer"),
        connect_timeout=10,
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


@contextmanager
def chalan_conn() -> Iterator:
    """Context-managed connection to chalan_db."""
    conn = _connect(config.env["CHALAN_DB_NAME"])
    try:
        yield conn
    finally:
        conn.close()


@contextmanager
def user_conn() -> Iterator:
    """Context-managed connection to user_db."""
    conn = _connect(config.env["USER_DB_NAME"])
    try:
        yield conn
    finally:
        conn.close()