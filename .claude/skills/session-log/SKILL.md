---
name: session-log
description: Write or update the session log with the user's decisions and the agent's changes in this session. Use at the end of a working session, after completing a plan, or when the Stop hook asks for it.
---

# Write the session log

1. Collect facts: `git branch --show-current`, `git status --short`, the decisions the user made in chat, and the files you changed (with the plan items they belong to).
2. File: `.local/session_log/YYYY-MM-DD_<branch>_<topic>.md` (branch with `/` replaced by `-`). If a log for this session already exists, update it instead of creating a new one.
3. Fill [template.md](template.md). All six sections are mandatory:
   1. Git branch name
   2. Completion time (local time, `YYYY-MM-DD HH:mm`)
   3. Short cause leading to the decisions / changes
   4. Table of decisions / changes
   5. Short impact of the decisions / chosen change approach
   6. Details of each decision / change (matching the table ids)
4. Record deviations from the plan (extra files, skipped items and who approved them).
5. Add or update the row in `.local/session_log/README.md`.
