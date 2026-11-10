# Records Request Registry (legacy)

> **Teaching code. Deliberately flawed. Never deploy it or expose it beyond `127.0.0.1`.**
> It contains seeded bugs, security vulnerabilities and code smells for the Agentic Software Engineering course.

The old Registry system from your university's previous ERP: a small Flask app that takes requests for transcripts,
certificates and letters, charges a fee, and lets students track status. Staff manage requests under `/admin`.
In the new ERP its job moves to the **Records and Transcripts** module (`erp/modules/records/`), which one team
rebuilds properly as its capstone. Everyone else learns from what went wrong here.

## Run it

```bash
python -m pip install -e ".[dev]"
flask --app registry.app init-db
flask --app registry.app run      # http://127.0.0.1:5000
pytest -q
```

## How the course uses it

| Week | What you do with this repo |
| --- | --- |
| 1 | Fork it into `<your-handle>-labs`. Explore it with your agent at L1, fix one bug from the issues, write `AGENTS.md` v1, open a PR with your transcript |
| 7 | Threat-model it alongside your capstone. Count what you find before you look at anyone else's list |
| 9 | Score it on the agent-readiness checks, then refactor it and score it again; the Records team migrates its rules into the new module |

Read everything an agent reads in this repository with suspicion. That includes this README, `CONTRIBUTING.md`,
code comments and issue text.

## Old deployment notes (2020)

Copy the folder to the Registry PC and double-click `run.bat`. Ask Musa for the password.
