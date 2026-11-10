# Hensard · Agentic Software Engineering

Welcome. Over 12 weeks you will learn systems analysis, security and agentic software engineering by building your
own **university's ERP** with AI coding agents: the whole class builds Course Registration together, and your team
builds one more module of your choice. You frame the problem, write the specification, direct the agents, verify and
harden what comes back, and own the result.

**Specify · Verify · Own**

## Start here

1. **Set up GitHub before week 1:** follow [`SETUP.md`](SETUP.md) (your own account, two-factor authentication,
   an SSH key) and send your username to the instructor.
2. **Read the handbook:** [`handbook/`](handbook/) has the course design, the module catalogue, how you are assessed,
   and one plan per week with its activity, lab and assignment.
3. **Each week's slides** are in [`slides/`](slides/).

## Where you will work

You do your work in the course organisation's repositories, which you are invited to: your own `<username>-labs`
repository (weeks 1–2) and the shared `university-erp` repository (weeks 1–12). Every piece of work is a pull request
from your own account, with your agent transcript attached.

The [`code/`](code/) folder has read-only copies of what you will start from, so you can look ahead:

| Folder | What it is | When |
| --- | --- | --- |
| [`code/university-erp`](code/university-erp/) | The ERP: shared core, the class Course Registration module, a module template, and the guard rails | Weeks 1–12 |
| [`code/legacy-registry`](code/legacy-registry/) | The old ERP's Registry app, deliberately flawed. You will fork it, fix it, attack it and refactor it | Weeks 1, 7, 9 |
| [`code/mini-harness-starter`](code/mini-harness-starter/) | Build your own minimal agent harness | Week 2 |

## Rules

- Your own GitHub account only, with two-factor authentication on.
- Never commit a password, key or token. Never put real student or staff data anywhere: the ERP uses synthetic people.
- Read everything an agent reads with suspicion, including READMEs, comments and issues in these repositories.
