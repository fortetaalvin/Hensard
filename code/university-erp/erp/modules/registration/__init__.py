"""Course Registration: the class module, built together in the weekly labs.

Rules (also in AGENTS.md): use erp.core.contracts for anything about students, staff, roles, sessions and auditing;
never import another module; talk to other modules only through events listed in docs/integration-contracts.md.
"""

from flask import Blueprint, render_template

from erp.core.auth import login_required

bp = Blueprint("registration", __name__, template_folder="templates")


@bp.route("/")
@login_required
def index():
    return render_template("registration/index.html")


def register_events(app):
    """Subscribe to other modules' events here, e.g. contracts.subscribe("fees.cleared", on_cleared)."""
