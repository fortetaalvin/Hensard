#!/usr/bin/env python3
"""Stop hook: copy the session transcript into transcripts/ (with obvious secrets redacted)
so it can be linked from the pull request. Never blocks."""

import datetime
import json
import os
import re
import sys

data = json.load(sys.stdin)
src = data.get("transcript_path")
if not src or not os.path.exists(src):
    sys.exit(0)
root = os.environ.get("CLAUDE_PROJECT_DIR", os.getcwd())
out_dir = os.path.join(root, "transcripts")
os.makedirs(out_dir, exist_ok=True)
stamp = datetime.datetime.now(datetime.UTC).strftime("%Y%m%d-%H%M")
dest = os.path.join(out_dir, f"{stamp}-{data.get('session_id', 'session')[:8]}.jsonl")
SECRET = re.compile(
    r"(sk-[A-Za-z0-9_-]{16,}|ghp_[A-Za-z0-9]{20,}|github_pat_[A-Za-z0-9_]{20,}|AKIA[0-9A-Z]{16}|"
    r"(?i:(api[_-]?key|token|secret|password)\s*[:=]\s*)[^\s\"']{8,})"
)
with open(src, encoding="utf-8", errors="replace") as f, open(dest, "w", encoding="utf-8") as g:
    for line in f:
        g.write(SECRET.sub("[REDACTED]", line))
sys.exit(0)
