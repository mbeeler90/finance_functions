def aroon(hist, indicator, look_back, price='Close'):
	for i in hist.index:
		if i >= look_back:
			high_number = 0
			low_number = 999999999
			for periods in range((look_back+1)):
				if hist.loc[i + periods - look_back, price] > high_number:
					high = look_back - periods
					high_number = hist.loc[i + periods - look_back, price] 
				if hist.loc[i + periods - look_back, price] < low_number:
					low = look_back - periods
					low_number = hist.loc[i + periods - look_back, price] 
			hist.loc[i, indicator+' up'] = (look_back - high)*100/look_back
			hist.loc[i, indicator+' down'] = (look_back - low)*100/look_back
