# Calculation of stochastic oscillator. Get the highest and lowest price in the look_back 
# period for every day and calculate where the current day price is in this range.
def stochastic(hist, indicator, look_back, MA = 3, price = 'Close'):
	for i in hist.index:
		if i >= look_back - 1:
			high = 0
			low = 9999999
			for time in range(look_back):
				if hist.loc[i - time, price] > high:
					high = hist.loc[i - time, price]
					hist.loc[i, indicator + '_high'] = high
				if hist.loc[i - time, price] < low:
					low = hist.loc[i - time, price]
					hist.loc[i, indicator + '_low'] = low
	hist[indicator] = 100 * (hist[price] - hist[indicator + '_low']) / (hist[indicator + '_high'] - hist[indicator + '_low'])
	hist[indicator + ' moving average'] = hist[indicator].rolling(MA).mean()

# Calculation of relative strength index. For every day, calculate the difference to
# the previous day. Add up all positive / negative differences during the look_back
# period. Get the relation between the sum positive / negative differences to calculate
# the RSI.
def RSI(hist, indicator, look_back, price = 'Close'):
	hist['diff'] = hist[price] - hist[price].shift()
	for i in hist.index:
		if hist.loc[i, 'diff'] >= 0:
			hist.loc[i, 'plus'] = hist.loc[i, 'diff'] 
			hist.loc[i, 'minus'] = 0
		else:
			hist.loc[i, 'minus'] = -hist.loc[i, 'diff'] 
			hist.loc[i, 'plus'] = 0
	hist['sum_plus'] = hist['plus'].rolling(look_back).sum()
	hist['sum_minus'] = hist['minus'].rolling(look_back).sum() 
	for i in hist.index:
		if i == look_back:
			hist.loc[i, indicator] = 100 - (100 / (1 + hist.loc[i, 'sum_plus'] / hist.loc[i, 'sum_minus'])) 
		elif i > look_back:
			hist.loc[i, indicator] = 100 - (100 / (1 + ((hist.loc[i - 1, 'sum_plus'] * (look_back - 1) / look_back) + hist.loc[i, 'plus']) / ((hist.loc[i - 1, 'sum_minus'] * (look_back - 1) / look_back) + hist.loc[i, 'minus']))) 

# Calculation of Chaikin indicator. Calculate whether the close price is closer to the high
# or low and multiply by the volume. Add up these numbers. Calculate a fast and a slow
# exponential moving averages of the result and slow from the fast average to get the result.
def chaikin(hist, indicator, low_EMA, high_EMA):
	hist[indicator] = float('NaN')
	hist['ADI'] = (2 * hist['Close'] - hist['Low'] - hist['High']) / (hist['High'] - hist['Low']) * hist['Volume']
	for i in hist.index:
		if i == 0:
			hist.loc[i, 'ADL'] = hist.loc[i, 'ADI']
		else:
			hist.loc[i, 'ADL'] = hist.loc[i - 1, 'ADL'] + hist.loc[i, 'ADI']
	for days in [low_EMA, high_EMA]:
		multiplier = 2 / (1 + days) 
		for i in hist.index:
			if i == days - 1:
				sum = 0
				for day in range(days):
					sum += hist.loc[i - day, 'ADL']
					hist.loc[i, 'EMA_ADL_' + str(days)] = sum / days
			elif i > days - 1:
				hist.loc[i, 'EMA_ADL_' + str(days)] = hist.loc[i, 'ADL'] * multiplier + hist.loc[i - 1, 'EMA_ADL_' + str(days)] * (1 - multiplier)
	hist[indicator] = hist['EMA_ADL_' + str(low_EMA)] - hist['EMA_ADL_' + str(high_EMA)]
