import pandas as pd

import srcs.moving_averages as MA
import srcs.ADX as ADX
import srcs.PSAR as PSAR

# call the function to add the selected indicator to df
def add_indicator(hist, ticker, indicator):
	# moving averages
	if indicator == '21 day DEMA':
		MA.double_exponential_moving_average(hist, indicator, 21)
	elif indicator == '21 day EMA':
		MA.exponential_moving_average(hist, indicator, 21)
	elif indicator == '21 day LWMA':
		MA.linear_weighted_moving_average(hist, indicator, 21)
	elif indicator == '21 day simple MA':
		MA.moving_average(hist, indicator, 21)
	elif indicator == '21 day Bollinger bands':
		MA.bollinger_bands(hist, indicator, 21)

	elif indicator == '14 day ADX':
		ADX.ADX(hist, indicator, 14)

	elif indicator == 'Parabolic SAR':
		PSAR.PSAR(hist)

	hist.to_csv('./data/'+ticker+'.csv')
