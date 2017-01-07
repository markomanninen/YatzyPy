# __init__.py
from . setup import save_probabilities
from . main import Strategy, Yatzy
from . AlanStrategy import AlanStrategy, get_score_table, probabilities
from . BylanStrategy import BylanStrategy, print_game, strategyaveragescore
from . MyStrategy import MyStrategy
from . tests import runTests
from . data import targets, order, categories, functions, hands, scoring, data
from . func import *