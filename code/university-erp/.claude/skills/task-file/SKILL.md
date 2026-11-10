---
name: task-file
description: Turn a feature or bug into agent-sized task files in tasks/. Use when planning work before any build.
---

A task is agent-sized when it is one pull request, one concern, one reviewer, and under an hour of agent time.

1. Read the module's `spec/` and the acceptance tests the work must make pass.
2. Split the work into tasks. For each, decide whether it can run in parallel with the others:
   two tasks that touch the same files **or the same interface** cannot.
3. Write each task as `tasks/NNN-<slug>.md` from `tasks/TEMPLATE.md`. Propose an autonomy level and a token budget,
   and say in one line why that level.
4. Print a table: id, title, depends on, parallel-safe (yes/no), autonomy, budget.
5. Do not start building. The human approves the plan first.
