# Phase 22C — Source Recovery and Coverage Qualification

## Objective
Recover additional qualifying weekly NIFTY option-expiry cycles for the frozen 30-member robustness envelope and the 504-family control without changing strategy mechanics or statistical gates.

## Candidate hierarchy
1. RISSIN primary archive.
2. Existing approved/public fallback archives.
3. Newly identified public expired-option archives, subject to empirical coverage/schema/hash validation.
4. Commercial archives only as a separately documented acquisition option.

## Candidate: Cloud Trader Pro / Shoonya Trader
Public documentation advertises 1-minute NIFTY expired-options OHLCV + OI, including weekly/monthly expiries and all strikes. This is a coverage claim, not yet a verified research input.

## Admission checks
- exact expiry dates;
- CE/PE strike coverage through ITM8/OTM8;
- 1-minute timestamps/timezone;
- OHLC/volume/OI fields;
- duplicate-row audit;
- deterministic download/hash;
- coverage after 2026-07-21;
- independent overlap checks.

## Non-admission rule
Do not use candidate data until all checks pass. Phase 22B remains authoritative meanwhile.
