#!/usr/bin/env python3
"""PostToolUse hook: format and lint-fix any Python file the agent just wrote. Never blocks."""

import json
import shutil
import subprocess
import sys

path = (json.load(sys.stdin).get("tool_input") or {}).get("file_path", "")
if path.endswith(".py") and shutil.which("ruff"):
    subprocess.run(["ruff", "format", "--quiet", path], check=False)
    subprocess.run(["ruff", "check", "--fix", "--quiet", path], check=False)
sys.exit(0)
