# Phase 18W Error Log

Known environment limitation: direct outbound internet from the local container is unavailable; GitHub Actions is the intended execution environment for authenticated/public dataset acquisition.

## E18-001 — 2026-09-30
- **Issue:** Earlier HF-03 recovery attempts included a checkout race where `source_probe.py` was absent from the checked-out commit.
- **Impact:** The affected run exited before recovery; no data conclusion was drawn.
- **Correction:** The recovery workflow was corrected and later source-inventory runs completed successfully.

## E18-002 — 2026-09-30
- **Issue:** Multiple source-inventory runs generated artifacts but their Git pushes were rejected because another process had advanced `phase-18w-data-recovery`.
- **Impact:** Those workflows were marked failed after artifact generation; the inventories were not treated as empirical recovery results until committed.
- **Correction:** Later commits captured the inventories. HF-03 recovery was serialized with a concurrency group.

## E18-003 — 2026-09-30
- **Issue:** A prior HF-03 run remained reported as `in_progress` with a stale timestamp while a clean replacement run was triggered.
- **Impact:** Its state could not be treated as evidence of successful or failed recovery.
- **Correction:** A new recovery run was triggered from the latest branch commit with serialized execution.

## E18-004 — 2026-09-30
- **Issue:** The first serialized HF-03 recovery remained in the 224-variant coverage step for substantially longer than expected, with no artifacts or live logs exposed.
- **Impact:** Recovery was not admitted and Phase 19 was correctly held. The state was treated as a performance/stall defect, not a data-quality conclusion.
- **Correction:** Replaced repeated full-DataFrame filtering inside the 224×63 loop with timestamp-level strike/open maps and direct dictionary lookups.

## E18-005 — 2026-09-30
- **Issue:** The original long-running recovery attempt (workflow run 36631329113) ended cancelled before producing artifacts.
- **Impact:** No empirical coverage conclusion was taken from that run.
- **Correction:** The optimized recovery implementation was executed separately; workflow run 36635955194 completed successfully and produced the admitted coverage report.
