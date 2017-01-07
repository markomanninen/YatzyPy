#MyStrategy.py
import numpy as np
from . func import *
from . const import *
from . main import Strategy

class MyStrategy(Strategy):
	""" use probability table to maximize scores """
	def hold(self):
		""" ... """
		# check small straight
		if SMALLSTRAIGHT not in self.yatzy.scores and isSmallStraight(self.yatzy.hand):
			return np.array([0,1,2,3,4])
		# check large straight
		elif LARGESTRAIGHT not in self.yatzy.scores and isLargeStraight(self.yatzy.hand):
			return np.array([0,1,2,3,4])
		elif FULLHOUSE not in self.yatzy.scores and isFullHouse(self.yatzy.hand) and sum(self.yatzy.hand) > 15:
			return np.array([0,1,2,3,4])
		# check others by trying to get upper part of the score table ready first
		a = self.yatzy.hand
		# get repeating item indices. if full house or pair has been used, then you might not hold whole set
		b = np.array([x for x in np.array([np.argwhere(i==a).flatten() for i in np.unique(a)]) if len(x) > 1])
		if len(b):
			b = np.concatenate(b)
		else:
			b = []
		return b
	"""
	def select(self):
		pass
	"""
