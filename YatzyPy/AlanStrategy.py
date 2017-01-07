# AlanStrategy.py
from . data import file as csvfile, categories, targets, functions, scoring, order
import pandas as pd
from . main import Strategy

probabilities = None

def process_category(x):
	return int(x)

def process_hand(x):
	return tuple(map(int, x.replace('[', '').replace(']', '').replace(' ', '').split(',')))

def process_hold(x):
	x = x.replace('(', '').replace(',)', '').replace(')', '').replace(' ', '')
	if x:
		return tuple(map(int, x.split(',')))
	return ()

def process_probability(x):
	# upper categories are 1,6,36 because at least 3 same numbers is required to get the upper bonus
	# yet probability is calculated by getting 5 same numbers!
    if x['category'] in [6,7,8,9,10,11] and len(x['hold']) > 2:
        return x['probability'] * 36
    # yatzies are 36 to make it sure it competes with upper categories maximum ie 36
    if x['category'] == 1 and x['probability'] == 1:
        return x['probability'] * 36
    return x['probability']

def read_probabilities(file=None):
	global probabilities
	file = file if file else csvfile
	try:
		df = pd.read_csv(file, sep='\t')
		try:
			del df['Unnamed: 0']
		except:
			pass
		df['category'] = df['category'].apply(process_category)
		df['hand'] = df['hand'].apply(process_hand)
		df['hold'] = df['hold'].apply(process_hold)
		df['probability'] = df.apply(process_probability, axis=1)
		probabilities = df
	except:
		print('Cannot read probabilities file: %s. Make sure you have created it by running setup.save_probabilities() function.' % file)
		probabilities = pd.DataFrame([], columns=['hand', 'hold', 'probability', 'category'])

def get_probability_and_hold(hand, category):
	result = probabilities[probabilities['hand'] == tuple(hand)]
	result = result[result['category'] == category]
	if len(result):
		return float(result['probability']), tuple(result['hold'])[0]
	return 0, ()

def get_probabilities(hand, probability_functions):
	# numbers in descending order, important to get the smallest biggest probability
	hand.sort(reverse=True)
	# result set
	result = {}
	# dictionary of categories that we should find out the probability
	for key, function in probability_functions.items():
		p, hold = get_probability_and_hold(hand, key)
		result[key] = [hand, hold, p]
	# return final results
	return result

def dataframe_probabilities(P):
	df = pd.DataFrame(P).T
	df.rename(columns={
				0: 'Hand',
				1: 'Hold', 
				2: 'Probability'}, inplace=True)
	df['Category'] = df.apply(lambda row: categories[row.name], axis=1)
	df['Aim_Score'] = df.apply(lambda row: targets[row.name], axis=1)
	df['Cur_Score'] = df.apply(lambda row: scoring[row.name](row['Hand']), axis=1)
	df['Threshold'] = df['Cur_Score'] >= df['Aim_Score']
	df['Order'] = [order[k] for k,v in P.items()]
	return df.sort_values(by=['Threshold', 'Probability', 'Order'], ascending=[0, 0, 1])


#dice = {1: '⚀', 2: '⚁', 3: '⚂', 4: '⚃', 5: '⚄', 6: '⚅'}

def toDices(row):
	return '<div class="cats">%s</div>' % (''.join(['<div class="cat%s%s"></div>' % \
			(k, ' hold' if i in row['Hold'] else '') for i, k in enumerate(row['Hand'])]))

class AlanStrategy(Strategy):
	""" use probability table to maximize scores """
	
	def hold(self):
		""" ... """
		y = self.yatzy
		# select only categories, that are not used yet
		p = {k:v for k,v in functions.items() if k not in y.scores}
		#hand = [i for i in y.hand]
		hand = list(y.hand)
		df = dataframe_probabilities(get_probabilities(hand, p))
		if 'dfs' not in self.__dict__:
			self.dfs = []
		self.dfs.append(df)
		y.hand = df['Hand'].iloc[0]
		if y.debug:
			print ('#%s' % y.throws, 'hand', hand, 'hold', df['Hold'].iloc[0], 'Target category:', categories[df.iloc[0].name].upper())
		return df['Hold'].iloc[0]
	
	def select(self):
		y = self.yatzy
		p = {k:v for k,v in functions.items() if k not in y.scores}
		hand = list(y.hand)
		df = dataframe_probabilities(get_probabilities(hand, p))
		self.dfs.append(df)
		category = df.iloc[0].name
		if y.debug:
			print ('#%s' % y.throws, 'hand', hand, 'Selected category:', categories[category].upper(), 'Score:', y.getScoreTable()[category])
			print()
		if 'dfs' not in y.__dict__:
			y.dfs = {}
		y.dfs[category] = {'order': len(y.dfs), 'dfs': self.dfs}
		self.dfs = []
		# if upper is not ready, then do not select one with upper key!
		return category

#res=yatzy.dfs
def get_score_table(res):
	d = pd.concat([x[:1] for x in res])
	d[''] = d.apply(toDices, axis=1)
	del d['Aim_Score']
	del d['Threshold']
	del d['Order']
	return d.to_html(escape=False)

read_probabilities()
