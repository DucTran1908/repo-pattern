# Tests

Test-Driven Development: tests are written from acceptance criteria and must fail before the implementation exists.

## Conventions

- Every test traces to an acceptance criterion: include `SPEC-<nnn>/AC-<n>` in the test name, docstring or tag.
- Red → green → refactor. A new test is committed only after it has been seen failing for the right reason.
- Keep fixtures under `tests/fixtures/`. When user-provided sample data is needed, copy the relevant values into a fixture — tests never read from the local workspace.
- Do not delete or weaken a test to make it pass; change it only when the spec changes.
- Run commands are defined in `CLAUDE.md` → *Project commands*.

## Layout

Adapt to the chosen stack, e.g.:

```
tests/
  unit/          fast, isolated tests
  integration/   tests crossing module or process boundaries
  fixtures/      static test data
```
