# Phase 17W Variant Registry

All 32 configurations are registered before empirical results are read.

| K1 rule | Definition |
|---|---|
| OTM1 | first strike > spot |
| OTM2 | second strike > spot |
| OTM3 | third strike > spot |
| ATM_NEAREST | closest strike to spot; tie higher |
| ATM_UP | first strike >= spot |
| ITM1 | highest strike < spot |
| ITM2 | second-highest strike < spot |
| ITM3 | third-highest strike < spot |

| K2 rule | Definition |
|---|---|
| NEXT1 | first strike > K1 |
| NEXT2 | second strike > K1 |
| NEXT3 | third strike > K1 |
| MIRROR_GAP | strike > K1 with spacing closest to abs(spot-K1); tie lower |

## Configuration IDs

- OTM1_NEXT1 (frozen baseline)
- OTM1_NEXT2
- OTM1_NEXT3
- OTM1_MIRROR_GAP
- OTM2_NEXT1
- OTM2_NEXT2
- OTM2_NEXT3
- OTM2_MIRROR_GAP
- OTM3_NEXT1
- OTM3_NEXT2
- OTM3_NEXT3
- OTM3_MIRROR_GAP
- ATM_NEAREST_NEXT1
- ATM_NEAREST_NEXT2
- ATM_NEAREST_NEXT3
- ATM_NEAREST_MIRROR_GAP
- ATM_UP_NEXT1
- ATM_UP_NEXT2
- ATM_UP_NEXT3
- ATM_UP_MIRROR_GAP
- ITM1_NEXT1
- ITM1_NEXT2
- ITM1_NEXT3
- ITM1_MIRROR_GAP
- ITM2_NEXT1
- ITM2_NEXT2
- ITM2_NEXT3
- ITM2_MIRROR_GAP
- ITM3_NEXT1
- ITM3_NEXT2
- ITM3_NEXT3
- ITM3_MIRROR_GAP

The baseline is a control, not a newly selected winner.
