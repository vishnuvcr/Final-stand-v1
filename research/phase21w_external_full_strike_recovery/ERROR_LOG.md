# Phase 21W External Recovery Error Log

## Resolved during resume

### E21X-001 — Recovery scope was broader than the actual unresolved set
- **Observed:** Older phase text described a larger missing-cycle population.
- **Correction:** Read the frozen Phase 21 combined coverage.json and narrowed the live recovery target to exactly five missing expiries.
- **Prevention:** Future source probes must derive their target set from the latest frozen coverage contract.

### E21X-002 — External recovery initially attempted to rebuild the spot interface
- **Observed:** The first recovery script draft downloaded a second NIFTY spot source.
- **Correction:** Changed the script to consume the exact frozen Phase 9 selected spot-bar artifact instead.
- **Reason:** Avoids changing the spot source while recovering only option bars.
- **Prevention:** External recovery may replace only the explicitly missing option-cycle cells.

### E21X-003 — Workflow output path mismatch
- **Observed:** The merge script initially wrote the Phase 9 interface outside the final-input directory.
- **Correction:** Changed the destination to work/final_input/phase9_weekly/output.
- **Prevention:** Final rerun validates all required interface paths before execution.

### E21X-004 — Workflow commit identity typo
- **Observed:** The first workflow draft contained a malformed bot email.
- **Correction:** Replaced it with the standard github-actions bot noreply address.
- **Prevention:** Workflow YAML is compiled/validated before the research run.

## Open risks

### E21X-005 — RISSIN schema/timestamp compatibility
- **Risk:** The public dataset's timestamp representation may require parsing/normalization on the runner.
- **Control:** Recovery script validates exact 10:00/14:00 bars, duplicate keys and all 224 variants for each target before admission.

### E21X-006 — RISSIN strike coverage
- **Risk:** The dataset card warns that some illiquid/far strikes can be sparse.
- **Control:** Every one of the 224 variants must pass exact entry/lock coverage on all five targets; otherwise the route is rejected rather than patched.

## E21X-007 — 2026-09-30
- **Issue:** Public-HF probe run 36711279624 failed with HTTP 404 because the pinned Rissin revision `78b1c54` did not contain `upstox_intraday/NIFTY/NIFTY_2026.parquet`.
- **Impact:** No empirical recovery result was produced.
- **Correction:** Resolve the current dataset `main` revision at run start, discover the exact NIFTY 2026 parquet, and record the resolved commit SHA and file SHA-256.
- **Prevention:** Validate required-file existence at the actual revision before freezing a public-source pin.

## E21X-008 — 2026-09-30
- **Issue:** The public-HF and full-recovery workflows used broad branch push triggers, causing redundant concurrent runs when research logs/output commits were made.
- **Impact:** Several runs were cancelled by concurrency before reaching the data-recovery step.
- **Correction:** Restrict push triggers to source-code/configuration paths; output commits no longer self-trigger the research workflows. Manual dispatch remains enabled.
- **Prevention:** All large-data workflows must be event-filtered to exclude generated outputs from push triggers.


### E21X-007 — Cross-workflow GitHub CLI artifact lookup rejected
- **Observed:** The first external-recovery workflow used gh run list with the workflow-scoped token and received HTTP 401 Bad credentials.
- **Correction:** Removed direct gh API lookup and replaced it with dawidd6/action-download-artifact@v25, which resolves the latest successful workflow artifact by workflow, branch and artifact name.
- **Prevention:** Cross-workflow artifact transfer now uses a dedicated artifact action and explicit actions:read permission rather than a shell API lookup.


### E21X-008 — Separate Phase 9 artifact lookup was unnecessary and unavailable
- **Observed:** The external workflow could not find a successful standalone Phase 9 artifact on its branch.
- **Correction:** Verified that the successful Phase 21 combined artifact already contains the exact Phase 9 weekly manifest and selected spot bars. The workflow now reuses those embedded frozen files.
- **Prevention:** Prefer the newest already-admitted composite artifact when it contains all required frozen interfaces; do not add redundant cross-workflow dependencies.


### E21X-009 — Baseline calendar lookup pointed at the wrong artifact subdirectory
- **Observed:** The first actual RISSIN recovery attempt stopped before Python execution because the combined artifact stores baseline_calendar.json under the Phase 21 output directory, not combined_input.
- **Correction:** Updated the workflow lookup to search the artifact output directory.
- **Prevention:** Artifact paths are now derived from the exact upload manifest of the successful Phase 21 combined workflow.


### E21X-010 — RISSIN parquet timezone metadata was rejected by Polars
- **Observed:** The RISSIN NIFTY 2026 parquet declares a +05:30 timezone that the runner's Polars timezone database did not accept during lazy schema collection.
- **Correction:** Enabled the same POLARS_IGNORE_TIMEZONE_PARSE_ERROR compatibility setting already used by the frozen Phase 9 ingestion code.
- **Prevention:** Keep timezone normalization explicit in the recovery script and retain the runner compatibility environment setting.

## E21X-011 — 2026-09-30
- **Issue:** Rissin recovery reached source loading after the timezone parser fix, but Polars compared Asia/Kolkata timestamp columns with Python datetimes interpreted as UTC.
- **Impact:** Recovery stopped before variant construction; no external data were admitted.
- **Correction:** Keep source and frozen spot timestamps in the original Asia/Kolkata representation for output, but add a temporary UTC comparison column and perform all equality/range filters against UTC-normalized instants.
- **Prevention:** External timezone handling must distinguish display/source timezone from comparison timezone; never compare timezone-aware Polars columns with fixed-offset Python literals directly.
