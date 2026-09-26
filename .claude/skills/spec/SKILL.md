---
name: spec
description: Write or update a feature spec in specs/ (Spec-Driven Development) with numbered acceptance criteria. Use when the user describes a new feature, a behaviour change, or asks for a spec before planning.
argument-hint: "<feature description>"
---

# Write a spec

1. Read the user's request and the relevant inputs in `.local/design_system/` (read-only) and `.local/reference/`. If requirements conflict or are missing, list them as open questions — never edit `design_system/`.
2. Pick the next free id from `specs/README.md` (`SPEC-001`, `SPEC-002`, …) and a short kebab-case slug.
3. Create `specs/<id>-<slug>.md` from [template.md](template.md). Fill every section:
   - Acceptance criteria are numbered `AC-1`, `AC-2`, … and each one must be observable and testable.
   - Restate any needed detail from local inputs in your own words — never link or quote `.local/` paths (no-leakage rule).
4. Add a row to the index table in `specs/README.md`.
5. Show the user the acceptance criteria and open questions. Set `Status: approved` only after the user confirms.
