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

### E-0018 — Runtime could not execute a direct Git clone for local verification
- Observation: The container runtime could not resolve github.com, so a local clone of the research branch was unavailable.
- Impact: Local execution of the updated unit tests could not be performed in this environment.
- Resolution: Repository changes were made through the GitHub connector and the workflow remains the execution authority. No empirical result was claimed.
- Prevention: Keep deterministic unit tests in the repository and rely on GitHub Actions for networked data execution; verify workflow artifacts before admitting results.

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
