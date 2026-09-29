# Error Log

## 2026-09-29

### E-0004 — Weekly branch plan path mismatch
- Observation: The new weekly branch was created from main, where `RESEARCH_PLAN.md` had not yet been copied from the earlier monthly branch.
- Impact: An attempted update returned GitHub 404 because the target file did not exist on the weekly branch.
- Resolution: Created a fresh weekly `RESEARCH_PLAN.md` rather than copying monthly assumptions.
- Prevention: When creating a replacement research branch, verify the complete file manifest on the branch before update operations.

### E-0005 — Weekly branch error-log path mismatch
- Observation: The weekly branch did not initially contain a branch-local `research/logs/ERROR_LOG.md` because only the new weekly research artifacts had been created.
- Impact: The first attempt to append the new reset error also returned GitHub 404.
- Resolution: Created the branch-local error log with the active weekly-reset error history.
- Prevention: Every research branch must contain both research and error logs before update operations begin.


### E-0006 — Public sample workbook unavailable to runtime
- Observation: A public GitHub backtesting repository advertises a bundled one-year NIFTY 1-minute workbook, but the binary workbook could not be fetched through the available GitHub/web runtime.
- Impact: The advertised sample could not be used as an empirical dataset in this run.
- Resolution: Do not fabricate or substitute synthetic observations. Keep the empirical gate pending and implement only deterministic mechanics/tests.
- Prevention: Maintain a source-access matrix and require successful checksum/ingestion validation before any dataset is admitted to the empirical sample.

### E-0007 — Two script-string escaping errors during repository updates
- Observation: Two JavaScript orchestration scripts contained unescaped backticks/template-literal content and failed before repository writes.
- Impact: No partial repository mutation occurred from those failed calls.
- Resolution: Rewrote the affected strings using ordinary strings and simpler payload construction.
- Prevention: Avoid nested template literals in repository-update scripts; use plain strings for code/document payloads.

### E-0008 — GitHub fetch schema mismatch
- Observation: A repository-root fetch call used repository/path/ref arguments against a fetch action that requires an approved public GitHub URL.
- Impact: No repository mutation occurred.
- Resolution: Switched to the dedicated file-fetch action for branch files.
- Prevention: Inspect the action schema before using generic GitHub fetch operations.

### E-0009 — Missing .gitignore is not evidence of a broken repository
- Observation: A direct fetch of .gitignore returned GitHub 404.
- Impact: None; the file simply is not present on the active weekly branch.
- Resolution: Continued without inventing a .gitignore and used explicit cache/output paths in the Phase 9 workflow.
- Prevention: Treat 404s on optional repository files as an observed repository state, not as a reason to create speculative files.

### E-0010 — Bulk Phase 9 write string parse failure
- Observation: A multi-file JavaScript payload failed because Markdown backticks were interpreted by the orchestration runtime.
- Impact: No partial repository mutation occurred from that call.
- Resolution: Split the write into safe serialized content and removed nested backtick interpolation.
- Prevention: Use plain-string payloads for repository artifacts that contain Markdown/code fencing.

