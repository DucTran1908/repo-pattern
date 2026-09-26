---
name: sync-reference
description: Refresh the project reference notes (goals & vision, pipeline, workflow, glossary of project-specific terms) in the local reference folder after the source changes. Use after finishing a plan or when the user asks to update the reference.
---

# Sync the reference notes

The reference folder is the quick-orientation layer for humans and agents. It holds four short summaries:

| File | Content |
|---|---|
| `.local/reference/vision.md` | Goals, vision, target users, success measures |
| `.local/reference/pipeline.md` | Data / processing pipeline: stages, inputs, outputs |
| `.local/reference/workflow.md` | How work flows through the repo (life cycle, commands, conventions actually in use) |
| `.local/reference/glossary.md` | Project-specific symbols, abbreviations and terms: `| Term | Meaning | Where used |` |

Steps:

1. Determine what changed (`git diff`, recent session logs, the plan just finished, specs in `specs/`).
2. Update only the affected files. Create a missing file with the structure above. Keep each file short — summaries, not copies of the code or specs.
3. Sources of truth win: if the reference disagrees with code or specs, fix the reference. If it disagrees with `.local/design_system/`, do not change either — report the conflict to the user.
4. Update `.local/reference/README.md` for any file added or removed.
