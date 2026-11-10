#!/usr/bin/env python3
"""PreToolUse hook for Bash: refuse commands that exfiltrate, destroy or bypass review."""

import json
import re
import sys

cmd = (json.load(sys.stdin).get("tool_input") or {}).get("command", "")
RULES = [
    (r"\bgit\s+push\b.*(--force|-f\b)", "Force-push is not allowed."),
    (r"\bgit\s+push\b.*\bmain\b", "Push a branch and open a PR; never push to main."),
    (r"\b(curl|wget|nc|ncat)\b", "Network tools are blocked in the harness. Ask the human."),
    (r"\brm\s+-[a-z]*r[a-z]*f|\brm\s+-[a-z]*f[a-z]*r", "Recursive force delete is blocked."),
    (r"(cat|less|more|head|tail|type)\s+[^|;]*\.env\b", "Reading .env is blocked."),
    (r"\bprintenv\b|\benv\s*$|\bset\s*$", "Dumping the environment can leak secrets."),
    (r"--no-verify", "Skipping hooks is not allowed."),
]
for pattern, reason in RULES:
    if re.search(pattern, cmd):
        print(f"Blocked: {reason} (command: {cmd[:120]})", file=sys.stderr)
        sys.exit(2)
sys.exit(0)
