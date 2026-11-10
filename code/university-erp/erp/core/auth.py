"""Login, logout and role checks. Passwords are hashed; roles can be scoped (e.g. hod for department CSC)."""

import functools

from flask import Blueprint, abort, flash, g, redirect, render_template, request, session, url_for
from werkzeug.security import check_password_hash, generate_password_hash

from .db import get_db

ROLES = [
    "student",
    "lecturer",
    "hod",
    "dean",
    "exams_officer",
    "registrar",
    "bursar",
    "admissions_officer",
    "hr_officer",
    "payroll_officer",
    "librarian",
    "hostel_officer",
    "timetable_officer",
    "admin",
]

bp = Blueprint("auth", __name__)


def hash_password(pw: str) -> str:
    return generate_password_hash(pw)


@bp.before_app_request
def load_user():
    uid = session.get("user_id")
    g.user = get_db().execute("SELECT * FROM users WHERE id = ? AND active = 1", (uid,)).fetchone() if uid else None


@bp.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        u = (
            get_db()
            .execute("SELECT * FROM users WHERE username = ? AND active = 1", (request.form.get("username", ""),))
            .fetchone()
        )
        if u and check_password_hash(u["password_hash"], request.form.get("password", "")):
            session.clear()
            session["user_id"] = u["id"]
            return redirect(url_for("core.home"))
        flash("Wrong username or password.")
    return render_template("login.html")


@bp.route("/logout", methods=["POST"])
def logout():
    session.clear()
    return redirect(url_for("auth.login"))


def login_required(view):
    @functools.wraps(view)
    def wrapped(*args, **kwargs):
        if g.user is None:
            return redirect(url_for("auth.login"))
        return view(*args, **kwargs)

    return wrapped


def require_role(*roles: str, scope_arg: str | None = None):
    """Decorator: the user must hold one of `roles`, globally or for the scope named by the URL argument `scope_arg`."""

    def deco(view):
        @functools.wraps(view)
        def wrapped(*args, **kwargs):
            if g.user is None:
                return redirect(url_for("auth.login"))
            scope = kwargs.get(scope_arg, "*") if scope_arg else "*"
            marks = ",".join("?" * len(roles))  # placeholders only; every value is bound below
            q = f"SELECT 1 FROM user_roles WHERE user_id = ? AND role IN ({marks}) AND scope IN ('*', ?)"  # noqa: S608
            if not get_db().execute(q, (g.user["id"], *roles, scope)).fetchone():
                abort(403)
            return view(*args, **kwargs)

        return wrapped

    return deco
