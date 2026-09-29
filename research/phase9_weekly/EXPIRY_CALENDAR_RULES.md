# Phase 9W — Historical NIFTY Weekly Expiry Calendar Rules

## Contract-family definition

The primary experiment uses serial weekly NIFTY option contracts excluding the monthly contract for that month.

For the Hugging Face expiry-partitioned source, monthly expiries are identified as the latest NIFTY expiry date present in each calendar month. All earlier expiry dates in that calendar month are treated as weekly contracts for the pilot.

This source-derived classification is checked against the NSE historical expiry-day regime.

## Historical expiry-day regime

NSE records that NIFTY weekly expiry was Thursday before the 2025 revision, and the June 23, 2025 circular revised the weekly expiry to Tuesday effective at the end of August 28, 2025. The same circular says the existing Thursday expiries through July 2025 were not revised. The later annexure confirms the new Tuesday series starts in September 2025. citeturn780591search23turn780591search22

For the primary sample:

- expiry dates through August 28, 2025 are expected to follow the Thursday-era regime, subject to holiday adjustments;
- contracts created under the revised regime after August 28, 2025 follow the Tuesday-era weekly regime, subject to holiday adjustments;
- the March 2025 circular that proposed a Monday expiry is treated as superseded for the final calendar because the later June 23, 2025 circular explicitly states the then-current day was Thursday and revises it to Tuesday. citeturn780591search24turn780591search23

## Why the source-derived classification is used

The source files provide expiry dates but do not, by themselves, encode a reliable weekly/monthly family label. The latest-expiry-in-calendar-month rule uses the actual observed expiry dates instead of assuming a weekday, so holiday-adjusted monthly expiries can remain correctly classified.

The pilot still records the historical regime and flags unusual dates rather than silently changing contract membership.

## Audit fields

Each Phase 9 cycle manifest must record:

- target expiry;
- prior weekly expiry;
- contract family = weekly;
- excluded monthly expiry for the same calendar month, when present;
- historical expiry regime;
- source file;
- source revision;
- source SHA-256.

## Research restriction

No trade cycle may be generated from a monthly expiry file. No entry day may use the previous monthly expiry when a prior serial weekly expiry exists.
