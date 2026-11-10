"""Tamper-evident audit log. Every significant action (grade change, payment, approval) is recorded here."""

import datetime
import hashlib
import json
import sqlite3

GENESIS = "0" * 64


def _digest(prev_hash: str, at: str, actor: str, action: str, entity: str, details: str) -> str:
    payload = "|".join([prev_hash, at, actor, action, entity, details])
    return hashlib.sha256(payload.encode("utf-8")).hexdigest()


def record(con: sqlite3.Connection, actor: str, action: str, entity: str, details: dict | None = None) -> str:
    """Append one event and return its hash. Commit is the caller's responsibility (same transaction as the change)."""
    row = con.execute("SELECT hash FROM audit_log ORDER BY id DESC LIMIT 1").fetchone()
    prev = row["hash"] if row else GENESIS
    at = datetime.datetime.now(datetime.UTC).isoformat(timespec="seconds")
    det = json.dumps(details or {}, sort_keys=True)
    h = _digest(prev, at, actor, action, entity, det)
    con.execute(
        "INSERT INTO audit_log (at, actor, action, entity, details, prev_hash, hash) VALUES (?, ?, ?, ?, ?, ?, ?)",
        (at, actor, action, entity, det, prev, h),
    )
    return h


def verify(con: sqlite3.Connection) -> tuple[bool, int | None]:
    """Recompute the chain. Returns (True, None) if intact, else (False, id of the first bad row)."""
    prev = GENESIS
    for r in con.execute("SELECT * FROM audit_log ORDER BY id"):
        expected = _digest(prev, r["at"], r["actor"], r["action"], r["entity"], r["details"])
        if r["prev_hash"] != prev or r["hash"] != expected:
            return False, r["id"]
        prev = r["hash"]
    return True, None
