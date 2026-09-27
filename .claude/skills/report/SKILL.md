---
name: report
description: Write a report requested by the user into the local report folder, always in Vietnamese with plain, non-technical wording so anyone can read it. Use when the user asks for a report, summary for stakeholders, or status update.
argument-hint: "<report topic>"
---

# Write a report

1. Clarify audience and topic if unclear. Gather facts from the code, tests, plans, session logs and `.local/test/` data (read-only).
2. Create `.local/report/YYYY-MM-DD_<slug>.md` from [template.md](template.md).
3. Writing rules — the report must be understandable by a non-engineer:
   - Vietnamese only.
   - Short sentences, everyday words. Avoid jargon; when a technical term is unavoidable, explain it in one plain phrase the first time.
   - Lead with the conclusion, then the supporting points. Prefer small tables and concrete numbers over long prose.
   - No code blocks, stack traces or file paths in the main text (put them in the appendix if really needed).
4. Add the report to `.local/report/README.md`.
