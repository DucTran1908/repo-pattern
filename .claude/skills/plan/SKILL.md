---
name: plan
description: Create an implement plan (8 required sections, checklist, acceptance criteria) and save it to the local plan folder, then stop for user approval. Use whenever the user asks for a plan or before any non-trivial implementation.
argument-hint: "<what to plan>"
---

# Create an implement plan

Never implement anything in this skill. The output is a plan file and a request for approval.

1. **Understand.** Read the request, the related spec in `specs/`, relevant code, `.local/reference/` and (read-only) `.local/design_system/`. Ask the user about genuinely open decisions before writing.
2. **Write.** Copy [template.md](template.md) to `.local/plan/YYYY-MM-DD_<slug>.md` (today's date, kebab-case slug). Rules:
   - Keep all 8 sections in order. Each starts with a one-line `> Tóm tắt:` summary.
   - Section 6 lists every file to add / modify / delete.
   - Section 7 checklist: small, verifiable items `- [ ] T1. ...`, ordered so they can be ticked top to bottom; test items come before the implementation items they cover (TDD).
   - Section 8 acceptance criteria are a numbered list (not checkboxes) and reference spec `AC-n` ids when a spec exists.
   - Fill in the current branch (`git branch --show-current`) and set `Status: draft`.
3. **Index.** Add the plan to `.local/plan/README.md` (`| path | short description |`).
4. **Stop.** Summarise the plan in chat and ask the user to approve. Do not start implementation in the same turn.

Editing an existing plan (other than ticking checklist items) requires the user's approval — the guard hook will prompt for it.
