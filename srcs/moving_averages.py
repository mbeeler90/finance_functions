def exponential_moving_average(hist, indicator, look_back, price='Close'):
	if not str(look_back)+' day moving average' in hist.columns:
		moving_average(hist, str(look_back)+' day moving average', look_back)
	multiplier = 2 / (1 + look_back) 
	for i in hist.index:
		if i < look_back - 1:
			continue
		elif i == look_back - 1:
			hist.loc[i, indicator] = hist.loc[i, str(look_back)+' day moving average']
		else:
			hist.loc[i, indicator] = hist.loc[i, price] * multiplier + hist.loc[i-1, indicator] * (1-multiplier)

def moving_average(hist, indicator, look_back, price='Close'):
	hist[indicator] = hist[price].rolling(look_back).mean()