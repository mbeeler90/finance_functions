import pandas as pd
import numpy as np
import datetime

# download the stock data for the ticker for the last year and save it in csv file
def download_data(ticker, stock, period='1y', interval='1d'):
	i = 0
	hist = pd.DataFrame([])
	while hist.empty and i < 3:
		try:
			hist = stock.history(period = period, interval = interval, auto_adjust = True, timeout=2)
			hist['Date'] = hist.index
			hist.reset_index(drop = True, inplace=True)
		except Exception as e:
			print(e)
		i += 1
	if hist.empty:
		return hist
	else:
		hist.to_csv('./data/'+ticker+'.csv')
		return hist
