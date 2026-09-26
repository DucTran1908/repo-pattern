# CLAUDE.md

This repository is developed with Claude Code as the primary coding assistant and follows three disciplines:

- **SDD – Spec-Driven Development**: every feature starts as a spec in `specs/` with numbered acceptance criteria.
- **TDD – Test-Driven Development**: tests are written from the acceptance criteria and must fail before implementation.
- **ADLC – Agent Development Life Cycle**: work moves through fixed stages, each owned by a skill or subagent.

## Development life cycle

```
Spec ──► Plan ──► [user approval] ──► Test (red) ──► Implement (green → refactor) ──► Review ──► Session log / Report
spec     plan                         test-writer     implementer                     reviewer     session-log / report
```

| Stage | Owner | Output |
|---|---|---|
| Spec | `spec` skill / `spec-writer` agent | `specs/<id>-<slug>.md` with acceptance criteria `AC-n` |
| Plan | `plan` skill | Implement plan in the local plan folder — **stop and wait for approval** |
| Test (red) | `test-writer` agent | Failing tests mapped to `AC-n` |
| Implement | `implement` skill / `implementer` agent | Code that makes the tests pass, checklist ticked item by item |
| Review | `reviewer` agent | Findings against the spec and the plan's acceptance criteria |
| Log / Report | `session-log`, `report`, `sync-reference` skills | Session log, Vietnamese report, refreshed reference notes |

Small fixes may skip the spec, but never the plan-approval step for non-trivial changes and never the red test.

## Project commands

Fill these in when the stack is chosen. Agents must use them instead of guessing.

| Purpose | Command |
|---|---|
| Install | `TODO` |
| Test (all) | `TODO` |
| Test (single) | `TODO` |
| Lint / format | `TODO` |
| Build | `TODO` |
| Hook self-test | `python -m unittest discover .claude/hooks/tests` |

## Local workspace (`.local/`)

`.local/` is always ignored by git (no need to check `.gitignore`). It holds per-machine session data and must always contain the subfolders below. Hooks in `.claude/hooks/` recreate missing folders at session start and enforce the write rules.

| Folder | Purpose | Agent may write? |
|---|---|---|
| `plan/` | Implement plans requested by the user | Create new plans freely. Editing an existing plan requires user approval, except ticking checklist items `[ ]`→`[x]` in order while executing it |
| `design_system/` | User's raw input: definitions and requirements for the repo | **Never.** Report blockers and propose changes instead |
| `report/` | Reports requested by the user | Yes — always in Vietnamese, plain non-technical language |
| `reference/` | Summaries: goals & vision, pipeline, workflow, project-specific terms | Yes — keep in sync when the source changes |
| `test/` | Test data provided by the user | Read and analyse only; edit only when the user explicitly asks |
| `temp/` | Scratch files for user and agent | Freely |
| `session_log/` | User decisions and agent changes per session | Yes — see *Session log* |

**Index rule.** Every subfolder has a `README.md` that contains only a heading and a mapping table `| Path | Description |` (short, precise description per file). Update it whenever a file is added, renamed or removed — this includes `design_system/` and `test/`, whose index is the only file an agent may edit there. Nothing else goes in the index.

**No leakage rule.** Tracked files (code, comments, specs, tests, commit messages, PR descriptions) must never reference specific content of `.local/` — no file names, numbers, quotes or paths into it. Only the framework files (`CLAUDE.md`, root `README.md`, `.gitignore`, `docs/workflow.md`, `.claude/**`) may describe the workspace *conventions*. If a spec needs information from `.local/`, restate the requirement in the spec itself.

## Implement plans

- Created with the `plan` skill from `.claude/skills/plan/template.md`, saved as `.local/plan/YYYY-MM-DD_<slug>.md`, and indexed in the plan `README.md`.
- Every section starts with a one-line summary (`> Tóm tắt: ...`). Required sections, in order:
  1. Nguyên nhân (cause)
  2. Phương án (approach)
  3. Phạm vi (scope)
  4. Tác động (impact)
  5. Lưu ý (caveats)
  6. Bảng file sẽ thay đổi (file change table)
  7. Checklist to do
  8. Tiêu chí nghiệm thu (acceptance criteria)
- **After writing a plan, stop.** Never start implementing until the user approves it; then set its status to `approved`.

### Executing a plan

- Work the checklist top to bottom. Tick each item (`- [ ]` → `- [x]`) **immediately** after finishing it and before starting the next one.
- Never skip an item or tick ahead. The only exceptions need direct user approval in chat — e.g. running the whole flow end to end to get results, or a blocker that requires changing the plan. Mark an approved skip as `- [~] ... (skipped: <reason>, approved by user)`.
- On a blocker: stop, explain it, propose options, and wait. Changing the plan's content requires approval.

## Session log

Write or update a session log with the `session-log` skill whenever the user made decisions or files changed (a Stop hook reminds you). File: `.local/session_log/YYYY-MM-DD_<branch>_<topic>.md`, template in `.claude/skills/session-log/template.md`. Mandatory sections:

1. Git branch name
2. Completion time
3. Short cause leading to the decisions / changes
4. Table of decisions / changes
5. Short impact of the decisions / chosen change approach
6. Details of each decision / change

## Coding conventions

- Tests map to acceptance criteria: name or tag each test with its `AC-n` id.
- Keep changes inside the approved plan's scope; list any extra file you had to touch in the session log.
- Commit only when the user asks. Commit messages describe the change itself, never local workspace content.
