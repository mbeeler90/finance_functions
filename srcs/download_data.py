import pandas as pd
import numpy as np
import json

# Download the stock data for the ticker for the last year and save it to a csv file
def download_data(ticker, stock, period='1y', interval='1d'):
	i = 0
	hist = pd.DataFrame([])
	while hist.empty and i < 3:
		try:
			hist = stock.history(period = period, interval = interval, auto_adjust = True, timeout = 2)
			hist['Date'] = hist.index
			hist.reset_index(drop = True, inplace = True)
		except Exception as e:
			print(e)
		i += 1
	if hist.empty:
		return hist
	else:
		stock_info = download_stock_info(stock, ticker, hist)
		return hist, stock_info

# Download the stock information and save it in a text file.
def download_stock_info(stock, ticker, hist):
	stock_info = {
		'name': 'not available',
		'industry': 'not available',
		'price': 'not available',
		'return': 'not available',
		'forwardEPS': 'not available',
		'forwardPE': 'not available',
		'news': 'not available',
	}

	try:
		stock_tmp = stock.info
		stock_info['name'] = stock_tmp['shortName']
		stock_info['industry'] = stock_tmp['sector']
		stock_info['forwardEPS'] = round(stock_tmp['forwardEps'], 2)
		stock_info['forwardPE'] = round(stock_tmp['forwardPE'], 2)
		if np.isnan(hist.loc[max(hist.index), 'Close']):
			price = round(hist.loc[max(hist.index) - 1, 'Close'], 2)
			performance = round((hist.loc[max(hist.index) - 1, 'Close'] - hist.loc[0, 'Close']) / hist.loc[0, 'Close'] * 100, 2)
		else:
			price = round(hist.loc[max(hist.index), 'Close'], 2)
			performance = round((hist.loc[max(hist.index), 'Close'] - hist.loc[0, 'Close']) / hist.loc[0, 'Close'] * 100, 2)
		stock_info['price'] = price
		stock_info['return'] = performance
		stock_info['news'] = stock.news
	except Exception as e:
		print(e)
	return stock_info
