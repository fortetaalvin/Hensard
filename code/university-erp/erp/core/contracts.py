"""The ONLY core functions modules may call. Changing a signature here needs an ADR and every team's review.

Modules must not query core tables directly or import another module's code; they use these functions and events.
"""

import sqlite3

from . import audit, events
from .config import grade_for, institution

__all__ = [
    "institution",
    "grade_for",
    "current_session",
    "get_student",
    "get_staff",
    "has_role",
    "record_event",
    "publish",
    "subscribe",
    "students_in_programme",
]

publish = events.publish
subscribe = events.subscribe


def current_session() -> str:
    return institution()["sessions"]["current"]


def get_student(con: sqlite3.Connection, matric_no: str) -> dict | None:
    r = con.execute(
        "SELECT s.matric_no, s.level, s.status, s.entry_session, u.full_name, u.email, p.name AS programme, "
        "p.department_code FROM students s JOIN users u ON u.id = s.user_id JOIN programmes p ON p.id = s.programme_id "
        "WHERE s.matric_no = ?",
        (matric_no,),
    ).fetchone()
    return dict(r) if r else None


def get_staff(con: sqlite3.Connection, staff_no: str) -> dict | None:
    r = con.execute(
        "SELECT st.staff_no, st.department_code, st.category, st.rank, u.full_name, u.email FROM staff st "
        "JOIN users u ON u.id = st.user_id WHERE st.staff_no = ?",
        (staff_no,),
    ).fetchone()
    return dict(r) if r else None


def students_in_programme(con: sqlite3.Connection, programme: str, level: int | None = None) -> list[dict]:
    sql = (
        "SELECT s.matric_no, s.level, u.full_name FROM students s JOIN programmes p ON p.id = s.programme_id "
        "JOIN users u ON u.id = s.user_id WHERE p.name = ?"
    )
    args: list = [programme]
    if level is not None:
        sql += " AND s.level = ?"
        args.append(level)
    return [dict(r) for r in con.execute(sql + " ORDER BY s.matric_no", args)]


def has_role(con: sqlite3.Connection, user_id: int, role: str, scope: str = "*") -> bool:
    """True if the user holds the role globally ('*') or for this scope (e.g. a department code)."""
    return (
        con.execute(
            "SELECT 1 FROM user_roles WHERE user_id = ? AND role = ? AND scope IN ('*', ?)", (user_id, role, scope)
        ).fetchone()
        is not None
    )


def record_event(con: sqlite3.Connection, actor: str, action: str, entity: str, details: dict | None = None) -> str:
    return audit.record(con, actor, action, entity, details)
