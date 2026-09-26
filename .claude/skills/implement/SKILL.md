---
name: implement
description: Execute an approved implement plan from the local plan folder item by item with TDD, ticking each checklist item as soon as it is done. Use when the user says to implement, execute or continue a plan.
argument-hint: "[plan file name]"
---

# Execute an implement plan

1. **Select.** Open the plan named by the user, or list plans with open items from `.local/plan/README.md` and ask which one. Confirm its status is `approved` (or `in-progress`). If it is `draft`, stop and ask for approval.
2. **Start.** Check the current branch matches the plan's branch (warn if not). With user approval, set the status to `in-progress`.
3. **Loop over the checklist, top to bottom:**
   - Do exactly what the item says, staying inside the plan's scope (section 3 and 6).
   - TDD: write the failing test first and run it (red), then implement until it passes (green), then refactor with tests still green. Use the commands from `CLAUDE.md` → *Project commands*.
   - Tick the item (`- [ ]` → `- [x]`) with a single Edit **before** starting the next item. Never tick an item that is not verifiably done.
4. **Never skip ahead.** If an item cannot be done in order — you need to run the whole flow for results, or you hit a blocker that changes the plan — stop, explain, propose options, and wait. Only with direct user approval mark it `- [~] ... (skipped: <reason>, approved by user)` or edit the plan.
5. **Finish.** Verify every acceptance criterion in section 8, report pass/fail with evidence, set status `done` (with approval), and write the session log (`session-log` skill). Run `sync-reference` if the change affects vision, pipeline, workflow or terminology.

For large plans you may delegate: `test-writer` for red tests, `implementer` for green/refactor, `reviewer` before finishing. You still own ticking the checklist in order.
