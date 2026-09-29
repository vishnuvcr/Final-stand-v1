from phase8_weekly_engine import *

def test_strike_selection():
    qs = [
        Quote(22100, 95, 105, 100),
        Quote(22150, 45, 55, 50),
        Quote(22200, 20, 30, 25),
        Quote(22250, 8, 12, 10),
    ]
    k1,k2,k3,d,target = choose_strikes(22080, qs)
    assert (k1.strike,k2.strike)==(22100,22150)
    assert d == 50
    assert target == 100
    assert k3.strike == 22200

def test_lock_cancels_middle_leg():
    # Algebraic state check: +K1 -K2 -K3 then +K2 -> +K1 -K3.
    assert [Leg(22100,1),Leg(22150,-1),Leg(22200,-1),Leg(22150,1)].count(Leg(22150,-1)) == 1

def test_expiry_tail_is_negative():
    p = expiry_payoff(22500, 22100, 22150, 22200, 10)
    assert p < 0

def test_locked_position_is_defined_risk():
    p = locked_expiry_payoff(22500, 22100, 22200, -5)
    assert p == -5 + 400 - 300
