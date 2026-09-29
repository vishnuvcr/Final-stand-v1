# Phase 17W Variant Registry

All **224** configurations are registered before empirical results are read.

## K1 rules

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

## K2 rules

| K2 rule | Definition |
|---|---|
| NEXT1 | first strike > K1 |
| NEXT2 | second strike > K1 |
| NEXT3 | third strike > K1 |
| MIRROR_GAP | strike > K1 with spacing closest to abs(spot-K1); tie lower |

## K3 target multipliers

For each K1/K2 pair:

**target K3 premium = M × (P1 − P2)**

The registered multipliers are:

| K3 multiplier | Interpretation |
|---:|---|
| 0.5 | target = 0.5D |
| 1.0 | target = 1.0D |
| 1.5 | target = 1.5D |
| 2.0 | target = 2.0D — frozen baseline |
| 2.5 | target = 2.5D |
| 3.0 | target = 3.0D |
| 4.0 | target = 4.0D |

K3 is always selected as the listed call strike **above K2** whose entry premium is closest to the target premium. Ties are resolved by the lower strike.

## Configuration ID format

<K1>_<K2>_K3M<multiplier>

Examples:
- OTM1_NEXT1_K3M2 — exact current frozen configuration.
- ATM_NEAREST_NEXT2_K3M1.5
- ITM2_MIRROR_GAP_K3M4

## Registered family size

8 K1 rules × 4 K2 rules × 7 K3 multipliers = **224 configurations**.

## Full K1/K2 family

For each of the eight K1 rules and four K2 rules below, all seven K3 multipliers are tested.

| K1 | K2 |
|---|---|
| OTM1 | NEXT1 |
| OTM1 | NEXT2 |
| OTM1 | NEXT3 |
| OTM1 | MIRROR_GAP |
| OTM2 | NEXT1 |
| OTM2 | NEXT2 |
| OTM2 | NEXT3 |
| OTM2 | MIRROR_GAP |
| OTM3 | NEXT1 |
| OTM3 | NEXT2 |
| OTM3 | NEXT3 |
| OTM3 | MIRROR_GAP |
| ATM_NEAREST | NEXT1 |
| ATM_NEAREST | NEXT2 |
| ATM_NEAREST | NEXT3 |
| ATM_NEAREST | MIRROR_GAP |
| ATM_UP | NEXT1 |
| ATM_UP | NEXT2 |
| ATM_UP | NEXT3 |
| ATM_UP | MIRROR_GAP |
| ITM1 | NEXT1 |
| ITM1 | NEXT2 |
| ITM1 | NEXT3 |
| ITM1 | MIRROR_GAP |
| ITM2 | NEXT1 |
| ITM2 | NEXT2 |
| ITM2 | NEXT3 |
| ITM2 | MIRROR_GAP |
| ITM3 | NEXT1 |
| ITM3 | NEXT2 |
| ITM3 | NEXT3 |
| ITM3 | MIRROR_GAP |

Every row above is crossed with all seven multipliers.

## Baseline control

OTM1_NEXT1_K3M2 is the historical frozen control.

The Phase 13W historical results remain unchanged. Phase 17W alternative results are not substituted into the earlier evidence.
