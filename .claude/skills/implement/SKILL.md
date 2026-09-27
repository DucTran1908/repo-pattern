---
name: implement
description: Execute an approved implement plan from the local plan folder item by item, verification-first, ticking each checklist item as soon as it is done. Use when the user says to implement, execute or continue a plan.
argument-hint: "[plan file name]"
---

# Execute an implement plan

1. **Select.** Open the plan named by the user, or list plans with open items from `.local/plan/README.md` and ask which one. Confirm its status is `approved` (or `in-progress`). If it is `draft`, stop and ask for approval.
2. **Start.** Check the current branch matches the plan's branch (warn if not). With user approval, set the status to `in-progress`.
3. **Loop over the checklist, top to bottom:**
   - Do exactly what the item says, staying inside the plan's scope (sections 3 and 6).
   - Verification-first, using the method each acceptance criterion declares (`CLAUDE.md` → *Verification methods*):
     - `test` / `metric` / `output-diff`: prepare the test, measuring script or golden output first and run it to see it fail; then do the work until it passes; refactor with it still passing.
     - `manual` / `review`: write the steps or checklist first; after the work, run through it and record the evidence (output, screenshot path, reviewer notes).
   - Use the commands from `CLAUDE.md` → *Project commands*.
   - Tick the item (`- [ ]` → `- [x]`) with a single Edit **before** starting the next item. Never tick an item that is not verifiably done.
4. **Never skip ahead.** If an item cannot be done in order — you need to run the whole flow for results, or you hit a blocker that changes the plan — stop, explain, propose options, and wait. Only with direct user approval mark it `- [~] ... (skipped: <reason>, approved by user)` or edit the plan.
5. **Finish.** Verify every acceptance criterion in section 8 with its method, report pass/fail with evidence, set status `done` (with approval), and write the session log (`session-log` skill). For large work, run the `reviewer` agent before finishing and `sync-reference` afterwards.

For large plans you may delegate: `verification-writer` for verification-first items, `implementer` for the work, `reviewer` before finishing. You still own ticking the checklist in order.
