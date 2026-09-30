# Phase 21W — 224-Configuration Parameter Surface Analysis

Holdout total net P&L in ₹. Descriptive analysis only; no new selection rule.

## K3 surface

| K3 | Mean holdout | Median | Positive |
|---:|---:|---:|---:|
| 0.5 | ₹-35082 | ₹-28391 | 0/32 |
| 1 | ₹-5032 | ₹-4302 | 11/32 |
| 1.5 | ₹17525 | ₹24790 | 24/32 |
| 2 | ₹38667 | ₹46226 | 32/32 |
| 2.5 | ₹56376 | ₹57498 | 32/32 |
| 3 | ₹72011 | ₹64214 | 32/32 |
| 4 | ₹91161 | ₹92482 | 32/32 |

## K1 surface

| K1 | Mean holdout | Median | Positive | Mean validity |
|---|---:|---:|---:|---:|
| OTM1 | ₹31224 | ₹36684 | 20/28 | 91.2% |
| OTM2 | ₹27719 | ₹38497 | 21/28 | 91.2% |
| OTM3 | ₹26798 | ₹40464 | 22/28 | 90.6% |
| ATM_NEAREST | ₹31219 | ₹36845 | 21/28 | 91.2% |
| ATM_UP | ₹31224 | ₹36684 | 20/28 | 91.2% |
| ITM1 | ₹33195 | ₹34597 | 19/28 | 91.3% |
| ITM2 | ₹40580 | ₹53855 | 19/28 | 90.1% |
| ITM3 | ₹47329 | ₹72263 | 21/28 | 90.1% |

## K2 surface

| K2 | Mean holdout | Median | Positive | Mean validity |
|---|---:|---:|---:|---:|
| NEXT1 | ₹18910 | ₹11997 | 37/56 | 99.4% |
| NEXT2 | ₹43565 | ₹47238 | 40/56 | 99.5% |
| NEXT3 | ₹40679 | ₹51377 | 48/56 | 99.4% |
| MIRROR_GAP | ₹31489 | ₹31751 | 38/56 | 65.1% |

## Holdout surface by K3

### K3 = 0.5

| K1 / K2 | NEXT1 | NEXT2 | NEXT3 | MIRROR_GAP |
|---|---:|---:|---:|---:|
| OTM1 | -41412 | -23053 | -17998 | -28391 |
| OTM2 | -57030 | -18979 | -13967 | -18700 |
| OTM3 | -61873 | -20201 | -17291 | -15909 |
| ATM_NEAREST | -39755 | -20795 | -16530 | -26734 |
| ATM_UP | -41412 | -23053 | -17998 | -28391 |
| ITM1 | -58715 | -30918 | -23290 | -37437 |
| ITM2 | -56365 | -39729 | -32277 | -44536 |
| ITM3 | -73030 | -60959 | -60905 | -54996 |

### K3 = 1

| K1 / K2 | NEXT1 | NEXT2 | NEXT3 | MIRROR_GAP |
|---|---:|---:|---:|---:|
| OTM1 | -9633 | -2226 | 15289 | -13082 |
| OTM2 | -13854 | -695 | 9868 | -7295 |
| OTM3 | -28684 | -4302 | 6607 | 3263 |
| ATM_NEAREST | -7879 | 408 | 15570 | -11328 |
| ATM_UP | -9633 | -2226 | 15289 | -13082 |
| ITM1 | -17876 | -3942 | 12231 | -22630 |
| ITM2 | -24698 | -14800 | 15462 | -14390 |
| ITM3 | -35618 | -15311 | 7561 | 10602 |

### K3 = 1.5

| K1 / K2 | NEXT1 | NEXT2 | NEXT3 | MIRROR_GAP |
|---|---:|---:|---:|---:|
| OTM1 | 1321 | 33037 | 36684 | -2128 |
| OTM2 | 1167 | 24790 | 38497 | 5788 |
| OTM3 | 3273 | 19854 | 32990 | 31751 |
| ATM_NEAREST | 704 | 28081 | 37184 | -2745 |
| ATM_UP | 1321 | 33037 | 36684 | -2128 |
| ITM1 | -2702 | 25633 | 35898 | -7457 |
| ITM2 | -11114 | -5085 | 41514 | 17608 |
| ITM3 | -14245 | 24896 | 42333 | 54374 |

### K3 = 2

| K1 / K2 | NEXT1 | NEXT2 | NEXT3 | MIRROR_GAP |
|---|---:|---:|---:|---:|
| OTM1 | 12750 | 47238 | 51501 | 9301 |
| OTM2 | 10432 | 45065 | 52929 | 24372 |
| OTM3 | 9254 | 42587 | 46226 | 50353 |
| ATM_NEAREST | 11997 | 42607 | 51144 | 8548 |
| ATM_UP | 12750 | 47238 | 51501 | 9301 |
| ITM1 | 16385 | 59859 | 60312 | 11630 |
| ITM2 | 6829 | 70397 | 66837 | 53855 |
| ITM3 | 10375 | 86775 | 72263 | 84733 |

### K3 = 2.5

| K1 / K2 | NEXT1 | NEXT2 | NEXT3 | MIRROR_GAP |
|---|---:|---:|---:|---:|
| OTM1 | 37214 | 65866 | 60677 | 33765 |
| OTM2 | 33954 | 56833 | 57498 | 43675 |
| OTM3 | 20283 | 54436 | 51377 | 60597 |
| ATM_NEAREST | 36845 | 67946 | 60302 | 33396 |
| ATM_UP | 37214 | 65866 | 60677 | 33765 |
| ITM1 | 34597 | 68840 | 71108 | 29842 |
| ITM2 | 46236 | 82985 | 78836 | 84109 |
| ITM3 | 44810 | 106037 | 86004 | 98432 |

