from flask import Blueprint, current_app, g, render_template

from .auth import login_required
from .config import institution
from .db import get_db

bp = Blueprint("core", __name__, template_folder="templates")


@bp.route("/")
@login_required
def home():
    roles = [
        r["role"] + ("" if r["scope"] == "*" else f" ({r['scope']})")
        for r in get_db().execute("SELECT role, scope FROM user_roles WHERE user_id = ?", (g.user["id"],))
    ]
    return render_template("home.html", inst=institution(), roles=roles, modules=current_app.config["ERP_MODULES"])
