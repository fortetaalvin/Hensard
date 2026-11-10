"""Application factory. Enabled modules (institution.yaml `modules:`) are imported and their blueprints registered."""

import importlib
import os
import secrets

import click
from flask import Flask

from .core import auth, views
from .core.config import institution
from .core.db import close_db, connect, default_path, init_schema


def create_app(test_config: dict | None = None) -> Flask:
    app = Flask(__name__, template_folder="core/templates")
    app.config.update(
        SECRET_KEY=os.environ.get("ERP_SECRET_KEY") or secrets.token_hex(32),
        ERP_DB=default_path(),
        ERP_MODULES=list(institution().get("modules", [])),
    )
    if test_config:
        app.config.update(test_config)
    app.teardown_appcontext(close_db)
    app.register_blueprint(auth.bp)
    app.register_blueprint(views.bp)
    for name in app.config["ERP_MODULES"]:
        mod = importlib.import_module(f"erp.modules.{name}")
        app.register_blueprint(mod.bp, url_prefix=f"/{name}")
        if hasattr(mod, "register_events"):
            mod.register_events(app)

    @app.context_processor
    def inject_inst():
        return {"inst": institution()}

    @app.cli.command("init-db")
    def init_db_cmd():
        """Create core and module tables."""
        con = connect(app.config["ERP_DB"])
        init_schema(con, app.config["ERP_MODULES"])
        click.echo(f"Initialised {app.config['ERP_DB']}")

    @app.cli.command("seed")
    @click.option("--students", default=20, help="Synthetic students per programme")
    def seed_cmd(students):
        """Load the institution structure and synthetic people (development only)."""
        from .core.seed import DEV_PASSWORD, seed

        con = connect(app.config["ERP_DB"])
        init_schema(con, app.config["ERP_MODULES"])
        counts = seed(con, students)
        click.echo(f"Seeded {counts}. Dev password for every account: {DEV_PASSWORD}")

    @app.cli.command("verify-audit")
    def verify_audit_cmd():
        """Check the audit log's hash chain."""
        from .core.audit import verify

        ok, bad = verify(connect(app.config["ERP_DB"]))
        click.echo("Audit chain intact." if ok else f"Audit chain BROKEN at row {bad}.")

    return app
