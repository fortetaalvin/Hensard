import pytest

from registry.app import app, init_db


@pytest.fixture
def client(tmp_path, monkeypatch):
    monkeypatch.setattr("registry.app.DB", str(tmp_path / "test.db"))
    app.config["TESTING"] = True
    with app.app_context():
        init_db()
    with app.test_client() as c:
        yield c
