# Phase 21W Research Log

## 2026-09-30 — E21-013 validation run
- Schema correction reached combined-input construction but a GitHub runner shutdown occurred.

## 2026-09-30 — E21-015 coverage-contract correction
- Bounded-memory build produced 11,702 combined cells; the executable set covered 58 of the 63 frozen expiries.
- Validation was corrected to distinguish the 63-cycle denominator from the executable subset and five missing expiries.

## 2026-09-30 — E21-016/E21-017 interface-path corrections
- Restored Phase-9 artifacts were moved under research/ and the builder baseline manifest path was aligned to that interface.

## 2026-09-30 — E21-018 repository persistence limit
- The exact backtest succeeded but the 346.32 MB combined parquet exceeded GitHub's 100 MB single-file limit.
- Compact outputs are committed and the full parquet is retained in the workflow artifact.

## 2026-09-30 — E21-019 exact frozen rerun closure
- Workflow run 36709664677 completed combined build, coverage validation, exact 224-variant backtest/statistics, artifact upload and compact-result commit successfully.
- Combined coverage: 11,702/14,112 cells (82.93%), 58 covered expiries, 5 missing expiries, zero source overlap, zero duplicate groups.
- Across 224 variants, zero had Holm-adjusted training p < 0.05 and zero were promoted to capital phase.
- Phase 21W combined rerun is closed. The missing-five data question is carried to the external full-strike recovery phase.