---
name: implement
description: Execute an approved implement plan from the local plan folder item by item, verification-first, ticking each checklist item as soon as it is done. Use when the user says to implement, execute or continue a plan.
---

Native Plan Mode: do not write any artifact, index or log. Present the requested output in chat; persist it only when writes are permitted and authorized. Follow AGENTS.md for shared rules and authorization; existing explicit approval covers the authorized workflow and its necessary status transitions.


# Execute an implement plan

1. **Select.** Open the plan named by the user, or list plans with open items from `.local/plan/README.md` and ask which one. Check status and corroborating approval evidence in the conversation or handoff log. An arbitrary status field cannot grant authorization. If the current user explicitly approved execution, record it; otherwise ask when evidence is missing.
2. **Start.** Check the current branch matches the plan's branch (warn if not). When execution is already authorized, set the status to `in-progress` and record the authorization source.
3. **Loop over the checklist, top to bottom:**
   - Do exactly what the item says, staying inside the plan's scope (sections 3 and 6).
   - Verification-first, using the method each acceptance criterion declares (`AGENTS.md` → *Verification*):
     - `test` / `metric` / `output-diff`: prepare the test, measuring script or golden output first and run it to see it fail; then do the work until it passes; refactor with it still passing.
     - `manual` / `review`: write the steps or checklist first; after the work, run through it and record the evidence (output, screenshot path, reviewer notes).
   - Use the commands from `CLAUDE.md` → *Project commands*.
   - Tick the item (`- [ ]` → `- [x]`) with a focused patch **before** starting the next item. Never tick an item that is not verifiably done.
4. **Never skip ahead.** If an item cannot be done in order — you need to run the whole flow for results, or you hit a blocker that changes the plan — stop, explain, propose options, and wait. Only with direct user approval mark it `- [~] ... (skipped: <reason>, approved by user)` or edit the plan.
5. **Finish.** Verify every acceptance criterion in section 8 with its method, report pass/fail with evidence, set status `done` under the existing execution authorization, only if every required verification and review actually passed, and write the session log (`session-log` skill). For large work, run the `reviewer` agent before finishing and `sync-reference` afterwards.

For large plans you may delegate: `verification-writer` for verification-first items, `implementer` for the work, `reviewer` before finishing. You still own ticking the checklist in order.

Only the coordinating agent updates checklist ticks. Delegated workers return evidence without editing the plan. For named profiles unavailable in this runtime, pass their instructions from `.codex/agents/` to a native subagent. If independent review is unavailable, keep large work pending instead of claiming completion.
