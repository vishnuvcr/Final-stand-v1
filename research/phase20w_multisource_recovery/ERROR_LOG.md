# Phase 20W Error Log

No Phase 20 execution errors yet.

## Methodological controls
- Never replace a primary HF-03 observation with an alternate source when the primary observation exists.
- Never interpolate or synthesize missing option prices.
- Log all schema, timestamp, strike, expiry, duplicate, conflict, and provenance failures.


## E20-001 — 2026-09-30
- **Issue:** The first Phase 20 inventory run passed the short HF commit prefix `f90f7ac` to the Hub tree API, which returned 404.
- **Impact:** Source inventory stopped before any files were examined.
- **Correction:** Pin the full verified commit SHA `f90f7acad633ba5a803f25cf431fb5f13ce3d162` for Recovery-1. The public archive and commit page confirm the dataset and revision. No data were downloaded or altered.


## E20-002 — 2026-09-30
- **Issue:** Hugging Face recursive tree listing returned 404 even for the verified full Recovery-1 commit SHA because the repository is LFS-backed and the tree endpoint is rejecting the revision path.
- **Impact:** Inventory could not enumerate files through `list_repo_files(..., revision=...)`.
- **Correction:** Resolve the immutable current `main` commit via `repo_info`, then enumerate files from the default branch and record the resolved SHA in the inventory. The public commit history shows that `main` resolves to the verified upload commit. No strategy or source-selection rule changes.


## E20-003 — 2026-09-30
- **Issue:** The Hugging Face Python API returned 404 for the public `johnwick3690/stocks` dataset even at `main`, preventing recursive inventory.
- **Impact:** No source files were enumerated through the API.
- **Correction:** Recovery-1 inventory now uses lightweight HTTPS probes against the verified weekly-expiry parquet path exposed by the public dataset tree. Recovery-2 and Recovery-3 remain registered and will receive separate schema discovery before download. No large file is downloaded during inventory.


## E20-004 — 2026-09-30
- **Issue:** The direct-probe inventory script imported `requests`, but the workflow installed only `huggingface_hub`.
- **Impact:** Inventory stopped before making any HTTP probe.
- **Correction:** Add `requests` to the workflow environment. No source or research rule changes.


## E20-005 — 2026-09-30
- **Issue:** Recovery-1 file-existence probes against the LFS `resolve` endpoint returned 404 despite verified files being present in the public commit tree.
- **Impact:** The inventory incorrectly reported zero matching files.
- **Correction:** Probe the public `blob/main/...` file pages instead. This validates exact path existence without downloading the underlying LFS object. The verified commit remains recorded as provenance.


## E20-006 — 2026-09-30
- **Issue:** Public Recovery-1 file pages returned HTTP 401 when the runner supplied the configured `HF_TOKEN` header.
- **Impact:** Anonymous public-file existence was masked as authentication failure.
- **Correction:** Inventory probes now omit authentication headers for public file pages. The token remains available for subsequent LFS payload downloads where required.
