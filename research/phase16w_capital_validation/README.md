# Phase 16W — Capital and Margin Validation

This phase follows the completed free historical-BBO discovery gate.

## Current objective
Reconstruct dated capital and margin requirements for the frozen weekly strategy using official NSE historical SPAN/risk-parameter/report infrastructure where accessible.

## Important limitation
The study still lacks a qualified free historical NIFTY option BBO archive. This phase does not replace BBO with OHLC and does not alter the strategy.

## Official evidence
NSE's derivatives reports page exposes historical F&O SPAN risk-parameter files and historical contract-wise price/volume archives. NSE also documents detailed margin files containing SPAN and related components.

## Deliverables
- source and cache manifest;
- contract/date mapping;
- peak capital requirement;
- capital-normalized diagnostics;
- quantified margin-data gaps;
- manuscript supplement.

## Workflow
Use the manual Phase 16W - Capital and Margin Validation GitHub Actions workflow.