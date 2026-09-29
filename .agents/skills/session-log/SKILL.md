---
name: session-log
description: Write or update the session log with the user's decisions and the agent's changes in this session. Use at the end of a working session, after completing a plan, or when the Stop hook asks for it.
---

Native Plan Mode: do not write any artifact, index or log. Present the requested output in chat; persist it only when writes are permitted and authorized. Follow AGENTS.md for shared rules and authorization; existing explicit approval covers the authorized workflow and its necessary status transitions.


# Write the session log

1. Collect facts: `git branch --show-current`, `git status --short`, the decisions the user made in chat, and the files you changed (with the plan items they belong to).
2. File: `.local/session_log/YYYY-MM-DD_<branch>_<topic>.md` (branch with `/` replaced by `-`). If a log for this session already exists, update it instead of creating a new one.
3. Fill [template.md](template.md). All six sections are mandatory:
   1. Git branch name
   2. Completion time (local time, `YYYY-MM-DD HH:mm`)
   3. Short cause leading to the decisions / changes
   4. Table of decisions / changes, with the work level of each change
   5. Short impact of the decisions / chosen change approach
   6. Details of each decision / change (matching the table ids)
4. Small work (see `AGENTS.md` → *Work levels and lifecycle*) gets one row in the table and no detail entry. Medium and large work get a detail entry including the verification evidence.
5. Record deviations from the plan (extra files, skipped items and who approved them).
6. Add or update the row in `.local/session_log/README.md`.

Use the existing actor column to identify Codex or Claude. Record the next unfinished plan item and existing approval evidence for handoff; do not invent approval.