### K3 = 3

| K1 / K2 | NEXT1 | NEXT2 | NEXT3 | MIRROR_GAP |
|---|---:|---:|---:|---:|
| OTM1 | 63440 | 81018 | 63671 | 59991 |
| OTM2 | 42076 | 75916 | 57498 | 53291 |
| OTM3 | 40464 | 60896 | 51377 | 64214 |
| ATM_NEAREST | 62952 | 77345 | 63297 | 59503 |
| ATM_UP | 63440 | 81018 | 63671 | 59991 |
| ITM1 | 65820 | 99757 | 74436 | 61065 |
| ITM2 | 64559 | 101902 | 84955 | 102821 |
| ITM3 | 92214 | 121247 | 88869 | 101633 |

### K3 = 4

| K1 / K2 | NEXT1 | NEXT2 | NEXT3 | MIRROR_GAP |
|---|---:|---:|---:|---:|
| OTM1 | 92482 | 94245 | 63671 | 89033 |
| OTM2 | 59276 | 85055 | 57498 | 71159 |
| OTM3 | 55304 | 70977 | 51377 | 71141 |
| ATM_NEAREST | 94244 | 93725 | 63297 | 90795 |
| ATM_UP | 92482 | 94245 | 63671 | 89033 |
| ITM1 | 109798 | 117729 | 74436 | 105044 |
| ITM2 | 126872 | 122096 | 84955 | 126409 |
| ITM3 | 149375 | 148445 | 92753 | 116536 |

## Top holdout configurations

| Configuration | Training | Validation | Holdout | Holdout Sharpe | Validity | Holm p |
|---|---:|---:|---:|---:|---:|---:|
| ITM3_NEXT1_K3M4 | ₹372208 | ₹68362 | ₹149375 | 8.33 | 98.4% | 0.074642 |
| ITM3_NEXT2_K3M4 | ₹299241 | ₹59853 | ₹148445 | 6.80 | 98.4% | 0.074642 |
| ITM2_NEXT1_K3M4 | ₹298163 | ₹65566 | ₹126872 | 7.01 | 98.4% | 0.074642 |
| ITM2_MIRROR_GAP_K3M4 | ₹253240 | ₹55175 | ₹126409 | 6.78 | 65.1% | 0.074642 |
| ITM2_NEXT2_K3M4 | ₹222235 | ₹46410 | ₹122096 | 6.06 | 98.4% | 0.085971 |
| ITM3_NEXT2_K3M3 | ₹283788 | ₹59853 | ₹121247 | 6.39 | 98.4% | 0.074642 |
| ITM1_NEXT2_K3M4 | ₹184615 | ₹28520 | ₹117729 | 6.12 | 100.0% | 0.085971 |
| ITM3_MIRROR_GAP_K3M4 | ₹187425 | ₹43920 | ₹116536 | 5.55 | 65.1% | 0.074642 |
| ITM1_NEXT1_K3M4 | ₹263120 | ₹52088 | ₹109798 | 6.88 | 100.0% | 0.074642 |
| ITM3_NEXT2_K3M2.5 | ₹273253 | ₹55177 | ₹106037 | 6.09 | 98.4% | 0.074642 |
| ITM1_MIRROR_GAP_K3M4 | ₹230962 | ₹51344 | ₹105044 | 6.85 | 65.1% | 0.074642 |
| ITM2_MIRROR_GAP_K3M3 | ₹227700 | ₹46850 | ₹102821 | 6.10 | 65.1% | 0.074642 |
| ITM2_NEXT2_K3M3 | ₹212126 | ₹46410 | ₹101902 | 5.68 | 98.4% | 0.074642 |
| ITM3_MIRROR_GAP_K3M3 | ₹187425 | ₹43920 | ₹101633 | 5.56 | 65.1% | 0.074642 |
| ITM1_NEXT2_K3M3 | ₹179777 | ₹28520 | ₹99757 | 6.12 | 100.0% | 0.074642 |
| ITM3_MIRROR_GAP_K3M2.5 | ₹187425 | ₹43920 | ₹98432 | 5.72 | 65.1% | 0.074642 |
| OTM1_NEXT2_K3M4 | ₹143310 | ₹18584 | ₹94245 | 5.34 | 100.0% | 0.074642 |
| ATM_UP_NEXT2_K3M4 | ₹143310 | ₹18584 | ₹94245 | 5.34 | 100.0% | 0.074642 |
| ATM_NEAREST_NEXT1_K3M4 | ₹234567 | ₹40955 | ₹94244 | 6.61 | 100.0% | 0.074642 |
| ATM_NEAREST_NEXT2_K3M4 | ₹149873 | ₹20059 | ₹93725 | 5.11 | 100.0% | 0.074642 |

## Interpretation

The frozen parameter surface shows a strong descriptive increase in holdout P&L with larger K3 values. ITM2/ITM3 configurations are prominent in the upper holdout tail, while NEXT2/NEXT3 have higher aggregate holdout means than NEXT1. MIRROR_GAP has lower mean validity because of its executable-cycle coverage. These are historical-sample observations, not future-return guarantees.

The inferential result is unchanged: minimum Holm-adjusted training p = 0.074642 and 0/224 configurations pass the complete preregistered promotion gate.

A future study can pre-register a fresh test of the apparent K3/ITM/NEXT interaction using unseen data and execution-quality quotes. It should not retroactively promote a Phase 21W configuration.
