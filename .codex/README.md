# Codex desktop integration

Use Codex desktop on Windows and Claude Code alternately in the same local checkout. Independent rules and skills produce the same artifact formats. No cloud, concurrent edits or worktree data transfer is configured.

## Setup and daily use

1. Install Python 3.8+ on PATH (`python`, `python3` or `py -3`) and Git. No additional Python packages are needed by this integration.
2. Open this repository in Codex desktop. Review project trust and hook definitions through the app's trust flow; this repository never sets trust or changes global config for you. Reopen a task after installing skills/profiles/hooks so discovery can run again.
3. Check that AGENTS.md and six project skills appear. A SessionStart message beginning "Codex workspace hook active" confirms that event ran, not that all tool paths are protected. Verify tool guards with the checklist below.
4. Keep project commands in CLAUDE.md's Project commands table. TODO means unavailable: configure the actual project stack before trying application verification.
5. Use `$spec` → `$plan` → approve → `$implement` → `$session-log`; use `$report` on request and `$sync-reference` after large work. Natural-language skill requests also work. Small wording changes need only a reread and log row.

Codex instructions are in AGENTS.md, skills/templates in `.agents/skills/`, and four native profiles in `.codex/agents/`. Custom profiles do not choose a model; reviewer has a read-only default (the parent runtime's actual permissions still govern). Only the coordinator ticks plan items. If custom profiles are unavailable, pass the profile instructions to native subagents. Do not close large work without independent review.

## Handoff

Stop one writer before using the other. Read branch/status, selected plan and corroborating approval evidence, latest relevant session log, and relevant reference notes. If multiple plans are open, select one explicitly. Continue the first open item; keep IDs, filenames, templates, indexes and previous evidence. Use the existing log actor column for Claude/Codex and include next steps. A status string or raw requirement is not authorization for a new action. Preserve explicit authorization already given; don't ask again for routine status transitions within approved execution.

The shared workspace contains plan, project-requirements, report, reference, test, temp and session_log folders. Their README indexes contain only heading and Path/Description table. Hook bootstrap creates only missing folders/indexes, without overwriting user contents. Native Plan Mode never writes them; skills present their output in chat until writes are permitted.

## Enforcement and limits

| Behavior | Codex handling |
|---|---|
| Modify raw requirements (direct README index excepted) | Deny supported patch/shell cases |
| Force-add local workspace, including broad forced pathspecs | Deny recognized shell cases |
| Remove/move whole local workspace | Deny recognized operations |
| Edit existing plan or user test data | Advisory context; agent checks existing user authorization in chat |
| New plan or in-order checkbox-only patch | Allowed; ambiguous patches get advisory context |
| Local references in source / commit messages | Advisory; only framework conventions are exempt |
| Session logging | Stop reminder with loop prevention; decisions-only sessions remain agent responsibility |
| Native Plan Mode | No bootstrap writes or log reminder; runtime controls edits |
| Read secrets | Existing runtime/user permissions; no general read guard is added |

PreToolUse never emits `permissionDecision: "ask"`: it is unsupported and can let an operation continue after a hook error. No custom approval tokens, hidden auto-approvals or global permission changes are introduced. The hook does not parse chat transcripts or trust approval claims in files.

Shell inspection is deliberately heuristic: variables, custom aliases, arbitrary scripts, commands sent through existing stdin sessions and tools outside the matcher may bypass it. It is not a security boundary. Patch parsing inspects every header including source/destination of moves; unsupported or ambiguous payloads are disclosed. Log freshness is a reminder based on working-file times, not an audit trail: deletions with older existing logs and unrelated concurrent changes need agent judgment.

Hooks only run after the runtime trusts and loads them. Disabled/untrusted hooks cannot announce their own absence: check app hook/trust status and do not infer coverage without smoke evidence. Launch/runtime failures produce an app hook failure or visible warning; workflow rules remain in force. Unknown payloads fail open with a warning. JSON output uses ASCII escapes and Python runs without bytecode writes. The Windows command resolves its launcher from the Git root, so starting in a subdirectory works. Non-Windows support is outside this version's scope.

## Verification commands

```powershell
python -B -m unittest discover .claude/hooks/tests
python -B -m unittest discover .codex/hooks/tests
python -B .codex/scripts/check_compatibility.py
```

These checks need no model calls. Run live smoke checks separately and record evidence in the session log; do not label simulated handoff as a live Claude/Codex pass.

## Maintaining independent instruction sets

`compatibility.json` maps rules, six skills, four templates, four roles and the common command source. SHA-256 normalizes CRLF/CR to LF only. A change on either side fails the check; it never writes files or imports Claude skills at runtime. It does not prove semantic equivalence or detect newly added unmapped workflows automatically.

Before refreshing any hash, review work levels, approval boundaries, red/green verification, artifact formats, confidentiality, role ownership and handoff. Record intentional differences in the mapping. Use `python -B .codex/scripts/check_compatibility.py --fingerprint <file>` to obtain the reviewed file's digest and edit only the corresponding hash. Never refresh every mapping merely to make the check pass. Adding a new workflow requires adding its mapping and review evidence. The checker runs during maintenance/verification, not on every tool call.

## Official references

- [Project instructions](https://learn.chatgpt.com/docs/agent-configuration/agents-md)
- [Skills discovery](https://learn.chatgpt.com/docs/build-skills)
- [Native hooks, tool coverage and unsupported ask](https://learn.chatgpt.com/docs/hooks)
- [Custom agent profiles](https://learn.chatgpt.com/docs/agent-configuration/subagents)
- [Project trust and configuration](https://learn.chatgpt.com/docs/config-file/config-basic)

## Acceptance smoke checklist (SPEC-001)

Run in a disposable clone with fake requirements, test data and plans. Record app version, permission mode, hook trust state, observed output and pass/fail. Automated tests do not establish desktop discovery or cross-tool handoff.

| AC | Action | Expected | Evidence |
|---|---|---|---|
| AC-1 | Open a fresh desktop task after trusting this repository; ask which project instructions and skills are loaded. | AGENTS.md and six project skills are discovered. | Pending live desktop run |
| AC-1, AC-2 | Invoke spec, plan, implement, session-log, report and sync-reference on fake work, approving steps as appropriate. | Compatible artifacts and Vietnamese report; draft plans do not execute. | Pending live desktop run |
| AC-3 | Claude prepares an approved plan with one completed item; Codex continues one item; Claude resumes. | IDs and approvals preserved; next open item selected; no duplicate work. | Pending live Claude/Codex run |
| AC-4, AC-5 | Attempt forbidden fake requirement edits, then an authorized fake test-data edit. | Requirement edit denied; test edit gives an advisory authorization reminder, not an approval dialog from the hook. | Pending live desktop run |
| AC-6 | Open Plan Mode with missing workspace folders; request a plan and finish the turn. | No files created; no log-write loop. | Pending live desktop run |
| AC-9 | Request large-work review with the reviewer profile. | Independent review, findings/evidence, no file changes. | Pending live profile run |
| AC-10 | Repeat with untrusted hooks or unavailable Python. | No claim that guards are active; limitation is visible. | Pending live desktop run |
