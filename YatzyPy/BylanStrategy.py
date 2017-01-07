# BylanStrategy.py
import pandas as pd
import numpy as np
from . main import Strategy, Yatzy
from numpy.random import shuffle
from IPython.display import HTML
from . data import targets, order, categories
from . func import ss, ls
from . const import *

#category_reselection = [0, 3, 4, 14, 1, 2, 5, 13, 12, 6, 7, 8, 9, 10, 11]
category_reselection = [3, 4, 0, 14, 2, 1, 13, 5, 12, 6, 7, 8, 9, 10, 11]
probability_lengths = {0:4, 3:5, 4:5, 14:4, 1:5, 2:5, 5:4, 13:3, 12:2, 6:3, 7:3, 8:3, 9:3, 10:3, 11:3}
upper = {6:1, 7:2, 8:3, 9:4, 10:5, 11:6}

def get_hold(category, hand):
    hold = ()
    # FULLHOUSE
    if category == FULLHOUSE:
        n = [i for k, i in upper.items() if hand.count(i) > 1]
        hold = tuple([i for i, v in enumerate(hand) if v in n])
    # PAIR
    if category == PAIR:
        hold = []
        a = {}
        for i, v in enumerate(hand):
            a[v] = a[v] if v in a else []
            if hand.count(v) > 3:
                if len(a[v]) < 4:
                    a[v].append(i)
            elif hand.count(v) > 1:
                if len(a[v]) < 2:
                    a[v].append(i)
        for k, v in a.items():
            hold.extend(v)
        hold.sort()
        hold = tuple(hold)
    # CHANGE
    elif category == CHANGE:
        # hold numbers only bigger than 3
        hold = tuple([i for i, v in enumerate(hand) if v > 3])
    # SMALLSTRAIGHT
    elif category == SMALLSTRAIGHT:
        hold = tuple([hand.index(v) for v in ss if v in hand])
    # LARGESTRAIGHT
    elif category == LARGESTRAIGHT:
        hold = tuple([hand.index(v) for v in ls if v in hand])
    # UPPER CATEGORIES
    elif category in upper:
        hold = tuple([i for i, v in enumerate(hand) if v == upper[category]])
    # DOUBLE, TRIPLE, QUADRUPLE, YATZY
    elif category in [DOUBLE, TRIPLE, QUADRUPLE, YATZY]:
        # double must restrict max count to 2 because [1,1,1,2,2] should return 2 as the biggest double.
        if category == DOUBLE:
            l = list((i, 2 if hand.count(i) > 1 else hand.count(i)) for k, i in upper.items())
        # triple, quadruple and yatzy just the biggest
        else:
            l = list((i, hand.count(i)) for k, i in upper.items())
        if len(l) > 0:
            # sort by value, then sort by key, for double biggest is used
            l.sort(key=lambda tpl: (tpl[1], tpl[0]), reverse=True)
            n = l[0][0]
            # detect how many items should we select for each category
            o = {12:2, 13:3, 14:4, 1:5}[category]
            hold = tuple([i for i, v in enumerate(hand) if v == n][:o])
    return hold

def no_leftovers(category, scores, value):
    # sum up all upper category scores available except given category
    # add value of given category to the sum and compare to upper categories bonus: 63
    return UPPER_BONUS_THRESHOLD > sum([scores[i] if i in scores else targets[i] for i, v in upper.items() if i is not category]) + value
    """
    d = {k:v for k, v in scores.items() if k in [7,8,9,10] and k > category}
    for k, v in d.items():
        if v >= targets[k]:
            return False
    return True
    """