### E-0011 — GitHub Actions expression interpolation in orchestration string
- Observation: A workflow payload contained GitHub expressions of the form ${{ ... }}, which the JavaScript template literal parser interpreted before the GitHub write.
- Impact: No repository mutation occurred from that failed call.
- Resolution: Escaped the dollar-brace sequence in the orchestration source so the literal GitHub expression reaches the workflow file.
- Prevention: Always escape ${{ in JavaScript template strings used to create GitHub Actions workflows.

### E-0012 — GitHub update-file argument name mismatch
- Observation: An update call used content_sha, while the action schema requires sha for the current blob identifier.
- Impact: No partial repository mutation occurred.
- Resolution: Retried with the exact schema field sha.
- Prevention: Use the returned fetch_file blob SHA and the action's declared argument names verbatim.
- Observation: Two JavaScript orchestration scripts contained unescaped backticks/template-literal content and failed before repository writes.
- Impact: No partial repository mutation occurred from those failed calls.
- Resolution: Rewrote the affected strings using ordinary string concatenation.
- Prevention: Avoid nested template literals in repository-update scripts; use plain strings for code/document payloads.


### E-0013 — Phase 9 README create/update ordering
- Observation: The Phase 9 README was created first; a later attempt used the create-file action again instead of the update-file action.
- Impact: GitHub correctly rejected the request with HTTP 422 because the file already existed; no partial mutation occurred.
- Resolution: Fetched the current blob SHA and updated the existing file through the update-file action.
- Prevention: Before any repository write, check whether the target path exists and choose create-file or update-file accordingly.

### E-0014 — GitHub Actions expression parsing in orchestration strings
- Observation: A workflow-edit payload used unescaped `${{ ... }}` expressions inside JavaScript template literals and failed before the repository write.
- Impact: No partial repository mutation occurred.
- Resolution: Reissued the patch using quoted strings with escaped dollar-brace sequences.
- Prevention: Never place raw GitHub Actions expressions inside JavaScript template literals; use plain quoted strings or escaped sequences.


### E-0015 — Workflow patch string parsing
- Observation: A workflow-edit orchestration string again parsed a raw GitHub Actions expression inside a JavaScript template literal and failed before the repository write.
- Impact: No partial repository mutation occurred.
- Resolution: Reissued the patch using quoted strings; the workflow update then succeeded.
- Prevention: For GitHub Actions files, use non-template string literals whenever the payload contains GitHub Actions expressions.


### E-0016 — Phase 11 bulk artifact string parsing
- Observation: A large JavaScript template-literal payload containing Python/Markdown backticks failed before repository writes.
- Impact: No partial repository mutation.
- Resolution: Retried with simplified plain-text artifact strings and created the backtest engine successfully.
- Prevention: Keep repository artifact payloads free of nested backticks or use quoted strings.

### E-0017 — Phase 12 workflow expression parsing
- Observation: A workflow payload containing GitHub Actions expressions failed when parsed as a JavaScript template literal.
- Impact: No partial repository mutation.
- Resolution: Escaped the expression interpolation and recreated the workflow.
- Prevention: Escape all GitHub Actions expression markers in orchestration template strings.

### E-0018 — Runtime could not execute a direct Git clone for local verification
- Observation: The container runtime could not resolve github.com, so a local clone of the research branch was unavailable.
- Impact: Local execution of the updated unit tests could not be performed in this environment.
- Resolution: Repository changes were made through the GitHub connector and the workflow remains the execution authority. No empirical result was claimed.
- Prevention: Keep deterministic unit tests in the repository and rely on GitHub Actions for networked data execution; verify workflow artifacts before admitting results.

### E-0019 — Phase 13 end-to-end execution remains workflow-dependent
- Observation: The local runtime cannot resolve github.com, while the Phase 13 workflow requires network access to Hugging Face.
- Impact: Local execution cannot substitute for the repository workflow.
- Resolution: Keep the workflow as the execution authority and require an observed artifact before admitting holdout results.
- Prevention: Never fabricate or infer workflow outputs from source code alone.

### E-0022 — GitHub Actions pip cache expected dependency manifest
- Observation: GitHub Actions failed at actions/setup-python because cache: pip was enabled without requirements.txt or pyproject.toml.
- Impact: The Phase 13 job stopped before dependency installation; no empirical data were processed.
- Resolution: Removed pip caching from the Phase 9/11/12/13 workflows. Hugging Face data caching remains enabled.
- Prevention: Do not enable setup-python dependency caching unless the repository contains a supported dependency lock/manifest file.

### E-0023 — Hugging Face Hub tree API incompatibility
- Observation: The first networked Phase 13 run reached data ingestion but failed because Hugging Face Hub 0.36.2 rejected list_repo_tree(path=...).
- Impact: No empirical cycles were ingested.
- Resolution: Changed the call to path_in_repo=... and pinned the workflow dependency to the 0.36.x series.
- Prevention: Pin external SDK major/minor compatibility and run the ingestion smoke test in CI before empirical processing.

### E-0024 — Polars rejected fixed-offset timezone metadata in HF parquet
- Observation: The next Phase 13 run reached the parquet read and failed on timestamp metadata '+05:30' under Polars 1.44.
- Impact: No weekly cycles were processed.
- Resolution: Enabled Polars fixed-offset timezone validation override at process start, followed by explicit normalization to Asia/Kolkata already present in the ingestion code.
- Prevention: Treat third-party parquet timezone metadata as an ingestion compatibility surface and normalize it before strategy timestamps are compared.

### E-0025 — Weekly lock price fields were referenced before assignment
- Observation: The live Phase 13 ingestion run reached CycleRecord construction and raised NameError for lock_p1.
- Impact: Data ingestion stopped after reaching cycle processing; no backtest result was produced.
- Resolution: Explicitly derive lock_p1, lock_p2 and lock_p3 from the validated lock rows before building the cycle record.
- Prevention: Keep manifest fields covered by executable integration tests that exercise at least one complete cycle.

### E-0026 — Phase 13 workflow invoked Phase 11 backtest with the wrong working-data defaults
- Observation: Phase 9 ingestion produced 63 USABLE_OHLC cycles, but every Phase 13 backtest reported zero trades because the backtest defaults point to research/phase9_weekly/output while the workflow execution context/path handling was not explicit.
- Impact: Holdout candidate files were empty; no strategy performance was measured.
- Resolution: Phase 13 and Phase 12 workflows now pass manifest/options/spot paths explicitly. The holdout reader now fails with a diagnostic rather than silently reading an empty CSV.
- Prevention: Workflows must pass data-interface paths explicitly across phase boundaries; zero-trade runs are treated as pipeline failures, not valid results.

### E-0027 — Historical-rate unit test was defined after its __main__ invocation
- Observation: The Phase 11 test file called test_historical_rate_schedule() before its definition.
- Impact: Direct execution of the Phase 11 unit-test script would raise NameError.
- Resolution: Moved the function definition before the __main__ block.
- Prevention: Keep executable test definitions above the entrypoint and run the repository test script in CI.


### E-0028 — Phase 13 workflow still used Phase 11 default data paths
- Observation: Although the intended fix was documented in E-0026, the committed Phase 13 workflow still invoked `weekly_backtest.py` without explicit manifest/options/spot arguments. The backtest therefore read absent default files and emitted zero trades for every stop candidate.
- Impact: Candidate CSVs contained only headers; holdout selection failed with `KeyError: mean_net_rupees`. No empirical performance result was produced.
- Resolution: Patch the Phase 13 workflow to pass the Phase 9 manifest, selected option bars and selected spot bars explicitly at the phase boundary.
- Prevention: CI workflows must pass all cross-phase data-interface paths explicitly; a documented fix is not considered complete until the committed workflow is inspected and the next run confirms nonzero executable cycles.


### E-0029 — Phase 13 zero-trade result persisted after explicit path correction
- Observation: Run 36596109078 successfully ingested 100 expiry candidates and 63 USABLE_OHLC cycles, but all seven Phase 11 candidate backtests still returned zero trades.
- Impact: The earlier path-only diagnosis was insufficient; no empirical result can be admitted.
- Resolution: Added a CI data-interface diagnostic that reports manifest status counts, option/spot row counts, and exact entry/lock/expiry-row availability for representative USABLE_OHLC cycles before candidate generation.
- Prevention: Cross-phase interfaces must be validated by observed row-level compatibility, not only by filesystem paths.


### E-0030 — Option timestamp representation mismatch
- Observation: Phase 13 diagnostic showed USABLE_OHLC cycles but zero entry/lock option rows because manifest timestamps and Parquet string rendering differed.
- Impact: Exact timestamp matching rejected otherwise usable cycles.
- Resolution: Phase 11 now normalizes timestamp strings to ISO `T` form and normalizes `+0530` to `+05:30` before exact comparisons.
- Prevention: Cross-phase timestamp contracts must normalize explicitly.


### E-0031 — Timestamp normalization regex escaped incorrectly
- Observation: The first E-0030 patch used an over-escaped `+0530` regex, so the intended offset normalization did not occur.
- Impact: Phase 11 continued to reject all exact entry/lock timestamps.
- Resolution: Corrected the regex to match the literal `+0530` suffix.
- Prevention: Add a direct unit test for representative timestamp normalization before accepting the phase interface.


### E-0032 — Zero fractional seconds in typed option timestamps
- Observation: Option Parquet `timestamp` is `Datetime(μs, Asia/Kolkata)` and stringifies as `YYYY-MM-DD HH:MM:SS.000000+05:30`; manifest timestamps are `YYYY-MM-DDTHH:MM:SS+05:30`.
- Impact: Exact entry/lock matching remained zero despite prior separator/offset normalization.
- Resolution: Normalize zero fractional seconds before comparisons.
- Prevention: Prefer typed datetime joins in future cross-phase interfaces and retain this string normalization only as compatibility logic.


### E-0033 — String timestamp matching remained non-reproducible
- Observation: Multiple string-normalization attempts still yielded zero matched option rows despite typed Datetime source data.
- Resolution: Replaced cross-phase timestamp string comparisons with timezone-aware Python datetime values compared directly against the typed Polars timestamp column.
- Rationale: This removes representation ambiguity without changing trade timestamps.


### E-0034 — Polars timezone literal normalized to UTC
- Observation: Python +05:30 datetimes were materialized by Polars as UTC and could not compare directly with the Asia/Kolkata source column.
- Impact: Typed timestamp diagnostics failed before evaluating entry/lock rows.
- Resolution: Convert parsed timestamps to ZoneInfo(Asia/Kolkata) before constructing Polars literals.
- Prevention: Cross-phase timestamp tests must assert timezone metadata as well as instant equality.


### E-0035 — Polars timezone-aware literal conversion remained unsuitable
- Observation: Even ZoneInfo Asia/Kolkata Python datetimes were materialized as UTC literals by the Polars comparison path.
- Resolution: Compare normalized local bar-time keys to second precision (`YYYY-MM-DDTHH:MM:SS`). All source bars and manifest timestamps are explicitly Asia/Kolkata, so no cross-timezone conversion is introduced.
- Prevention: Keep cross-phase comparison keys timezone-local and separately validate timezone metadata at ingestion.


### E-0036 — Diagnostic retained obsolete typed datetime comparison
- Observation: Phase 13 diagnostic itself still compared Asia/Kolkata timestamps with Python datetime literals, reproducing the UTC schema error after the backtest had been converted to local keys.
- Resolution: Diagnostic now uses the same second-precision local timestamp key as Phase 11.

## E-0044 — Public sample versus historical archive distinction
- Observation: TickBytes and OptionVault expose public Level-2 samples containing bid/ask fields, but their documentation identifies complete historical archives as subscription/licensed datasets.
- Impact: It would be invalid to treat the public samples as evidence that the full 63-cycle historical bid/ask archive is freely available.
- Resolution: Classify the sources as schema-qualified but archive-unqualified; do not alter the frozen backtest or claim quote-validated historical performance.
- Prevention: Require date coverage, exact-contract coverage, completeness and licensing checks before admitting an execution dataset into Phase 15W.
### E-0045 — Free-source schema/archive confusion during expanded audit
- Observation: Several public projects expose bid/ask fields in schemas, sample files or live APIs, while their historical data files are not publicly archived or expired-contract access is restricted.
- Impact: A schema hit could be incorrectly classified as a free historical BBO archive.
- Resolution: Added a four-level qualification standard (quote-qualified, schema-qualified, OHLC-qualified, rejected) and required date/contract/completeness/licensing checks.
- Prevention: Do not admit any execution source until an actual historical file/API response for the study's expired NIFTY contracts is observed and reproducibly ingested.

### E-0046 — Authenticated API access boundary
- Observation: The strongest remaining BBO-capable route requires authenticated/vendor access; the project has no authorized TrueData/Dhan/Breeze/Upstox credentials available to this session.
- Impact: An empirical historical-BBO probe cannot be honestly executed yet.
- Resolution: Added a credential-safe probe protocol and scaffold. No credentials are fabricated or requested in repository files.
- Prevention: Treat missing authentication as a blocking data-access condition, not as evidence of data absence; do not substitute OHLC for BBO.


### E-0048 — Phase 16W begins with unresolved historical BBO limitation
- Observation: no free historical NIFTY weekly-options BBO archive was qualified in Phase 15W.
- Impact: capital validation cannot be presented as executable-fill validation.
- Resolution: carry the BBO limitation forward explicitly; use Phase 16W only for capital/margin reconstruction and risk normalization.
- Prevention: keep BBO and capital evidence as separate evidence classes in the manuscript.


### E-0049 — Strategy-definition scope change required a separate validation phase
- Observation: The user requested explicit testing of alternative K1/K2 definitions after the frozen weekly strategy had already been used for Phase 13W holdout evidence.
- Impact: Silently changing K1/K2 would invalidate comparability with the frozen evidence and could contaminate the locked holdout selection.
- Resolution: Created Phase 17W as a separate preregistered strategy-definition validation phase. The Phase 13W control remains immutable and the final holdout is descriptive only for this new family.
- Prevention: Treat any change that alters K1, K2, K3 construction, timing, stop or execution assumptions as a new registered experiment rather than editing prior results.

### E-0050 — GitHub Actions expression escaping in Phase 17W workflow
- Observation: The first workflow commit stored GitHub Actions expressions with a literal backslash before the expression marker because of orchestration-string escaping.
- Impact: The workflow file would not evaluate inputs/secrets correctly.
- Resolution: Replaced the stored escaped markers with native GitHub Actions expression syntax and committed the corrected workflow before relying on empirical execution.
- Prevention: Inspect committed workflow text after creation and validate that every expression is stored exactly as ${{ ... }}.

### E-0051 — Second Phase 17W workflow expression escape survived the first patch
- Observation: GitHub Actions run 36615776492 showed --max-expiries received the literal value \\104 because a shell backslash still preceded the expression marker.
- Impact: The first Phase 17W empirical run stopped before data ingestion; no variant result was produced.
- Resolution: Removed every remaining backslash before GitHub Actions expressions and verified the committed YAML contains native expressions such as ${{ inputs.max_expiries || '104' }}.
- Prevention: Inspect the rendered workflow text and the first shell command line in CI logs before treating a workflow run as an empirical result.

### E-0052 — Phase 17W module import path
- Observation: Workflow run 36615889752 successfully rebuilt the 63-cycle Phase 9 interface, then the variant engine failed with ModuleNotFoundError: research when invoked as a script by path.
- Impact: No alternative backtests were executed.
- Resolution: Changed the workflow to invoke the engine as the module research.phase17w_strike_alternatives.strike_alternatives from repository root, matching the existing test import path.
- Prevention: In CI, invoke repository-internal Python modules with -m when they import sibling research packages unless package path setup is explicit.

### E-0053 — Phase 17W variant engine required scale optimization
- Observation: The first corrected empirical run reached the 32-variant engine, where the initial implementation repeatedly scanned full expiry parquet data while constructing variant-specific paths.
- Impact: This created unnecessary repeated I/O/CPU and risked an excessively long CI execution for the finite 32-configuration experiment.
- Resolution: Reworked the engine to read each expiry source once for variant-path extraction, filter to the union of required strikes, and partition the combined option bars by (variant, expiry) before backtesting.
- Prevention: For finite multi-variant studies, share immutable data reads and pre-partition variant inputs before running the common backtest kernel.
