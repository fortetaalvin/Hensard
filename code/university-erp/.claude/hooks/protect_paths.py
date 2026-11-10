#!/usr/bin/env python3
"""PreToolUse hook: block agent edits to the spec, acceptance tests, workflows and secrets.
Exit code 2 blocks the call; stderr is shown to the agent as the reason."""

import json
import os
import sys

PROTECTED = ("erp/core/", "docs/integration-contracts.md", "institution.yaml", ".github/", ".claude/", "secrets/")
# Any module's spec/ folder and acceptance tests are human-owned too.
PROTECTED_PARTS = ("/spec/", "/tests/test_acceptance.py")
SECRET_NAMES = (".env",)

data = json.load(sys.stdin)
path = (data.get("tool_input") or {}).get("file_path", "")
root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
rel = os.path.relpath(os.path.abspath(path), root).replace(os.sep, "/") if path else ""

# A human may unlock one protected prefix for a session: AGENT_UNLOCK=spec/adr/ claude ...
unlocked = os.environ.get("AGENT_UNLOCK", "")
if rel.startswith("../"):
    print(f"Blocked: {rel} is outside the repository.", file=sys.stderr)
    sys.exit(2)
if os.path.basename(rel).startswith(SECRET_NAMES):
    print(
        "Blocked: agents never write secret files. Use environment variables or Actions secrets.",
        file=sys.stderr,
    )
    sys.exit(2)
for part in PROTECTED_PARTS:
    if part in "/" + rel and not (unlocked and rel.startswith(unlocked)):
        print(
            f"Blocked: {rel} is part of a module's specification. Humans change the spec; if it looks wrong, "
            "stop and explain why.",
            file=sys.stderr,
        )
        sys.exit(2)
for prefix in PROTECTED:
    if rel.startswith(prefix) and not (unlocked and rel.startswith(unlocked)):
        print(
            f"Blocked: {prefix} is protected. The spec and the harness are changed by humans. "
            "If you think it is wrong, stop and explain why.",
            file=sys.stderr,
        )
        sys.exit(2)
sys.exit(0)
