import pandas as pd

import srcs.moving_averages as MA
import srcs.ADX as ADX
import srcs.PSAR as PSAR
import srcs.aroon as aroon
import srcs.oscillators as oscillators

# Call the function to add the selected indicator to df
def add_indicator(hist, ticker, indicator):
	# Moving averages
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
	elif indicator == '12 / 26 day MACD':
		MA.MACD(hist, indicator, 12, 26, 9)

	elif indicator == '14 day ADX':
		ADX.ADX(hist, indicator, 14)

	elif indicator == 'Parabolic SAR':
		PSAR.PSAR(hist)

	elif indicator == '25 day Aroon indicator':
		aroon.aroon(hist, indicator, 25)

	# Oscilators
	elif indicator == '14 day stochastic oscillator':
		oscillators.stochastic(hist, indicator, 14)
	elif indicator == '14 day RSI':
		oscillators.RSI(hist, indicator, 14)
	elif indicator == '3 / 10 day Chaikin indicator':
		oscillators.chaikin(hist, indicator, 3, 10)

	hist.to_csv('./data/' + ticker + '.csv', index = False)
