---
name: plan
description: Create an implement plan (8 required sections, checklist, acceptance criteria with verification methods) and save it to the local plan folder, then stop for user approval. Use whenever the user asks for a plan and before any medium or large work.
---

Native Plan Mode: do not write any artifact, index or log. Present the requested output in chat; persist it only when writes are permitted and authorized. Follow AGENTS.md for shared rules and authorization; existing explicit approval covers the authorized workflow and its necessary status transitions.


# Create an implement plan

Never implement anything in this skill. The output is a plan (in chat during native Plan Mode; otherwise a file) awaiting user approval.

0. **Level.** Classify the work (`AGENTS.md` → *Work levels and lifecycle*). Small work needs no plan — tell the user and do it directly unless they still want a plan. Large work needs an approved spec first (`spec` skill).
1. **Understand.** Read the request, the related spec in `specs/`, relevant code, `.local/reference/` and (read-only) `.local/project-requirements/`. Ask the user about genuinely open decisions before writing.
2. **Write.** Copy [template.md](template.md) to `.local/plan/YYYY-MM-DD_<slug>.md` (today's date, kebab-case slug). Rules:
   - Fill in the level, the current branch (`git branch --show-current`) and `Status: draft`.
   - Keep all 8 sections in order. Each starts with a one-line `> Tóm tắt:` summary.
   - Section 6 lists every file to add / modify / delete.
   - Section 7 checklist: small, verifiable items `- [ ] T1. ...`, ordered so they can be ticked top to bottom; verification items come before the work they verify (verification-first).
   - Section 8 is a table: each criterion has an id (the spec's `AC-n` when a spec exists), a method (`test`, `metric`, `output-diff`, `manual`, `review`) and how it is verified.
3. **Index.** Add the plan to `.local/plan/README.md` (`| path | short description |`).
4. **Stop.** Summarise the plan in chat and await user approval. Do not start implementation without it; an explicit implementation request for an already approved plan uses the implement skill.

Editing an existing plan (other than ticking checklist items) requires the user's approval — Codex hooks only remind; the agent checks authorization in the conversation.
