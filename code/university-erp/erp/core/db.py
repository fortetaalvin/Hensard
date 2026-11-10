"""SQLite connection per request (ERP_DB sets the path). Swap for PostgreSQL in an ADR if your team needs it."""

import os
import pathlib
import sqlite3

from flask import current_app, g

CORE_SCHEMA = pathlib.Path(__file__).with_name("schema.sql")
MODULES_DIR = pathlib.Path(__file__).resolve().parents[1] / "modules"


def connect(path: str) -> sqlite3.Connection:
    con = sqlite3.connect(path)
    con.row_factory = sqlite3.Row
    con.execute("PRAGMA foreign_keys = ON")
    return con


def get_db() -> sqlite3.Connection:
    if "db" not in g:
        g.db = connect(current_app.config["ERP_DB"])
    return g.db


def close_db(_exc=None) -> None:
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_schema(con: sqlite3.Connection, modules: list[str]) -> None:
    con.executescript(CORE_SCHEMA.read_text(encoding="utf-8"))
    for name in modules:
        schema = MODULES_DIR / name / "schema.sql"
        if schema.exists():
            con.executescript(schema.read_text(encoding="utf-8"))
    con.commit()


def default_path() -> str:
    return os.environ.get("ERP_DB", str(pathlib.Path.cwd() / "erp.db"))
