# Specs

Spec-Driven Development: every feature or behaviour change starts here, before any plan or code.

## Conventions

- One file per feature: `SPEC-<nnn>-<slug>.md`, created with the `spec` skill from `.claude/skills/spec/template.md`.
- Ids are sequential and never reused. Deprecated specs stay in place with `Status: deprecated`.
- Required for large work (see `CLAUDE.md` → *Work levels*); optional for medium work, which updates the affected criteria of an existing spec when behaviour changes.
- Acceptance criteria are numbered `AC-1`, `AC-2`, … inside each spec, each with a verification method (`test`, `metric`, `output-diff`, `manual`, `review`), and referenced by verification artifacts as `SPEC-<nnn>/AC-<n>`.
- A spec is self-contained: restate every requirement in the spec itself instead of pointing to local working files.
- Status flow: `draft` → `approved` (user confirmed) → `implemented` → `deprecated`.

## Index

| Id | Title | Status |
|---|---|---|
| SPEC-001 | Codex desktop support | approved |
