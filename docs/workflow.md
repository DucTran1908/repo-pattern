# Workflow

How humans and Claude Code work together in this repository. The binding rules for agents are in [`CLAUDE.md`](../CLAUDE.md); this page explains the flow.

## Work levels

Every task is first classified; the level decides how much process it needs.

| Level | Examples | What happens |
|---|---|---|
| Small | Typo fixes, translating prompts / reports / plans, rewording docs, formatting | Done directly, no plan; one row in the session log |
| Medium | Bug fix, behaviour change in one module, refactor, rename | Plan → approval → verification-first → implement → self-review → log |
| Large | New feature, cross-module or architecture change, schema / public interface / dependency change, data migration or deletion | Spec → plan → approval → verification-first → implement → `reviewer` agent → log → reference sync |

## Life cycle (medium and large work)

```
 ┌────────┐   ┌────────┐   ┌──────────┐   ┌──────────────┐   ┌─────────────┐   ┌────────┐   ┌────────────────┐
 │  Spec  │──►│  Plan  │──►│ Approval │──►│ Verify-first │──►│ Implement:  │──►│ Review │──►│ Log / Report / │
 │ (SDD)  │   │        │   │  (user)  │   │    (red)     │   │ green→refac │   │        │   │   Reference    │
 └────────┘   └────────┘   └──────────┘   └──────────────┘   └─────────────┘   └────────┘   └────────────────┘
  spec          plan                        verification-      implement /        reviewer     session-log,
  spec-writer                               writer             implementer                     report, sync-reference
```

1. **Spec** — describe the behaviour and its acceptance criteria in `specs/`, each with a verification method (required for large work).
2. **Plan** — the agent writes an implement plan with 8 sections (cause, approach, scope, impact, caveats, file table, checklist, acceptance criteria) into the local plan folder and stops.
3. **Approval** — the user reviews and approves the plan. Nothing is implemented before this.
4. **Verify-first** — the verification for each criterion is prepared before the work and seen failing where possible.
5. **Implement** — the checklist is executed top to bottom; each item is ticked as soon as it is done. Skipping requires the user's explicit approval.
6. **Review** — changes are checked against the acceptance criteria, the verification evidence, the plan scope and the no-leakage rule.
7. **Log / Report / Reference** — the session log records decisions and changes; reports (Vietnamese, plain language) and reference notes are updated on request or when the source changes.

## Verification methods

Not every domain has unit tests, so each acceptance criterion picks the method that fits:

| Method | Typical domain | Example |
|---|---|---|
| `test` | Application code | Unit / integration test |
| `metric` | Data, ML, performance | `accuracy >= 0.90` on a fixed evaluation set |
| `output-diff` | Pipelines, generated reports, CLIs | Output equals the golden file |
| `manual` | UI, infrastructure | Written steps with expected results, evidence recorded |
| `review` | Documents, content, prompts | Written review checklist |

## Local workspace

`.local/` is git-ignored and recreated automatically at session start:

| Folder | What goes there | Who writes |
|---|---|---|
| `plan/` | Implement plans | Agent creates; edits need user approval (checklist ticks excepted) |
| `project-requirements/` | Raw requirements from the user | User only |
| `report/` | Requested reports, in Vietnamese | Agent |
| `reference/` | Vision, pipeline, workflow, glossary summaries | Agent, kept in sync with the source |
| `test/` | Test data from the user | User (agent only on explicit request) |
| `temp/` | Scratch files | Anyone |
| `session_log/` | Decisions and changes per session | Agent |

Each folder has a `README.md` index (path + short description) and nothing else in it.

## Enforcement

Rules are written in `CLAUDE.md` and backed by hooks in `.claude/hooks/` (registered in `.claude/settings.json`):

| Hook | Event | Effect |
|---|---|---|
| `bootstrap_local.py` | SessionStart | Creates missing workspace folders and indexes; reports the branch and plans with open items |
| `guard_local.py` | Before Edit / Write | Denies writes to `project-requirements/`, asks for `test/` and plan edits, lets in-order checklist ticks through, asks when tracked files reference `.local/` |
| `guard_shell.py` | Before Bash / PowerShell | Same protections for common shell writes; asks when a commit message mentions `.local/`; denies force-adding it |
| `session_log_check.py` | Stop | Asks the agent to update the session log when files changed after the last log |

Hooks do not know the work level, so small edits to protected files (e.g. translating a plan) still show an approval prompt.

Hooks need Python 3.8+ (`run-hook.sh` picks `python3`, `python` or `py`) and fail open if it is missing. Self-test: `python -m unittest discover .claude/hooks/tests`.
