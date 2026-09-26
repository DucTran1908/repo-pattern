# CLAUDE.md

This repository is developed with Claude Code as the primary coding assistant and follows three disciplines:

- **SDD – Spec-Driven Development**: every feature starts as a spec in `specs/` with numbered acceptance criteria.
- **Verification-first** (TDD for code): every acceptance criterion declares how it will be verified, and that verification is prepared — and seen failing where possible — before the work is done.
- **ADLC – Agent Development Life Cycle**: work moves through fixed stages, each owned by a skill or subagent.

## Work levels

Before starting any task, state its level in one line (e.g. `Level: small — typo fix`). When unsure, pick the higher level and ask the user.

| Level | Typical work | Spec | Plan | Verification | Review | Session log |
|---|---|---|---|---|---|---|
| **Small** | Fix typos; translate text files (prompts, reports, plans); reword docs or comments; formatting; update a `README.md` index. No behaviour or logic change. | No | No — do it directly | Re-read the result | No | One row in the table |
| **Medium** | Behaviour change inside one module or a few files; bug fix; refactor without interface change; renames | Update the affected `AC-n` if behaviour changes | Yes — all 8 sections, wait for approval | Yes, per declared method | Self-review against the plan | Yes |
| **Large** | New feature; changes across modules; architecture, data schema, public interface, new dependency; hard-to-reverse operations (data migration or deletion) | Yes — required | Yes — all 8 sections, wait for approval | Yes, per declared method | `reviewer` agent | Yes, plus `sync-reference` |

Small work still passes through the hooks: e.g. translating an existing plan triggers an approval prompt, because hooks cannot tell work levels apart.

## Development life cycle (medium and large work)

```
Spec ──► Plan ──► [user approval] ──► Verify-first (red) ──► Implement (green → refactor) ──► Review ──► Session log / Report
spec     plan                         verification-writer    implementer                     reviewer     session-log / report
```

| Stage | Owner | Output |
|---|---|---|
| Spec | `spec` skill / `spec-writer` agent | `specs/<id>-<slug>.md` with acceptance criteria `AC-n` and their verification method |
| Plan | `plan` skill | Implement plan in the local plan folder — **stop and wait for approval** |
| Verify-first | `verification-writer` agent | Tests, metric scripts, golden outputs or check lists mapped to `AC-n`, failing where possible |
| Implement | `implement` skill / `implementer` agent | Work that makes the verifications pass, checklist ticked item by item |
| Review | `reviewer` agent | Findings against the spec, the plan's acceptance criteria and the verification evidence |
| Log / Report | `session-log`, `report`, `sync-reference` skills | Session log, Vietnamese report, refreshed reference notes |

## Verification methods

Every acceptance criterion (in specs and plans) names one method. Prefer the most automated method that fits.

| Method | Use for | "Red first" means |
|---|---|---|
| `test` | Code with deterministic logic (default for code) | The automated test runs and fails |
| `metric` | Data, ML, performance | The measuring script runs and the threshold is not met yet (e.g. `accuracy >= 0.90`) |
| `output-diff` | Pipelines, generated reports, CLIs | Output differs from the expected (golden) output |
| `manual` | UI, infrastructure, one-off operations | Steps and expected results are written down before the work; evidence is recorded when run |
| `review` | Documents, content, prompts | A review checklist is written down before the work |

Verification artifacts live under `tests/` (see `tests/README.md`).

## Project commands

Fill these in when the stack is chosen. Agents must use them instead of guessing.

| Purpose | Command |
|---|---|
| Install | `TODO` |
| Test (all) | `TODO` |
| Test (single) | `TODO` |
| Verify (metrics / golden) | `TODO` |
| Lint / format | `TODO` |
| Build | `TODO` |
| Hook self-test | `python -m unittest discover .claude/hooks/tests` |

## Local workspace (`.local/`)

`.local/` is always ignored by git (no need to check `.gitignore`). It holds per-machine session data and must always contain the subfolders below. Hooks in `.claude/hooks/` recreate missing folders at session start and enforce the write rules.

| Folder | Purpose | Agent may write? |
|---|---|---|
| `plan/` | Implement plans requested by the user | Create new plans freely. Editing an existing plan requires user approval, except ticking checklist items `[ ]`→`[x]` in order while executing it |
| `project-requirements/` | User's raw input: definitions and requirements for the project | **Never.** Report blockers and propose changes instead |
| `report/` | Reports requested by the user | Yes — always in Vietnamese, plain non-technical language |
| `reference/` | Summaries: goals & vision, pipeline, workflow, project-specific terms | Yes — keep in sync when the source changes |
| `test/` | Test data provided by the user | Read and analyse only; edit only when the user explicitly asks |
| `temp/` | Scratch files for user and agent | Freely |
| `session_log/` | User decisions and agent changes per session | Yes — see *Session log* |

**Index rule.** Every subfolder has a `README.md` that contains only a heading and a mapping table `| Path | Description |` (short, precise description per file). Update it whenever a file is added, renamed or removed — this includes `project-requirements/` and `test/`, whose index is the only file an agent may edit there. Nothing else goes in the index.

**No leakage rule.** Tracked files (code, comments, specs, tests, commit messages, PR descriptions) must never reference specific content of `.local/` — no file names, numbers, quotes or paths into it. Only the framework files (`CLAUDE.md`, root `README.md`, `.gitignore`, `docs/workflow.md`, `.claude/**`) may describe the workspace *conventions*. If a spec needs information from `.local/`, restate the requirement in the spec itself.

## Implement plans

- Required for medium and large work. Created with the `plan` skill from `.claude/skills/plan/template.md`, saved as `.local/plan/YYYY-MM-DD_<slug>.md`, and indexed in the plan `README.md`.
- The header states the work level. Every section starts with a one-line summary (`> Tóm tắt: ...`). Required sections, in order:
  1. Nguyên nhân (cause)
  2. Phương án (approach)
  3. Phạm vi (scope)
  4. Tác động (impact)
  5. Lưu ý (caveats)
  6. Bảng file sẽ thay đổi (file change table)
  7. Checklist to do
  8. Tiêu chí nghiệm thu (acceptance criteria, each with its verification method)
- **After writing a plan, stop.** Never start implementing until the user approves it; then set its status to `approved`.

### Executing a plan

- Work the checklist top to bottom. Tick each item (`- [ ]` → `- [x]`) **immediately** after finishing it and before starting the next one.
- Never skip an item or tick ahead. The only exceptions need direct user approval in chat — e.g. running the whole flow end to end to get results, or a blocker that requires changing the plan. Mark an approved skip as `- [~] ... (skipped: <reason>, approved by user)`.
- On a blocker: stop, explain it, propose options, and wait. Changing the plan's content requires approval.

## Session log

Write or update a session log with the `session-log` skill whenever the user made decisions or files changed (a Stop hook reminds you). Small work gets one row in the table and needs no detail section. File: `.local/session_log/YYYY-MM-DD_<branch>_<topic>.md`, template in `.claude/skills/session-log/template.md`. Mandatory sections:

1. Git branch name
2. Completion time
3. Short cause leading to the decisions / changes
4. Table of decisions / changes
5. Short impact of the decisions / chosen change approach
6. Details of each decision / change

## Conventions

- Every verification artifact maps to an acceptance criterion: name or tag it with its `AC-n` id.
- Keep changes inside the approved plan's scope; list any extra file you had to touch in the session log.
- Commit only when the user asks. Commit messages describe the change itself, never local workspace content.
