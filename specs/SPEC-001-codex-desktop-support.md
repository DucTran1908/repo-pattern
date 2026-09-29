# SPEC-001: Codex desktop support

- Status: approved
- Owner: project maintainer
- Created: 2026-09-27
- Related plans / PRs: implementation authorized by the user in chat; no PR

## Goal
Allow Claude Code and Codex desktop on Windows to work alternately in one checkout, with equivalent development disciplines and interoperable artifacts.

## Context
The template already implements SDD, verification-first and ADLC for Claude Code. Codex needs independent instructions, skills, agent profiles and native hook adapters. The user approved this specification's requirements and acceptance criteria as part of the implementation request.

## Requirements
- R-1: Preserve work levels, approval boundaries, ordered checklists, verification methods, artifact formats and commit-on-request behavior.
- R-2: Provide six independent skills and four agent roles. Reuse the existing project command table, never invent commands still marked TODO.
- R-3: Share working artifacts between tools; do not require simultaneous writers or new workflow stages.
- R-4: Enforce supported prohibitions through native hooks; distinguish advisory approval reminders from enforced decisions.
- R-5: Keep Plan Mode non-mutating and document inactive hooks, trust requirements and runtime limitations.
- R-6: Detect unreviewed drift in either instruction set without automatic synchronization.
- R-7: Restrict Claude changes to framework exceptions and corresponding regression tests.

## Out of scope
Cloud, concurrent writers, worktree transfer, new application stack, plugins, MCP services, global settings changes and model selection.

## Acceptance criteria

| ID | Criterion | Method | How it is verified |
|---|---|---|---|
| AC-1 | Desktop discovers project instructions and all six skills. | manual | Fresh desktop task and invocation of each skill. |
| AC-2 | Plans, logs, specs and indexes retain compatible structure and identifiers. | review | Compare templates and workflow contracts. |
| AC-3 | Both tools resume the same next unfinished item without duplicate work. | manual | Claude to Codex to Claude exercise using disposable artifacts. |
| AC-4 | Guards reject supported forbidden writes and handle multi-file patches and Windows paths. | test | Isolated temporary-repository hook tests. |
| AC-5 | Approval reminders never emit unsupported ask decisions or infer authorization from files. | test | Decision and adversarial-payload cases; desktop advisory smoke check. |
| AC-6 | Plan Mode causes no bootstrap or logging writes. | test | Filesystem snapshots and desktop read-only exercise. |
| AC-7 | Existing Claude protections do not regress. | test | Existing hook suite plus Codex framework exception cases. |
| AC-8 | Source or target instruction drift fails the compatibility check. | test | Mutate isolated fixtures; normalize newline-only differences. |
| AC-9 | Large work receives independent read-only review. | manual | Review output with findings and verification evidence. |
| AC-10 | Integration adds no production dependency, global setting or eager context expansion. | review | Inspect config, imports, discovery and documented limits. |

## Open questions
None. Live desktop discovery and cross-tool smoke checks require runtime evidence before being marked passed.
