# University ERP

The ERP your class builds over 12 weeks of Agentic Software Engineering, for **your own university**.
A shared core plus one module per office: the whole class builds **Course Registration** together in the weekly labs,
and each team builds one more module as its capstone.

## Run it

```bash
python -m pip install -e ".[dev]"
flask --app erp.app seed        # creates erp.db from institution.yaml with synthetic students and staff
flask --app erp.app run         # http://127.0.0.1:5000
pytest -q
```

Seeded accounts all use the password `change-me-dev-only`: `admin`, `registrar`, `bursar`, `exams.officer`,
`admissions.officer`, `hr.officer`, `payroll.officer`, `librarian`, `hostel.officer`, `timetable.officer`,
departmental staff such as `csc.staff1` (the HOD), and students `stu0001` onward.

## Make it your university (week 1)

Edit `institution.yaml`: the name, faculties, departments and programmes, matric and staff number formats, the
grading scale and credit-load limits from your Senate regulations. Structure only: **never put real student or staff
data anywhere in this repository**. The seed generates invented people.

## How the class works in this repository

| Who | Works in | Reviewed by |
| --- | --- | --- |
| The whole class | `erp/modules/registration/` (weekly labs) | Instructors and trainees |
| Each team | `erp/modules/<your-module>/` (capstone) | Your team (CODEOWNERS) |
| Instructors | `erp/core/`, `institution.yaml`, `docs/integration-contracts.md` | Instructors |

- **Pick a module** in week 3 from [`docs/module-catalogue.md`](docs/module-catalogue.md); copy `erp/modules/_template/`.
- **Integrate** in weeks 9–10 through the events in [`docs/integration-contracts.md`](docs/integration-contracts.md).
- **Every change is a pull request** with its agent transcript, autonomy level and token budget (the PR template and
  the `PR evidence` check enforce it).

## What protects the ERP from its builders

| Guard rail | Where |
| --- | --- |
| Agents cannot edit the core, any spec, acceptance tests, the contracts or the institution config | `.claude/settings.json`, `.claude/hooks/protect_paths.py` |
| Risky shell commands (force-push, network tools, reading `.env`) are blocked | `.claude/hooks/guard_bash.py` |
| Every consequential action is in a hash-chained, append-only audit log | `erp/core/audit.py`; `flask --app erp.app verify-audit` |
| Teams can only approve changes to their own module | `.github/CODEOWNERS` + branch protection |
| Evals check the agent setup against injected instructions, spec tampering, secrets and unauthorised grade changes | `evals/` |
| A scheduled agent runs only behind a human approval gate, with a budget and a kill switch | `.github/workflows/scheduled-agent.yml` |
