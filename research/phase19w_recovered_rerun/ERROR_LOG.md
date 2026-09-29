# Phase 19W Error Log

## E19-001 — 2026-09-30
- **Issue:** Initial workflow template generation produced malformed GitHub Actions expressions because the file-generation code interpolated GitHub `${{ ... }}` tokens.
- **Impact:** The first committed workflow definition was syntactically invalid and was not executed.
- **Correction:** Replaced the workflow with a fixed manual `workflow_dispatch` job using the frozen 224-variant range and a temporary `HF_REVISION=main` setting. No empirical result was generated from the malformed workflow.
- **Prevention:** Future workflow generation will treat GitHub expression syntax as literal configuration text rather than host-language interpolation.

## Inherited limitation
Phase 17W maximum usable coverage was 39/63 for the registered family. This remains a Phase 18W data-recovery question, not a Phase 19W empirical result.

## E19-002 — 2026-09-30
- **Issue:** Direct local execution could not reach Hugging Face because the runtime has DNS/network isolation (`NameResolutionError` for `huggingface.co`).
- **Impact:** No local empirical result was produced and no local result was substituted for the GitHub Actions/HF pipeline.
- **Correction:** The empirical rerun remains delegated to GitHub Actions, where `HF_TOKEN` and the existing cache are available.
- **Prevention:** Treat network-isolated local execution as a diagnostic only; do not reinterpret it as source-data unavailability.


## E19-003 — 2026-09-30
- **Issue:** The first automatic Phase 19 trigger failed before job creation because `hashFiles()` was used in a job-level `if` expression.
- **Impact:** No empirical computation ran and no result was produced.
- **Correction:** Removed the unsupported job-level gate. The committed `ADMISSION.md` is now the explicit repository admission record; the workflow retains both manual and push triggers.


## E19-004 — 2026-09-30
- **Issue:** The first live Phase 19 execution bridge reached the runner but failed immediately with `ModuleNotFoundError: No module named 'research'`.
- **Impact:** No empirical computation ran and no output was admitted.
- **Correction:** Set `PYTHONPATH` to the checked-out repository workspace in the execution environment. No strategy, data, cost, or statistical parameter was changed.
