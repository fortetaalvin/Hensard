---
name: write-adr
description: Draft an architecture decision record in spec/adr/ from a decision the team has already made. Use when someone says "record this decision" or "write an ADR".
---

1. Ask for (or find in the conversation) the decision, the options considered, and why this one won. Do not invent reasons.
2. Find the next number: list the module's `spec/adr/` and add one to the highest `NNNN`.
3. Write `erp/modules/<name>/spec/adr/NNNN-<kebab-title>.md` with the sections Context, Options considered, Decision, Consequences and fill every section.
4. Keep it under one page. Consequences must include at least one cost or risk, not only benefits.
5. Status is `Proposed`. Only a human changes it to `Accepted`.
6. Because spec folders are protected, print the finished ADR for the human to save, unless they started the session
   with `AGENT_UNLOCK=erp/modules/<name>/spec/adr/`.
