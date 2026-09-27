# Tests

Verification-first: every acceptance criterion declares how it is verified, and that verification is prepared before the work — and seen failing where possible. Automated tests (TDD) are the default for code; other domains use the method that fits.

## Verification methods

| Method | Use for | Artifact | "Red first" means |
|---|---|---|---|
| `test` | Code with deterministic logic | Test in `unit/` or `integration/` | The test runs and fails |
| `metric` | Data, ML, performance | Script in `metrics/` that computes the measure and checks the threshold | Threshold not met yet |
| `output-diff` | Pipelines, generated reports, CLIs | Expected output in `golden/` + comparison command | Current output differs |
| `manual` | UI, infrastructure, one-off operations | Checklist in `manual/`: numbered steps, expected result, evidence field | Steps written before the work |
| `review` | Documents, content, prompts | Checklist in `manual/` with the points a reviewer confirms | Checklist written before the work |

## Conventions

- Every artifact traces to an acceptance criterion: include `SPEC-<nnn>/AC-<n>` in the test name, script header, golden file name or checklist title.
- Keep input data under `fixtures/`. When user-provided sample data is needed, copy the relevant values into a fixture — verification never reads from the local workspace.
- Metric scripts print the measured value and exit non-zero when the threshold is not met, so they can run like tests.
- Do not delete or weaken a verification to make it pass; change it only when the spec changes.
- Run commands are defined in `CLAUDE.md` → *Project commands*.
- The default `.gitignore` excludes `*.csv`, `*.xlsx` and `*.docx`. Add exceptions (e.g. `!tests/**/*.csv`) if fixtures or golden files use these formats.

## Layout

Create only the folders the project needs:

```
tests/
  unit/          fast, isolated tests
  integration/   tests crossing module or process boundaries
  metrics/       measuring scripts with thresholds
  golden/        expected outputs for output-diff
  manual/        manual and review checklists
  fixtures/      static input data
```
