# evals/

Measures this repository's **agent configuration** (AGENTS.md, `.claude/`, skills, model), not the application.
When you change any of those, rerun the evals; the `Evals` workflow does it automatically on pull requests.

A task is a YAML file: `id`, `title`, `prompt`, `check` (exit 0 = pass), optional `setup` and `adversarial`.
The three examples are adversarial: an injected instruction, a request to tamper with the spec, and a secret left as bait.
Week 6 asks for at least five tasks of your own and a before/after table.
