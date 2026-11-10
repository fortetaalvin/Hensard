#!/usr/bin/env python3
"""Run the harness eval suite: each task in evals/tasks/*.yaml is given to the agent in a clean
git worktree, then a check command decides pass or fail.

    python evals/run_evals.py --dry-run              # validate tasks, run nothing
    EVAL_AGENT_CMD='claude -p --max-turns 15' python evals/run_evals.py --out reports/evals.md
    python evals/run_evals.py --only no-spec-tampering

EVAL_AGENT_CMD is any headless agent command that reads the prompt on stdin.
The check command sees $EVAL_OUTPUT (the agent's output file) and runs inside the worktree.
"""

import argparse
import os
import pathlib
import shutil
import subprocess
import sys
import tempfile
import time

import yaml

ROOT = pathlib.Path(__file__).resolve().parent.parent
REQUIRED = {"id", "title", "prompt", "check"}


def load_tasks(only=None):
    tasks = []
    for f in sorted((ROOT / "evals" / "tasks").glob("*.yaml")):
        t = yaml.safe_load(f.read_text(encoding="utf-8"))
        missing = REQUIRED - set(t)
        if missing:
            sys.exit(f"{f.name}: missing fields {sorted(missing)}")
        if not only or t["id"] in only:
            tasks.append(t)
    return tasks


def sh(cmd, cwd, env=None, stdin=None, timeout=900):
    return subprocess.run(
        cmd, shell=True, cwd=cwd, env=env, input=stdin, text=True, capture_output=True, timeout=timeout
    )


def run_task(t, agent_cmd, timeout):
    tmp = pathlib.Path(tempfile.mkdtemp(prefix=f"eval-{t['id']}-"))
    wt = tmp / "wt"
    sh(f'git worktree add --detach "{wt}" HEAD', ROOT)
    out = tmp / "agent-output.txt"
    env = {**os.environ, "EVAL_OUTPUT": str(out)}
    try:
        if t.get("setup"):
            sh(t["setup"], wt, env)
        start = time.time()
        try:
            r = sh(agent_cmd, wt, env, stdin=t["prompt"], timeout=timeout)
            out.write_text(r.stdout + r.stderr, encoding="utf-8")
        except subprocess.TimeoutExpired:
            out.write_text("TIMEOUT", encoding="utf-8")
        secs = time.time() - start
        ok = sh(t["check"], wt, env).returncode == 0
        return ok, secs
    finally:
        sh(f'git worktree remove --force "{wt}"', ROOT)
        shutil.rmtree(tmp, ignore_errors=True)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    ap.add_argument("--only", nargs="*")
    ap.add_argument("--out")
    ap.add_argument("--timeout", type=int, default=900)
    a = ap.parse_args()
    tasks = load_tasks(a.only)
    rows = ["| Task | Adversarial | Result | Seconds |", "| --- | --- | --- | --- |"]
    agent_cmd = os.environ.get("EVAL_AGENT_CMD")
    if not a.dry_run and not agent_cmd:
        sys.exit("Set EVAL_AGENT_CMD, or use --dry-run.")
    passed = 0
    for t in tasks:
        adv = "yes" if t.get("adversarial") else "no"
        if a.dry_run:
            rows.append(f"| {t['id']}: {t['title']} | {adv} | not run (dry run) | – |")
            continue
        ok, secs = run_task(t, agent_cmd, a.timeout)
        passed += ok
        rows.append(f"| {t['id']}: {t['title']} | {adv} | {'PASS' if ok else 'FAIL'} | {secs:.0f} |")
    summary = f"\n**{len(tasks)} tasks**" + (
        "" if a.dry_run else f", **{passed} passed** ({passed / max(1, len(tasks)):.0%})"
    )
    report = "## Eval results\n\n" + "\n".join(rows) + "\n" + summary + "\n"
    print(report)
    if a.out:
        pathlib.Path(a.out).parent.mkdir(parents=True, exist_ok=True)
        pathlib.Path(a.out).write_text(report, encoding="utf-8")


if __name__ == "__main__":
    main()
