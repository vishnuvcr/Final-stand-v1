# Phase 20W Status

**State:** COMPLETE — alternate executable-bar recovery exhausted for the public HF routes used in this phase.

## Recovery result
- Frozen sample: 63 weekly expiry cycles.
- Phase-19 executable source coverage: 36/63 cycles.
- Missing at Phase-20 start: 40/63 cycles.
- HF-02 supplied intraday observations for 27/40 missing cycles.
- Fully recovered HF-02 cycles: **19/27** (224/224 variant-cycles).
- Partially recovered HF-02 cycles: **3/27** (159, 161, and 126 usable variants respectively).
- HF-02 cycles with zero executable variant-cycles: **5/27**, all in 2026.
- Additional usable variant-cycles recovered: **3,638 / 8,960** missing cells.
- Combined Phase-19 + Phase-20 executable variant-cycle coverage: **11,702 / 14,112 = 82.93%**.
- Equivalent fully covered cycles: 55/63, plus 3 partial cycles; 5 cycles remain entirely unrecovered.

## Source provenance
- HF-03 pinned: `0f4800e43e6f96cec0794369d78eb4d3c4211ef5`
- HF-02 pinned: `45e0a043f34f3f40f9694e52a944297803c2af8b`
- HF-01 2024/2025 inventory verified, but HF-01 begins 2024-10 and has no frozen-source file for the 2026 missing cycles at the pinned HF-01 revision.
- No synthetic bars were created and no conflicting sources were blended.

## Phase conclusion
Public-source recovery materially improves the frozen sample from 36/63 executable cycles to 55 fully covered cycles plus 3 partial, but **does not yet reach the original 50/63 promotion gate for every variant**. The next phase reruns the exact 224 variants using deterministic HF-03 → HF-02 source precedence for each variant-cycle, preserves missing cells as missing, and applies the unchanged statistical gate.
