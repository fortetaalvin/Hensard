"""MODULE_NAME module. Copy this folder to erp/modules/<your_module>/ and replace MODULE_NAME everywhere.

Rules (also in AGENTS.md): use erp.core.contracts for anything about students, staff, roles, sessions and auditing;
never import another module; talk to other modules only through events listed in docs/integration-contracts.md.
"""

from flask import Blueprint, render_template

from erp.core.auth import login_required

bp = Blueprint("MODULE_NAME", __name__, template_folder="templates")


@bp.route("/")
@login_required
def index():
    return render_template("MODULE_NAME/index.html")


def register_events(app):
    """Subscribe to other modules' events here, e.g. contracts.subscribe("fees.cleared", on_cleared)."""
