Read AGENTS.md first; it is the shared context for every coding agent in this repository.

Claude-specific notes:
- Sub-agents live in `.claude/agents/` (`reviewer`, `spec-auditor`). Use `reviewer` in a fresh context before opening a PR.
- Skills live in `.claude/skills/` (`write-adr`, `task-file`).
- Hooks in `.claude/hooks/` block edits to protected paths and save your transcript to `transcripts/` when you stop.
