"""Synthetic seed data: the institution's structure from institution.yaml plus invented people.
Never load real student or staff records into a development database."""

import os
import random

from . import audit
from .auth import hash_password
from .config import institution

FIRST = [
    "Ebiere",
    "Tonye",
    "Chinedu",
    "Aisha",
    "Oluwaseun",
    "Ngozi",
    "Ibrahim",
    "Ese",
    "Tamuno",
    "Zainab",
    "Emeka",
    "Funmilayo",
    "Musa",
    "Preye",
    "Halima",
    "Ayebatari",
    "Kelechi",
    "Amaka",
    "Yusuf",
    "Tari",
    "Bolanle",
    "Ovie",
]
LAST = [
    "Okafor",
    "Ebikake",
    "Adeyemi",
    "Bello",
    "Ogbuehi",
    "Ibe",
    "Diepreye",
    "Abubakar",
    "Eze",
    "Opukiri",
    "Usman",
    "Okonkwo",
    "Alamieyeseigha",
    "Nwosu",
    "Lawal",
    "Tamarau",
    "Obi",
    "Akpan",
    "Ojo",
    "Ayibapreye",
    "Danjuma",
]
DEV_PASSWORD = os.environ.get("ERP_DEV_PASSWORD", "change-me-dev-only")  # noqa: S105 - dev databases only


def _user(con, username, full_name, roles, domain, pw_hash):
    cur = con.execute(
        "INSERT INTO users (username, full_name, email, password_hash) VALUES (?, ?, ?, ?)",
        (username, full_name, f"{username}@{domain}", pw_hash),
    )
    for role, scope in roles:
        con.execute("INSERT INTO user_roles (user_id, role, scope) VALUES (?, ?, ?)", (cur.lastrowid, role, scope))
    return cur.lastrowid


def seed(con, students_per_programme: int = 20, seed_value: int = 7) -> dict:
    rnd = random.Random(seed_value)
    cfg = institution()
    dom, short = cfg["email_domain"], cfg["short_name"]
    session_year = int(cfg["sessions"]["current"][:4])
    counts = {"students": 0, "staff": 0, "courses": 0}
    pw = hash_password(DEV_PASSWORD)  # hashed once: every seeded account shares the dev password
    _user(con, "admin", "System Administrator", [("admin", "*")], dom, pw)
    for role in (
        "registrar",
        "bursar",
        "exams_officer",
        "admissions_officer",
        "hr_officer",
        "payroll_officer",
        "librarian",
        "hostel_officer",
        "timetable_officer",
    ):
        _user(
            con,
            role.replace("_", "."),
            f"{rnd.choice(FIRST)} {rnd.choice(LAST)} ({role.replace('_', ' ')})",
            [(role, "*")],
            dom,
            pw,
        )
    staff_serial, matric_serial = 1, 1
    for fac in cfg["faculties"]:
        con.execute("INSERT INTO faculties (code, name) VALUES (?, ?)", (fac["code"], fac["name"]))
        for dept in fac["departments"]:
            con.execute(
                "INSERT INTO departments (code, name, faculty_code) VALUES (?, ?, ?)",
                (dept["code"], dept["name"], fac["code"]),
            )
            for lvl in (100, 200, 300, 400):
                for sem_i, sem in enumerate(cfg["sessions"]["semesters"], start=1):
                    for k in (1, 2, 3):
                        code = f"{dept['code']} {lvl + sem_i * 10 + k}"
                        con.execute(
                            "INSERT INTO courses (code, title, units, level, semester, department_code) "
                            "VALUES (?, ?, ?, ?, ?, ?)",
                            (
                                code,
                                f"{dept['name']} {lvl}-level topic {sem_i}.{k}",
                                rnd.choice([2, 3, 3, 4]),
                                lvl,
                                sem,
                                dept["code"],
                            ),
                        )
                        counts["courses"] += 1
            for i, rank in enumerate(["Professor", "Senior Lecturer", "Lecturer I", "Lecturer II"]):
                name = f"{rnd.choice(FIRST)} {rnd.choice(LAST)}"
                roles = [("lecturer", dept["code"])] + ([("hod", dept["code"])] if i == 0 else [])
                uid = _user(con, f"{dept['code'].lower()}.staff{i + 1}", name, roles, dom, pw)
                con.execute(
                    "INSERT INTO staff (staff_no, user_id, department_code, category, rank) VALUES (?, ?, ?, ?, ?)",
                    (cfg["staff_no_format"].format(serial=staff_serial), uid, dept["code"], "academic", rank),
                )
                staff_serial += 1
                counts["staff"] += 1
            for prog in dept["programmes"]:
                pid = con.execute(
                    "INSERT INTO programmes (name, department_code) VALUES (?, ?)", (prog, dept["code"])
                ).lastrowid
                for _ in range(students_per_programme):
                    level = rnd.choice([100, 200, 300, 400])
                    entry = session_year - level // 100 + 1
                    matric = cfg["matric_format"].format(year=entry, dept=dept["code"], serial=matric_serial)
                    uid = _user(
                        con,
                        f"stu{matric_serial:04d}",
                        f"{rnd.choice(FIRST)} {rnd.choice(LAST)}",
                        [("student", "*")],
                        dom,
                        pw,
                    )
                    con.execute(
                        "INSERT INTO students (matric_no, user_id, programme_id, level, entry_session) "
                        "VALUES (?, ?, ?, ?, ?)",
                        (matric, uid, pid, level, f"{entry}/{entry + 1}"),
                    )
                    matric_serial += 1
                    counts["students"] += 1
    audit.record(con, "system", "seed", short, counts)
    con.commit()
    return counts
