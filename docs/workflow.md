# Workflow

How humans and Claude Code work together in this repository. The binding rules for agents are in [`CLAUDE.md`](../CLAUDE.md); this page explains the flow.

## Life cycle

```
 ┌────────┐   ┌────────┐   ┌──────────┐   ┌───────────┐   ┌─────────────┐   ┌────────┐   ┌────────────────┐
 │  Spec  │──►│  Plan  │──►│ Approval │──►│ Test: red │──►│ Implement:  │──►│ Review │──►│ Log / Report / │
 │ (SDD)  │   │        │   │  (user)  │   │   (TDD)   │   │ green→refac │   │        │   │   Reference    │
 └────────┘   └────────┘   └──────────┘   └───────────┘   └─────────────┘   └────────┘   └────────────────┘
  spec          plan                        test-writer     implement /        reviewer     session-log,
  spec-writer                                               implementer                     report, sync-reference
```

1. **Spec** — describe the behaviour and its acceptance criteria in `specs/`.
2. **Plan** — the agent writes an implement plan with 8 sections (cause, approach, scope, impact, caveats, file table, checklist, acceptance criteria) into the local plan folder and stops.
3. **Approval** — the user reviews and approves the plan. Nothing is implemented before this.
4. **Test (red)** — failing tests are written from the acceptance criteria.
5. **Implement** — the checklist is executed top to bottom; each item is ticked as soon as it is done. Skipping requires the user's explicit approval.
6. **Review** — changes are checked against the acceptance criteria, the plan scope and the no-leakage rule.
7. **Log / Report / Reference** — the session log records decisions and changes; reports (Vietnamese, plain language) and reference notes are updated on request or when the source changes.

## Local workspace

`.local/` is git-ignored and recreated automatically at session start:

| Folder | What goes there | Who writes |
|---|---|---|
| `plan/` | Implement plans | Agent creates; edits need user approval (checklist ticks excepted) |
| `design_system/` | Raw requirements from the user | User only |
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
| `guard_local.py` | Before Edit / Write | Denies writes to `design_system/`, asks for `test/` and plan edits, lets in-order checklist ticks through, asks when tracked files reference `.local/` |
| `guard_shell.py` | Before Bash / PowerShell | Same protections for common shell writes; asks when a commit message mentions `.local/`; denies force-adding it |
| `session_log_check.py` | Stop | Asks the agent to update the session log when files changed after the last log |

Hooks need Python 3.8+ (`run-hook.sh` picks `python3`, `python` or `py`) and fail open if it is missing. Self-test: `python -m unittest discover .claude/hooks/tests`.
