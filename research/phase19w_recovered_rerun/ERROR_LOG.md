# Phase 19W Error Log

## E19-001 — 2026-09-30
- **Issue:** Initial workflow template generation produced malformed GitHub Actions expressions because the file-generation code interpolated GitHub expression tokens.
- **Impact:** The first committed workflow definition was syntactically invalid and was not executed.
- **Correction:** Replaced the workflow with a fixed manual `workflow_dispatch` job using the frozen 224-variant range. No empirical result was generated from the malformed workflow.
- **Prevention:** Future workflow generation treats GitHub expression syntax as literal configuration text.

## Inherited limitation
Phase 17W maximum usable coverage was 39/63 for the registered family. This remained a Phase 18W data-recovery question, not a Phase 19W empirical result.

## E19-002 — 2026-09-30
- **Issue:** Direct local execution could not reach Hugging Face because the runtime has DNS/network isolation (`NameResolutionError` for `huggingface.co`).
- **Impact:** No local empirical result was produced and no local result was substituted for the GitHub Actions/HF pipeline.
- **Correction:** The empirical rerun remains delegated to GitHub Actions, where `HF_TOKEN` and the existing cache are available.
- **Prevention:** Treat network-isolated local execution as a diagnostic only; do not reinterpret it as source-data unavailability.

## E19-003 — 2026-09-30
- **Issue:** An earlier automatic Phase 19 trigger failed before computation because an unsupported job-level `hashFiles()` gate was used.
- **Impact:** No empirical computation ran and no result was produced.
- **Correction:** Removed the unsupported job-level gate. The Phase 18 admission record is the explicit repository admission record.

## E19-004 — 2026-09-30
- **Issue:** Dedicated Phase 19 workflow run 36636186213 reached the empirical step but Python raised `ModuleNotFoundError: No module named 'research'`.
- **Impact:** No empirical computation or result was produced.
- **Correction:** Added `PYTHONPATH=${{github.workspace}}` to the empirical step so repository package imports resolve deterministically.
- **Prevention:** Workflow validation now includes the repository module path explicitly.
