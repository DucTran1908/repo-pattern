# repo_pattern

A stack- and domain-agnostic repository template for building with Claude Code, following **SDD** (spec-driven), **verification-first** (TDD for code; metrics, golden outputs, manual or review checks elsewhere) and **ADLC** (agent development life cycle). Work is scaled by level: small tasks are done directly, medium and large ones go through a plan approved by the user.

## What's inside

| Path | Purpose |
|---|---|
| `CLAUDE.md` | Binding rules for agents: work levels, life cycle, verification methods, local workspace, plans, session logs |
| `.claude/settings.json` | Hook registration and base permissions |
| `.claude/hooks/` | Python guards that enforce the rules (+ unit tests) |
| `.claude/skills/` | `spec`, `plan`, `implement`, `session-log`, `report`, `sync-reference` with templates |
| `.claude/agents/` | `spec-writer`, `verification-writer`, `implementer`, `reviewer` |
| `specs/` | Feature specs with acceptance criteria and verification methods |
| `tests/` | Verification artifacts (tests, metric scripts, golden outputs, manual checklists) mapped to acceptance criteria |
| `src/` | Production code |
| `docs/workflow.md` | The workflow explained for humans |

## Start a new project from this template

```bash
git clone <this-repo-url> my-project
cd my-project
rm -rf .git
git init
```

- This template repo tracks the empty `.local/` skeleton (7 folders, each with an empty `README.md` index) by force-adding it. After `git init` the skeleton stays on disk but `.gitignore` excludes `.local/`, so nothing in it is ever committed in the new project. If it is missing, the SessionStart hook recreates it.
- Pick your stack and fill in *Project commands* in `CLAUDE.md`; extend `.gitignore` for the stack.
- Make sure Python 3.8+ is on `PATH` (needed only for the hooks).

## Daily use

1. Drop your raw requirements into `.local/project-requirements/` and any sample data into `.local/test/`.
2. Small tasks (typos, translations, wording): just ask — no plan needed.
3. Medium and large tasks: `/spec` (large) → `/plan` → approve → `/implement` → `/session-log`.

## Maintaining the template

The `.local/` skeleton is tracked only in this template repo. Only the seven empty `README.md` indexes belong there — keep plans, logs and other working files out of it. A new file under `.local/` is ignored and needs `git add -f`; the guard hook blocks agents from doing that, so run it yourself.

See [docs/workflow.md](docs/workflow.md) for the full flow.
