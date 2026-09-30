from research.phase17w_strike_alternatives import strike_alternatives as base

base.K1_RULES = [*[f"OTM{i}" for i in range(1,9)], "ATM_NEAREST", "ATM_UP", *[f"ITM{i}" for i in range(1,9)]]
base.K2_RULES = ["NEXT1","NEXT2","NEXT3","MIRROR_GAP"]
base.K3_MULTIPLIERS = [0.5,1.0,1.5,2.0,2.5,3.0,4.0]
base.VARIANT_IDS = [base.make_variant_id(k1,k2,m) for k1 in base.K1_RULES for k2 in base.K2_RULES for m in base.K3_MULTIPLIERS]

assert len(base.K1_RULES) == 18
assert len(base.VARIANT_IDS) == 504

strikes = [24000 + 50*i for i in range(-12, 13)]
spot = 24600.0
assert base.choose_k1(strikes, spot, 'OTM8') == 25000.0
assert base.choose_k1(strikes, spot, 'ITM8') == 24200.0

k1 = base.choose_k1(strikes, spot, 'OTM8')
assert base.choose_k2(strikes, spot, k1, 'NEXT3') == 25150.0
assert base.choose_k2(strikes, spot, k1, 'MIRROR_GAP') is not None

print('504-family unit checks passed')