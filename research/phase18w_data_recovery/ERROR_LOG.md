# Phase 18W Error Log

No Phase 18W errors yet.

Known environment limitation: direct outbound internet from the local container is unavailable; web research is available and GitHub Actions is the intended execution environment for authenticated/public dataset acquisition.


## E18-001 — 2026-09-30
- **Issue:** Earlier HF-03 recovery attempts included a checkout race where `source_probe.py` was absent from the checked-out commit.
- **Impact:** The affected run exited before recovery; no data conclusion was drawn.
- **Correction:** The recovery workflow was corrected and later source-inventory runs completed successfully.

## E18-002 — 2026-09-30
- **Issue:** Multiple source-inventory runs successfully generated artifacts but their Git pushes were rejected because another process had advanced `phase-18w-data-recovery`.
- **Impact:** The workflow was marked failed after artifact generation; the source inventory itself was not treated as a data-recovery result.
- **Correction:** Later commits captured the generated inventories on the branch. HF-03 recovery is now serialized with a concurrency group.

## E18-003 — 2026-09-30
- **Issue:** A prior HF-03 run remained reported as `in_progress` with a stale timestamp while a clean replacement run was triggered.
- **Impact:** Its state cannot be treated as evidence of successful or failed recovery.
- **Correction:** A new recovery run was triggered from the latest branch commit with `cancel-in-progress: true`.


## E18-004 — 2026-09-30
- **Issue:** The serialized HF-03 recovery run remained `in_progress` in the 224-variant coverage step for substantially longer than expected, with no artifacts or live logs exposed.
- **Impact:** Recovery was not admitted and Phase 19 was correctly held. The state was treated as a performance/stall defect, not a data-quality conclusion.
- **Correction:** Replaced repeated full-DataFrame filtering inside the 224×63 loop with timestamp-level strike/open maps and direct dictionary lookups. The concurrency group remains enabled so the corrected commit supersedes the stale run.