class BylanStrategy(Strategy):
    """
    from YatzyPy import Yatzy, BylanStrategy
    c = Yatzy(strategy=BylanStrategy)
    c.autoGame()
    print(c.getTotalScore(), {categories[k]: v for k, v in c.scores.items()})
    """
    
    def __init__(self, yatzy=None):
        super(Strategy, self).__init__()
        self.yatzy = yatzy
        if yatzy.debug and 'dfs' not in yatzy.__dict__:
            yatzy.dfs = {}
            self.dfs = []
    
    def hold(self):
        return get_hold(self.select_category(), self.yatzy.hand)
    
    def select(self):
        category = self.select_category()
        # if upper category is selected but it doesn't meet score target criteria and upper categories
        # are not going to be filled with it
        if category in upper and \
            self.yatzy.getScoreTable()[category] < targets[category] and \
            no_leftovers(category, self.yatzy.scores, self.yatzy.getScoreTable()[category]):
            # select the most unprobable and least giving score category option from remaining categories
            # CHANGE, SMALLCHANGE, LARGECHANGE, QUADRUPLE, YATZY, FULLHOUSE, TRIPLE, PAIR, DOUBLE, ONE, TWO,...
            # varying this table might give different average score, so run with all different combinations
            for c in category_reselection:
                if c not in self.yatzy.scores:
                    category = c
                    # show reselected category on debug dataframe
                    if self.yatzy.debug:
                        self.dfs[len(self.dfs)-1].set_value(0, 'reselect', category)
                    break
        # for debugging purposes collect dataframes for each draw
        if self.yatzy.debug:
            self.yatzy.dfs[category] = {'order': len(self.yatzy.dfs), 'dfs': self.dfs}
            # reset dataframes for the set of 1 to 3 hands (draw)
            self.dfs = []
        return category
    
    # len hold - len target 
    # how many dices to roll = a = 5 - len hold
    # how many dices to target = b = len target - len hold
    # probability = a/6^b -> 1/6^1 [1,2,3,4,x]
    def select_category(self):
        yatzy = self.yatzy
        if yatzy.debug:
            ll = len(self.dfs)
            # if last hold is 5, then no need to proceed more
            if ll > 0 and len(self.dfs[ll-1]['hold'][0]) == 5:
                # return the last category
                return self.dfs[ll-1]['category'][0]
        # sort hand
        hand = list(yatzy.hand)
        hand.sort(reverse=True)
        yatzy.hand = hand
        # get all maximum holds for each category
        holds = {k: get_hold(k, yatzy.hand) for k, v in categories.items()}
        # calculate threshold and simple probability
        rows = [{
                'hand': yatzy.hand, 
                'category': k, 
                'name': categories[k], 
                'hold': holds[k], 
                'order': order[k], 
                'score': v, 
                'reselect': '', 
                'threshold': 1 if v >= targets[k] else 0, 
                # TODO: probability calculation could be more sophisticated...
                'probability': 1 if probability_lengths[k] - len(holds[k]) <= 0 else (1/6**(probability_lengths[k] - len(holds[k])))*(5-len(holds[k])/6)
                } for k, v in yatzy.getScoreTable().items() if k not in yatzy.scores]
        # sort rows
        rows.sort(key=lambda r: [-r['threshold'], -r['probability'], r['order'], -r['score']])
        # for visually appealing debug use pandas dataframes to collect data
        if yatzy.debug:
            self.dfs.append(pd.DataFrame(rows))
        # return the best category
        return rows[0]['category']

def toDices(row):
    return '<div class="cats">%s</div>' % (''.join(['<div class="cat%s%s"></div>' % \
            (k, ' hold' if i in row['hold'] else '') for i, k in enumerate(row['hand'])]))

def _get_df(s):
    """ vertical results """
    d = pd.concat([x[:1] for x in s])
    d[''] = d.apply(toDices, axis=1)
    del d['threshold']
    del d['order']
    del d['probability']
    del d['score']
    d['name'] = d.apply(lambda row: "%s%s" % (row['name'], " (%s)" % categories[row['reselect']] if row['reselect'] != "" and row['reselect'] != row['category'] else ""), axis=1)
    del d['category']
    del d['reselect']
    return d.to_html(escape=False)

def get_df(s, n):
    """ horizontal results """
    d = None
    for i, x in enumerate(s):
        i += 1
        if d is None:
            d = pd.DataFrame(x[:n])

            d['name'] = d.apply(lambda row: "%s%s" % (row['name'], " (%s)" % categories[row['reselect']] if row['reselect'] != "" and row['reselect'] != row['category'] else ""), axis=1)
            
            if n == 1:
                d['dice %s'%i] = d.apply(toDices, axis=1)
                del d['threshold']
                del d['order']
                del d['probability']
                del d['score']
            del d['category']
            del d['reselect']
        else:
            d['hand %s'%i] = x[:n]['hand']
            d['hold %s'%i] = x[:n]['hold']

            d['name %s'%i] = x[:n].apply(lambda row: "%s%s" % (row['name'], " (%s)" % categories[row['reselect']] if row['reselect'] != "" and row['reselect'] != row['category'] else ""), axis=1)
   
            if n == 1:
                d['dice %s'%i] = x[:n].apply(toDices, axis=1)
            else:
                d['threshold %s'%i] = x[:n]['threshold']
                d['order %s'%i] = x[:n]['order']
                d['probability %s'%i] = x[:n]['probability']
                d['score %s'%i] = x[:n]['score']
            
    # add score column to the end?
    d['total score'] = x[:n].apply(lambda row: row['score'] if row['reselect'] == '' else 0, axis=1)
    return d.to_html(escape=False)

def print_game(c, n=1):
    s = sorted([v for k, v in c.dfs.items()], key=lambda k: k['order'])
    return HTML("<br/>Total score: %s" % c.getTotalScore() + ". All 15 draws:<br/>" + ''.join([get_df(v['dfs'], n) for v in s]))

def strategyaveragescore(r=100, strategy=None, debug=False):
    totals = []
    n = 0
    mx = [-np.inf, None]
    mn = [np.inf, None]
    while n < r:
        c = Yatzy(strategy=strategy, debug=debug)
        c.autoGame()
        s = c.getTotalScore()
        totals.append(s)
        if mx[0] < s:
            mx[0] = s
            mx[1] = c
        if mn[0] > s:
            mn[0] = s
            mn[1] = c
        n += 1

    res = max(totals), min(totals), round(sum(totals)/n, 2), mn, mx
    print("max: %d min: %d total average: %f mn: %s mx%s" % res)
    return res

def find_optimal_category_selection(n=2):
    global category_reselection
    avg = 0
    for i in range(1,n):
        mx, mn, av, m, n = strategyaveragescore(r=100, strategy=BylanStrategy)
        if avg < av:
            avg = av
            print('MAX', avg, category_reselection)
        shuffle(category_reselection)

