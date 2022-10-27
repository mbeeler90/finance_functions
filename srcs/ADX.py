import srcs.ATR as ATR

# Calculation of ADX indicator
def ADX(hist, indicator, look_back):
	if not 'ATR ' + str(look_back) in hist.columns:
		ATR.ATR(hist, 'ATR ' + str(look_back), look_back)

	# Set positive deviations (DM+) for up days and negative deviations (DM-) for down days
	for i in hist.index:
		if i > 0:
			if (hist.loc[i, 'High'] - hist.loc[i - 1, 'High'] > 0) and (hist.loc[i, 'High'] - hist.loc[i - 1, 'High'] >= hist.loc[i - 1, 'Low'] - hist.loc[i, 'Low']):
				hist.loc[i, 'DM+'] = hist.loc[i, 'High'] - hist.loc[i - 1, 'High']
				hist.loc[i, 'DM-'] = 0
			elif (hist.loc[i - 1, 'Low'] - hist.loc[i, 'Low'] > 0) and (hist.loc[i, 'High'] - hist.loc[i - 1, 'High'] < hist.loc[i - 1, 'Low'] - hist.loc[i, 'Low']): 
				hist.loc[i, 'DM+'] = 0
				hist.loc[i, 'DM-'] = hist.loc[i - 1, 'Low'] - hist.loc[i, 'Low']
			else:
				hist.loc[i, 'DM+'] = 0
				hist.loc[i, 'DM-'] = 0

	# Calculate smoothed averages for the positive / negative deviations
	for i in hist.index:
		DM_plus = 0
		DM_minus = 0
		if i == look_back:
			for time in range(look_back):
				DM_plus += hist.loc[time + 1, 'DM+']
				DM_minus += hist.loc[time + 1, 'DM-']
			hist.loc[i, 'DM+_smoothed'] = DM_plus
			hist.loc[i, 'DM-_smoothed'] = DM_minus
		elif i > look_back:
			hist.loc[i, 'DM+_smoothed'] = hist.loc[i - 1, 'DM+_smoothed'] * ((look_back - 1) / look_back) + hist.loc[i, 'DM+']
			hist.loc[i, 'DM-_smoothed'] = hist.loc[i - 1, 'DM-_smoothed'] * ((look_back - 1) / look_back) + hist.loc[i, 'DM-']

	# Calculate the absolute strenght of the trend (can be up- or down trend)
	hist['+DI_'+str(look_back)] = hist['DM+_smoothed'] / hist['ATR ' + str(look_back)] * 100
	hist['-DI_'+str(look_back)] = hist['DM-_smoothed'] / hist['ATR ' + str(look_back)] * 100
	hist['DX_'+str(look_back)] = abs(hist['+DI_' + str(look_back)] - hist['-DI_' + str(look_back)]) / abs(hist['+DI_' + str(look_back)] + hist['-DI_' + str(look_back)]) * 100

	# Calculate ADX as smoothed moving average of the daily trends
	for i in hist.index:
		ADX = 0
		if i < 2 * look_back - 1:
			continue
		elif i == 2 * look_back - 1:
			for time in range(look_back):
				ADX += hist.loc[i + time - look_back + 1, 'DX_' + str(look_back)]
			hist.loc[i, indicator] = ADX / look_back
		else:
			hist.loc[i, indicator] = hist.loc[i - 1, indicator] * ((look_back - 1) / look_back) + hist.loc[i, 'DX_' + str(look_back)] / look_back
