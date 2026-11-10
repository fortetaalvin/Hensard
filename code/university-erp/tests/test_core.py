import sqlite3

import pytest

from erp.core import audit, contracts, events
from erp.core.config import grade_for, institution
from erp.core.seed import DEV_PASSWORD


def test_institution_config_loads():
    cfg = institution()
    assert cfg["name"] and cfg["faculties"] and cfg["credit_load"]["max"] > cfg["credit_load"]["min"]


@pytest.mark.parametrize("score,grade", [(70, "A"), (69.9, "B"), (50, "C"), (45, "D"), (40, "E"), (39, "F")])
def test_grade_scale(score, grade):
    assert grade_for(score)[0] == grade


def test_seed_builds_structure_from_config(db):
    depts = sum(len(f["departments"]) for f in institution()["faculties"])
    assert db.execute("SELECT COUNT(*) FROM departments").fetchone()[0] == depts
    assert db.execute("SELECT COUNT(*) FROM students").fetchone()[0] == 5 * depts
    assert db.execute("SELECT COUNT(*) FROM staff").fetchone()[0] == 4 * depts


def test_contracts_get_student_and_roles(db):
    matric = db.execute("SELECT matric_no FROM students LIMIT 1").fetchone()[0]
    s = contracts.get_student(db, matric)
    assert s["matric_no"] == matric and s["programme"]
    hod = db.execute("SELECT user_id, scope FROM user_roles WHERE role = 'hod' LIMIT 1").fetchone()
    assert contracts.has_role(db, hod["user_id"], "hod", hod["scope"])
    assert not contracts.has_role(db, hod["user_id"], "hod", "SOME-OTHER-DEPT")
    assert not contracts.has_role(db, hod["user_id"], "bursar")


def test_audit_chain_detects_tampering(db):
    contracts.record_event(db, "exams.officer", "grade.change", "CSC 311/stu0001", {"from": "C", "to": "A"})
    db.commit()
    assert audit.verify(db) == (True, None)
    # Triggers stop ordinary edits...
    with pytest.raises(sqlite3.DatabaseError):
        db.execute("UPDATE audit_log SET details = '{}' WHERE id = 2")
    # ...and if someone drops the trigger and edits anyway, the chain shows exactly where.
    db.execute("DROP TRIGGER audit_no_update")
    db.execute('UPDATE audit_log SET details = \'{"from": "C", "to": "B"}\' WHERE id = 2')
    assert audit.verify(db) == (False, 2)


def test_event_bus_isolates_failing_handlers():
    got = []
    events.subscribe("fees.cleared", lambda p: 1 / 0)
    events.subscribe("fees.cleared", got.append)
    assert events.publish("fees.cleared", {"matric_no": "X"}) == 1
    assert got == [{"matric_no": "X"}]


def test_login_and_home(app):
    c = app.test_client()
    assert c.get("/").status_code == 302
    r = c.post("/login", data={"username": "registrar", "password": DEV_PASSWORD}, follow_redirects=True)
    assert b"registrar" in r.data and b"Registration" in r.data
    assert c.post("/login", data={"username": "registrar", "password": "wrong"}).status_code == 200


def test_registration_module_is_mounted(app):
    c = app.test_client()
    c.post("/login", data={"username": "admin", "password": DEV_PASSWORD})
    assert c.get("/registration/").status_code == 200
