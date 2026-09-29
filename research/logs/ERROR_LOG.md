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
- Resolution: Rewrote the affected strings using ordinary string concatenation.
- Prevention: Avoid nested template literals in repository-update scripts; use plain strings for code/document payloads.
