from itertools import product

K1_RULES = [*[f'OTM{i}' for i in range(1,9)], 'ATM_NEAREST', 'ATM_UP', *[f'ITM{i}' for i in range(1,9)]]
K2_RULES = ['NEXT1','NEXT2','NEXT3','MIRROR_GAP']
K3_MULTIPLIERS = [0.5,1.0,1.5,2.0,2.5,3.0,4.0]
VARIANT_IDS = [f'{a}_{b}_K3M{m:g}' for a,b,m in product(K1_RULES,K2_RULES,K3_MULTIPLIERS)]

assert len(K1_RULES) == 18
assert len(VARIANT_IDS) == 504

def choose_k1(strikes, spot, rule):
    s=sorted(set(float(x) for x in strikes))
    if rule.startswith('OTM'):
        n=int(rule[3:]); c=[k for k in s if k>spot]; return c[n-1] if len(c)>=n else None
    if rule.startswith('ITM'):
        n=int(rule[3:]); c=[k for k in s if k<spot]; return c[-n] if len(c)>=n else None
    if rule=='ATM_NEAREST': return min(s,key=lambda k:(abs(k-spot),-k))
    if rule=='ATM_UP':
        c=[k for k in s if k>=spot]; return c[0] if c else None
    raise ValueError(rule)

def choose_k2(strikes, spot, k1, rule):
    h=sorted(k for k in set(float(x) for x in strikes) if k>k1)
    if rule.startswith('NEXT'):
        n=int(rule[4:]); return h[n-1] if len(h)>=n else None
    if rule=='MIRROR_GAP':
        g=abs(spot-k1); return min(h,key=lambda k:(abs((k-k1)-g),k)) if h else None
    raise ValueError(rule)

strikes = [25000 + 50*i for i in range(-20, 21)]
spot = 25000.0
assert choose_k1(strikes, spot, 'OTM8') == 25400.0
assert choose_k1(strikes, spot, 'ITM8') == 24600.0
k1 = choose_k1(strikes, spot, 'OTM8')
assert choose_k2(strikes, spot, k1, 'NEXT3') == 25550.0
assert choose_k2(strikes, spot, k1, 'MIRROR_GAP') == 25800.0

print('504-family unit checks passed')