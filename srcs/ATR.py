import numpy as np

# Calculation of average true range.
def ATR(hist, indicator, look_back):           
	for i in hist.index:
		if i > 0:
			high_low = hist.loc[i, 'High'] - hist.loc[i, 'Low']
			high_close = np.abs(hist.loc[i, 'High'] - hist.loc[i - 1, 'Close'])
			low_close = np.abs(hist.loc[i, 'Low'] - hist.loc[i - 1, 'Close'])
			hist.loc[i, 'TR'] = np.max([high_low, high_close, low_close])
	hist[indicator] = hist['TR'].rolling(look_back).mean()
