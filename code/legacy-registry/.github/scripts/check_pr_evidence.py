#!/usr/bin/env python3
"""Check a pull request description carries the evidence the course requires."""

import json
import re
import sys

event = json.load(open(sys.argv[1], encoding="utf-8"))
body = (event.get("pull_request") or {}).get("body") or ""


def field(label):
    m = re.search(rf"\*\*{label}:\*\*(.*)", body)
    return re.sub(r"<!--.*?-->", "", m.group(1)).strip() if m else ""


problems = []
transcript = field("Transcript")
if not re.search(r"(transcripts/\S+|https?://\S+)", transcript):
    problems.append("Transcript: link a file in transcripts/ or a URL.")
if not re.search(r"\bL[0-3]\b", field("Autonomy level")):
    problems.append("Autonomy level: state L0, L1, L2 or L3.")
if not re.search(r"declared\s*\d+", field("Token budget"), re.I):
    problems.append("Token budget: give the declared budget (and what you used).")
wrong = body.split("## What the agent got wrong, and how I caught it")
if len(wrong) < 2 or not re.sub(r"<!--.*?-->|\s|#.*", "", wrong[1].split("## ")[0]):
    problems.append("'What the agent got wrong' is empty.")

if problems:
    print("This PR is missing required evidence:\n- " + "\n- ".join(problems))
    sys.exit(1)
print("Evidence present: transcript, autonomy level, budget, and what the agent got wrong.")
