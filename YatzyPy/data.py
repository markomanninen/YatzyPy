# data.py
import numpy as np
from itertools import product, combinations
from . func import *
from . const import *


# totally 31 hold options in two dimentional array
all_hold_options = np.array([list(combinations([0,1,2,3,4], r=repeat)) for repeat in range(1, 6)])
# plus one empty option, makes it 32 options
all_hold_options[0].append(())
# numbers from 1 to 6
numbers = range(1, 7)

# all unique ordered hands
hands = []
for hand in product(numbers, repeat=5):
    hand = list(hand)
    hand.sort(reverse=True)
    if hand not in hands:
        hands.append(hand)

file = 'yatzy_probabilities.csv'

# data table
data = {
    CHANGE: {'name': 'change', 'func': isChange, 'target': 17, 'order': 9, 'score': change},

    SMALLSTRAIGHT: {'name': 'smallstraight', 'func': isSmallStraight, 'target': SMALL_STRAIGHT_BONUS, 'order': 8, 'score': smallStraight},
    LARGESTRAIGHT: {'name': 'largestraight', 'func': isLargeStraight, 'target': LARGE_STRAIGHT_BONUS, 'order': 7, 'score': largeStraight},

    DOUBLE: {'name': 'double', 'func': isKindNumber2, 'target': 8, 'order': 6, 'score': kindNumber2},
    TRIPLE: {'name': 'triple', 'func': isKindNumber3, 'target': 12, 'order': 5, 'score': kindNumber3},
    PAIR: {'name': 'pair', 'func': isPair, 'target': 14, 'order': 4, 'score': pair},

    QUADRUPLE: {'name': 'quadruple', 'func': isKindNumber4, 'target': 14, 'order': 1, 'score': kindNumber4},
    FULLHOUSE: {'name': 'fullhouse', 'func': isFullHouse, 'target': (FULL_HOUSE_BONUS if FULL_HOUSE_BONUS else 20), 'order': 1, 'score': fullHouse},

    ONE: {'name': 'one', 'func': isNumberKind1, 'target': 3, 'order': 1, 'score': numberKind1},
    TWO: {'name': 'two', 'func': isNumberKind2, 'target': 6, 'order': 1, 'score': numberKind2},
    THREE: {'name': 'three', 'func': isNumberKind3, 'target': 9, 'order': 1, 'score': numberKind3},
    FOUR: {'name': 'four', 'func': isNumberKind4, 'target': 12, 'order': 1, 'score': numberKind4},
    FIVE: {'name': 'five', 'func': isNumberKind5, 'target': 15, 'order': 1, 'score': numberKind5},
    SIX: {'name': 'six', 'func': isNumberKind6, 'target': 18, 'order': 1, 'score': numberKind6},

    YATZY: {'name': 'yatzy', 'func': isYatzy, 'target': YATZY_BONUS, 'order': 1, 'score': yatzy}

}

categories = {k:v['name'] for k,v in data.items()}
functions = {k:v['func'] for k,v in data.items()}
targets = {k:v['target'] for k,v in data.items()}
scoring = {k:v['score'] for k,v in data.items()}
#order = [v['order'] for k,v in data.items()]
order = {k:v['order'] for k,v in data.items()}
