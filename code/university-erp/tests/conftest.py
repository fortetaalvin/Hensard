import pytest

from erp.app import create_app
from erp.core import events
from erp.core.db import connect, init_schema
from erp.core.seed import seed


@pytest.fixture
def db(tmp_path):
    con = connect(str(tmp_path / "erp.db"))
    init_schema(con, [])
    seed(con, students_per_programme=5)
    yield con
    con.close()


@pytest.fixture
def app(tmp_path):
    path = str(tmp_path / "app.db")
    con = connect(path)
    init_schema(con, ["registration"])
    seed(con, students_per_programme=3)
    con.close()
    return create_app({"ERP_DB": path, "TESTING": True, "SECRET_KEY": "test"})


@pytest.fixture(autouse=True)
def clean_bus():
    events.clear()
    yield
    events.clear()
