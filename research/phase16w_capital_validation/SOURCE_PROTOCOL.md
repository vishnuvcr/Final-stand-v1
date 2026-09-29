# Phase 16W Source Protocol

## Primary official source
NSE's derivatives reports expose historical F&O SPAN risk-parameter files, including begin-of-day, intraday and end-of-day variants. NSE also documents detailed margin reports and historical contract-wise archives. These are the preferred source family for capital reconstruction.

## Admission requirements
A source is admitted only if:
- date is explicit;
- segment is NIFTY index options / relevant F&O;
- file/report type is documented;
- contract identity can be mapped;
- retrieval provenance is recorded;
- checksum is recorded when a file is cached;
- licensing/redistribution constraints are recorded.

## Rejection rules
Reject:
- current-day-only margin observations presented as historical;
- broker UI screenshots without machine-readable provenance;
- estimates copied from present-day margin calculators as historical truth;
- undocumented third-party margin numbers;
- any data requiring silent interpolation across missing dates.

## Capital interpretation
The exchange-level reconstructed requirement is not automatically identical to the cash a Paytm Money client would need in practice. Broker RMS buffers, peak-margin implementation, available collateral, premium debit/credit and intraday risk controls must remain separate assumptions.

## Execution limitation carried from Phase 15W
Historical bid/ask remains unqualified from free sources. Capital validation therefore improves the denominator/risk interpretation of the frozen OHLC reconstruction but does not convert reconstructed OHLC fills into verified historical executable fills.