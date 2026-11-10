# Governance

Who is accountable for this agent-built system, and how anyone can check. Week 11; reviewed by all three roles.

## 1. Accountability
- A human merges every change and is accountable for it. Agents never merge.
- Roles: **Analyst** owns the spec · **Operator** owns the harness, cost and evals · **Guardian** owns security.
- CODEOWNERS enforces review by the owner of each sensitive path.

## 2. Autonomy policy
| Kind of change | Maximum autonomy | Human gate |
| --- | --- | --- |
| Docs, tests, refactors with full test coverage | L2 | PR review after the fact |
| Application features | L1 | Review of every diff before merge |
| Schema migrations, auth, payments, personal data, grades | L0 | Human writes or types the change |
| Any change to a result after Senate approval | Not delegable | Exams Officer and HOD both approve in the results workflow; audit event recorded |
| Scheduled maintenance tasks | L3 | `agent-approval` environment; draft PRs only |

## 3. Data protection (Nigeria Data Protection Act 2023)
- Controller: <!-- the organisation that decides why and how personal data is processed -->
- Personal data held, lawful basis, retention period, and who can access it: <!-- table -->
- No real personal data in development, tests, prompts or transcripts. Fixtures are synthetic.

## 4. Licensing and intellectual property
- Project licence: <!-- chosen in week 11 -->
- Dependency licences allowed: MIT, BSD, Apache-2.0, ISC, PSF, MPL-2.0. Enforced by the `Licence check` workflow.
- Agent output is reviewed for copied code; a suspected copy is removed and recorded in an issue labelled `licence`.

## 5. Audit trail
- Every change: PR + transcript + CI run. Scheduled runs: Actions artifacts kept 90 days.
- Repository audit log and branch rulesets are reviewed by the Guardian each week.

## 6. Incidents
- Runbook: `docs/runbook.md`. Postmortems: `docs/incidents/`. Blameless; actions tracked as issues.
