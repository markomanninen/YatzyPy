# main.py
from . func import *
from . data import *
from . const import *
import numpy as np
import pandas as pd
from numpy.random import randint
from operator import itemgetter


pd.set_option('display.max_colwidth', -1)

MAX_THROWS = 3

class Strategy:
    
    def __init__(self, yatzy=None):
        self.yatzy = yatzy
        self.indices = np.arange(5)
    
    def hold(self):
        """ hold repeating items, semi blind default hold strategy """
        # check others
        a = self.yatzy.hand
        b = np.array([x for x in np.array([np.argwhere(i==a).flatten() for i in np.unique(a)]) if len(x) > 1])
        if len(b):
            b = np.concatenate(b)
        else:
            b = []
        return b
        
    def select(self):
        """ select max category value, semi blind default select strategy """
        for k, v in self.yatzy.getSortedScoreTable():
            if k not in self.yatzy.scores:
                return k
        if self.yatzy.debug:
         	print("All scores done!")
        return None
    
class Yatzy:
    
    def __init__(self, hand=None, strategy=None, debug=False):
        self.scores = {}
        self.draw(hand)
        self.debug = debug
        self.strategy = strategy(self) if strategy else Strategy(self)

    def draw(self, hand=None):
        self.hand = self.roll() if hand is None else np.array(hand)
        self.throws = 1
    
    def roll(self, size=5):
        return randint(1, 7, size=size)
    
    def select(self, category):
        if category not in self.scores:
            self.scores[category] = self.getScoreTable()[category]
        elif self.debug:
        	print("Trying to select already existing category: %s" % category)
    
    def getTotalScore(self):
        upper_keys = [ONE, TWO, THREE, FOUR, FIVE, SIX]
        upper_vals = sum([v for k, v in self.scores.items() if k in upper_keys])
        lower_vals = sum([v for k, v in self.scores.items() if k not in upper_keys])
        total_vals = upper_vals+lower_vals
        return total_vals if upper_vals < UPPER_BONUS_THRESHOLD else total_vals+UPPER_BONUS
    
    def autoSelect(self):
        return self.strategy.select()
    
    def autoHold(self):
        return self.strategy.hold()
    
    def autoGame(self, r=15):
        """ Run 15 draws so that every category has been used """
        n = 0
        while n < r:
            # second round with hold suggestion
            suggested_hold = self.autoHold()
            if len(suggested_hold) < 5:
                self.hold(suggested_hold)
                # third round with hold suggestion
                suggested_hold = self.autoHold()
                if len(suggested_hold) < 5:
                    self.hold(suggested_hold)
            # suggest the category for the hand
            suggested_select = self.autoSelect()
            if suggested_select is not None:
                self.select(suggested_select)
            # make next draw
            self.draw()
            # mark iteration
            n += 1
    
    def getScoreTable(self):
        return {
            CHANGE: change(self.hand),
            YATZY: yatzy(self.hand),
            FULLHOUSE: fullHouse(self.hand),
            SMALLSTRAIGHT: smallStraight(self.hand),
            LARGESTRAIGHT: largeStraight(self.hand),
            PAIR: pair(self.hand),
            ONE: numberKind1(self.hand),
            TWO: numberKind2(self.hand),
            THREE: numberKind3(self.hand),
            FOUR: numberKind4(self.hand),
            FIVE: numberKind5(self.hand),
            SIX: numberKind6(self.hand),
            DOUBLE: kindNumber2(self.hand),
            TRIPLE: kindNumber3(self.hand),
            QUADRUPLE: kindNumber4(self.hand)
        }

    def getSortedScoreTable(self, reverse=True):
        return sorted(self.getScoreTable().items(), key=itemgetter(1), reverse=reverse)
    
    def hold(self, hold):
        if self.throws < MAX_THROWS:
            l = len(hold)
            if l < 5:
                take = np.take(self.hand, hold)
                roll = self.roll(5-l)
                self.hand = np.append(take, roll)
            self.throws += 1

    def show(self):
        category = self.autoSelect()
        hold = self.autoHold()
        return '<div><p>%s</p><br/><p>Suggested category: %s | Hold: %s | Score: %s</p></div>' % \
                    (self.dices(hold), categories[category], hold, self.getScoreTable()[category])

    def dices(self, hold):
        return '<div class="cats">%s</div>' % (''.join(['<div class="cat%s%s"></div>' % \
                (k, ' hold' if i in hold else '') for i, k in enumerate(sorted(self.hand, reverse=True))]))
