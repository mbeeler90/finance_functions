import pandas as pd

import srcs.moving_averages as MA
import srcs.ADX as ADX

# call the function to add the selected indicator to df
def add_indicator(hist, ticker, indicator):
	# moving averages
	if indicator == '21 day exponential moving average':
		MA.exponential_moving_average(hist, indicator, 21)
	elif indicator == '21 day moving average':
		MA.moving_average(hist, indicator, 21)

	elif indicator == '14 day ADX':
		ADX.ADX(hist, indicator, 14)

	hist.to_csv('./data/'+ticker+'.csv')
