# setup.py
import pandas as pd
from itertools import product
from . data import file as csvfile, hands, functions, numbers, all_hold_options

# different number products to be used on the probability calculation
products = {n:list(product(numbers, repeat=n)) for n in [0,1,2,3,4,5]}

def save_probabilities(file=None):
	file = file if file else csvfile
	try:
		df = pd.read_csv(file, sep='\t')
		del df['Unnamed: 0']
	except:
		df = pd.DataFrame(columns=['hand', 'hold', 'probability', 'category'])

	r=0
	for hand in hands:
		hand.sort(reverse=True)
		c = get_probabilities(hand)
		for k, v in c.items():
			df = df.append(pd.DataFrame([[hand, v[1], v[2], int(k)]], columns=['hand', 'hold', 'probability', 'category'], index=[r]))
			r += 1
		df.to_csv(file, sep='\t')

def dice_face_probability_with_hold(function, hold=(), n=2):
	# p max combinations, q_1 is combinations that will give true from given function
	p, q = 6**n, sum(function(x+hold) for x in products[n])
	# (probability, sum, max)
	return [q / p, q, p]

def get_probabilities(hand):
	# numbers in descending order, important to get the smallest biggest probability
	hand.sort(reverse=True)
	# result set
	result = {}
	# dictionary of categories that we should find out the probability
	for key, function in functions.items():
		# go thru all hold options
		for holds in all_hold_options:
			# there are 32 different holds (index combinations)
			for hold_indices in holds:
				# length of the hold: 0 - 5
				n = 5-len(hold_indices)
				# list of items from the current hand based on hold indices
				hold_numbers = tuple([hand[h] for h in hold_indices])
				# initialize result set with the given key
				if key not in result:
					# 1. current hand
					# 2. the best hold_indices
					# 3. the best probability
					result[key] = [hand, (), 0]
				# get the probability. it will take around 10µs.
				# so max time is 32 times 10µs, or around 0.3 seconds
				p = dice_face_probability_with_hold(function, hold=hold_numbers, n=n)
				# if the probability is greater than previous ones, use it
				if p[0] > result[key][2]:
					result[key][1] = hold_indices
					result[key][2] = p[0]
	# return final results
	return result
