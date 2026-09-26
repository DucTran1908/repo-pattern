# Specs

Spec-Driven Development: every feature or behaviour change starts here, before any plan or code.

## Conventions

- One file per feature: `SPEC-<nnn>-<slug>.md`, created with the `spec` skill from `.claude/skills/spec/template.md`.
- Ids are sequential and never reused. Deprecated specs stay in place with `Status: deprecated`.
- Acceptance criteria are numbered `AC-1`, `AC-2`, … inside each spec and referenced by tests as `SPEC-<nnn>/AC-<n>`.
- A spec is self-contained: restate every requirement in the spec itself instead of pointing to local working files.
- Status flow: `draft` → `approved` (user confirmed) → `implemented` → `deprecated`.

## Index

| Id | Title | Status |
|---|---|---|
