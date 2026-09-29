from phase8_weekly_engine import Quote, choose_strikes, expiry_payoff, locked_expiry_payoff

qs = [
    Quote(22100, 95, 105, 100),
    Quote(22150, 45, 55, 50),
    Quote(22200, 20, 30, 25),
    Quote(22250, 8, 12, 10),
]

k1, k2, k3, d, target = choose_strikes(22080, qs)
assert (k1.strike, k2.strike, k3.strike) == (22100, 22150, 22200)
assert d == 50
assert target == 100

pre_lock = expiry_payoff(22500, 22100, 22150, 22200, 10)
assert pre_lock < 0

post_lock = locked_expiry_payoff(22500, 22100, 22200, -5)
assert post_lock == 95

print("Phase 10W mechanics tests: PASS")
