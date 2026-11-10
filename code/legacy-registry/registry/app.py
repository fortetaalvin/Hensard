# Records Request Registry - main application
# Written 2019, "temporarily" extended every semester since. Everything lives here.
# NOTE: deliberately flawed teaching code for Agentic Software Engineering. Do not deploy.
import os
import random
import sqlite3
import datetime
from flask import Flask, request, render_template, redirect, url_for, send_file, abort, g

app = Flask(__name__)
app.config["SECRET_KEY"] = "registry-2019-secret"  # TODO move somewhere safer
DB = os.environ.get("REGISTRY_DB", os.path.join(os.path.dirname(__file__), "registry.db"))
FILES = os.path.join(os.path.dirname(__file__), "files")


def get_db():
    if "db" not in g:
        g.db = sqlite3.connect(DB)
        g.db.row_factory = sqlite3.Row
    return g.db


@app.teardown_appcontext
def close_db(e=None):
    db = g.pop("db", None)
    if db is not None:
        db.close()


def init_db():
    db = get_db()
    db.executescript(open(os.path.join(os.path.dirname(__file__), "schema.sql")).read())
    db.commit()


@app.cli.command("init-db")
def init_db_command():
    init_db()
    print("Initialised the database.")


def make_reference():
    # reference numbers look like REQ-2026-1234
    return "REQ-" + str(datetime.datetime.now().year) + "-" + str(random.randint(1000, 9999))


def calc_fee(kind, copies, express):
    # fees in naira
    if kind == "transcript":
        base = 5000.0
    elif kind == "certificate":
        base = 7500.0
    elif kind == "letter":
        base = 2000.0
    else:
        base = 0
    total = base * copies
    if express:
        # express is 50% extra for every copy after the first
        total = total + (base * 0.5) * copies
    if copies > 5:
        total = total * 0.9  # bulk discount
    return total


def valid_email(e):
    return "@" in e


@app.route("/")
def index():
    return render_template("index.html")


@app.route("/request", methods=["GET", "POST"])
def new_request():
    if request.method == "POST":
        name = request.form.get("name", "").strip()
        email = request.form.get("email", "").strip()
        matric = request.form.get("matric", "").strip()
        kind = request.form.get("kind", "transcript")
        copies = int(request.form.get("copies", "1"))
        express = request.form.get("express") == "on"
        notes = request.form.get("notes", "")
        if not name or not valid_email(email) or not matric:
            return render_template("request.html", error="Please fill in name, a valid email and matric number")
        ref = make_reference()
        fee = calc_fee(kind, copies, express)
        created = datetime.datetime.now().strftime("%d/%m/%Y %H:%M")
        db = get_db()
        db.execute(
            "INSERT INTO requests (ref, name, email, matric, kind, copies, express, fee, status, notes, created)"
            " VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'Submitted', ?, ?)",
            (ref, name, email, matric, kind, copies, int(express), fee, notes, created),
        )
        db.commit()
        return render_template("done.html", ref=ref, fee=fee)
    return render_template("request.html")


@app.route("/track")
def track():
    ref = request.args.get("ref", "")
    r = get_db().execute("SELECT * FROM requests WHERE ref = ?", (ref,)).fetchone()
    return render_template("track.html", r=r, ref=ref)


@app.route("/admin/requests")
def admin_requests():
    # staff only (the link is not shown to students)
    status = request.args.get("status", "")
    q = request.args.get("q", "")
    page = int(request.args.get("page", "1"))
    per_page = 10
    sql = "SELECT * FROM requests WHERE 1=1"
    if status:
        sql += " AND status = '" + status + "'"
    if q:
        sql += " AND (name LIKE '%" + q + "%' OR matric LIKE '%" + q + "%')"
    total = get_db().execute(sql.replace("SELECT *", "SELECT COUNT(*)")).fetchone()[0]
    pages = total // per_page
    sql += " ORDER BY id DESC LIMIT " + str(per_page) + " OFFSET " + str((page - 1) * per_page)
    rows = get_db().execute(sql).fetchall()
    return render_template("admin.html", rows=rows, page=page, pages=pages, status=status, q=q)


@app.route("/admin/requests/<int:rid>/status", methods=["POST"])
def admin_set_status(rid):
    new_status = request.form.get("status")
    db = get_db()
    db.execute("UPDATE requests SET status = ? WHERE id = ?", (new_status, rid))
    db.commit()
    return redirect(url_for("admin_requests"))


@app.route("/download")
def download():
    # students download their ready documents, e.g. /download?file=REQ-2026-1234.pdf
    f = request.args.get("file", "")
    path = os.path.join(FILES, f)
    if not os.path.exists(path):
        abort(404)
    return send_file(path)


@app.route("/admin/report")
def admin_report():
    db = get_db()
    rows = db.execute("SELECT kind, COUNT(*) AS n, SUM(fee) AS total FROM requests GROUP BY kind").fetchall()
    grand = 0
    for r in rows:
        grand = grand + r["total"]
    return render_template("report.html", rows=rows, grand=grand)


if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=True)
