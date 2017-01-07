# func.py
from . const import *
import numpy as np
from collections import Counter

ss = [1,2,3,4,5]
ls = [6,2,3,4,5]

def isSmallStraight(a):
    return np.all(np.in1d(ss, a))

def isLargeStraight(a):
    return np.all(np.in1d(ls, a))

def isFullHouse(a):
    mc = Counter(a).most_common(2)
    return (mc[0][1] > 4 or (len(mc) > 1 and mc[0][1] == 3 and mc[1][1] == 2))

def isYatzy(a):
    return np.all(np.in1d(a, [a[0]]*5))

def isKindNumber2(a):
    mc = Counter(a).most_common(1)
    return mc[0][1] > 1

def isKindNumber3(a):
    mc = Counter(a).most_common(1)
    return mc[0][1] > 2

def isKindNumber4(a):
    mc = Counter(a).most_common(1)
    return mc[0][1] > 3

def isChange(a):
    c = Counter(a)
    return sum([k*v for k, v in c.items() if k > 2]) >= 15

def isNumberKindN(a, m=1, n=3):
    return a.count(m) >= n

def isNumberKind1(a):
    return isNumberKindN(a, m=1, n=5)

def isNumberKind2(a):
    return isNumberKindN(a, m=2, n=5)

def isNumberKind3(a):
    return isNumberKindN(a, m=3, n=5)

def isNumberKind4(a):
    return isNumberKindN(a, m=4, n=5)

def isNumberKind5(a):
    return isNumberKindN(a, m=5, n=5)

def isNumberKind6(a):
    return isNumberKindN(a, m=6, n=5)

def isPair(a):
    # see if given array contains any pair of numbers (xxyyz, xxxyy, xxxxy, xxxxx)
    mc = Counter(a).most_common(2)
    return len(mc) == 1 or mc[0][1] == 4 or (mc[0][1] > 1 and mc[1][1] > 1)

def isDouble(a):
    return len(set(a)) < len(a)

def isTriple(a):
    return Counter(a).most_common(1)[0][1] > 2

def isQuadruple(a):
    return Counter(a).most_common(1)[0][1] > 3

def yatzy(a):
    return YATZY_BONUS if isYatzy(a) else 0

def fullHouse(a):
    return (sum(a) if FULL_HOUSE_BONUS is None else FULL_HOUSE_BONUS) if isFullHouse(a) else 0

def change(a):
    return sum(a)

def smallStraight(a):
    return SMALL_STRAIGHT_BONUS if isSmallStraight(a) else 0

def largeStraight(a):
    return LARGE_STRAIGHT_BONUS if isLargeStraight(a) else 0

def pair(a):
    a = Counter(a).most_common(2)
    if a[0][1] > 3:
        return a[0][0]*4
    if a[0][1] > 1 and a[1][1] > 1:
        b = sorted(a, key=lambda x: x[0], reverse=True)
        return b[0][0]*2 + b[1][0]*2
    return 0

def kindNumber(a, n):
    # triple and quadruple
    if n > 2:
        a = {v: k for k, v in Counter(a).items()}
        if n in a:
            return a[n]*n
        elif n==3 and 4 in a:
            return a[4]*3
        elif n==3 and 5 in a:
            return a[5]*3
        elif n==4 and 5 in a:
            return a[5]*4
        return 0
    # double
    a = Counter(a).most_common(2)
    if a[0][1] > 1:
        b = sorted(a, key=lambda x: x[0], reverse=True)
        return b[0][0]*2
    return 0

def numberKind(a, n):
    return Counter(a)[n] * n

def numberKind1(a):
    return numberKind(a, 1)

def numberKind2(a):
    return numberKind(a, 2)

def numberKind3(a):
    return numberKind(a, 3)

def numberKind4(a):
    return numberKind(a, 4)

def numberKind5(a):
    return numberKind(a, 5)

def numberKind6(a):
    return numberKind(a, 6)

def kindNumber2(a):
    return kindNumber(a, 2)

def kindNumber3(a):
    return kindNumber(a, 3)

def kindNumber4(a):
    return kindNumber(a, 4)
