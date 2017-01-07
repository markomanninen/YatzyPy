# tests.py
from . main import Yatzy

def runTests():
    c = Yatzy([5, 5, 6, 5, 6])
    s = c.getScoreTable()
    assert s['change'] == 27 and s['fullhouse'] == 27
    assert s['double'] == 12 and s['six'] == 12
    assert s['five'] == 15 and s['triple'] == 15
    assert s['pair'] == 22
    
    c = Yatzy([5, 5, 5, 5, 5])
    s = c.getScoreTable()
    assert s['change'] == 25 and s['fullhouse'] == 25 and s['five'] == 25
    assert s['double'] == 10
    assert s['triple'] == 15
    assert s['pair'] == 20 and s['quadruple'] == 20
    assert s['yatzy'] == 50
    
    c = Yatzy([4,4,4,4,1])
    s = c.getScoreTable()
    assert s['change'] == 17
    assert s['double'] == 8
    assert s['triple'] == 12
    assert s['one'] == 1
    assert s['pair'] == 16 and s['quadruple'] == 16

    c = Yatzy([3,3,3,2,1])
    s = c.getScoreTable()
    assert s['change'] == 12
    assert s['double'] == 6
    assert s['triple'] == 9 and s['three'] == 9
    assert s['one'] == 1
    assert s['two'] == 2

    c = Yatzy([3,3,4,2,1])
    s = c.getScoreTable()
    assert s['change'] == 13
    assert s['one'] == 1
    assert s['two'] == 2
    assert s['four'] == 4
    assert s['three'] == 6 and s['double'] == 6

    c = Yatzy([3,5,4,2,1])
    s = c.getScoreTable()
    assert s['change'] == 15 and s['smallstraight'] == 15
    assert s['one'] == 1
    assert s['two'] == 2
    assert s['three'] == 3
    assert s['four'] == 4
    assert s['five'] == 5

    c = Yatzy([3,5,4,2,6])
    s = c.getScoreTable()
    assert s['change'] == 20 and s['largestraight'] == 20
    assert s['six'] == 6
    assert s['two'] == 2
    assert s['three'] == 3
    assert s['four'] == 4
    assert s['five'] == 5

    c = Yatzy([3,5,4,1,6])
    s = c.getScoreTable()
    assert s['change'] == 19
    assert s['six'] == 6
    assert s['one'] == 1
    assert s['three'] == 3
    assert s['four'] == 4
    assert s['five'] == 5

    c = Yatzy([3,3,4,4,5])
    s = c.getScoreTable()
    assert s['change'] == 19
    assert s['three'] == 6
    assert s['four'] == 8 and s['double'] == 8
    assert s['five'] == 5
    assert s['pair'] == 14
