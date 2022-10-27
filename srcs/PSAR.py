# Calculation of parabolic stop and reverse. Set for every period whether PSAR is
# falling or rising and set the prior / current highs / lows accordingly.
def PSAR(hist):
	for i in hist.index:
		if i < 5:
			continue
		elif i == 5:
			if hist.loc[i, 'Close'] <= hist.loc[0, 'Close']:
				set_FPSAR(hist, i)
			else: 
				set_RPSAR(hist, i)				
		else:
			if hist.loc[i - 1, 'RPSAR'] > 0:
				if hist.loc[i, 'High'] > hist.loc[i - 1, 'Prior_high']:
					set_high(hist, i)
					hist.loc[i, 'Prior_high'] = hist.loc[i, 'High']
					hist.loc[i, 'Prior_high_count'] = min(10, (hist.loc[i - 1, 'Prior_high_count'] + 1))
					hist.loc[i, 'RPSAR'] = hist.loc[i - 1, 'RPSAR'] + 0.02 * hist.loc[i, 'Prior_high_count'] * (hist.loc[i, 'Prior_high'] - hist.loc[i - 1, 'RPSAR'])
					if hist.loc[i, 'RPSAR'] > hist.loc[i, 'Close']:
						set_FPSAR(hist, i)
				else:
					set_high(hist, i)
					hist.loc[i, 'Prior_high'] = hist.loc[i - 1, 'Prior_high']
					hist.loc[i, 'Prior_high_count'] = hist.loc[i - 1, 'Prior_high_count']
					hist.loc[i, 'RPSAR'] = hist.loc[i - 1, 'RPSAR'] + 0.02 * hist.loc[i, 'Prior_high_count'] * (hist.loc[i, 'Prior_high'] - hist.loc[i - 1, 'RPSAR'])
					if hist.loc[i, 'RPSAR'] > hist.loc[i, 'Close']:
						set_FPSAR(hist, i)
			else:
				if hist.loc[i, 'Low'] < hist.loc[i - 1, 'Prior_low']:
					set_low(hist, i)
					hist.loc[i, 'Prior_low'] = hist.loc[i, 'Low']
					hist.loc[i, 'Prior_low_count'] = min(10, (hist.loc[i - 1, 'Prior_low_count'] + 1))
					hist.loc[i, 'FPSAR'] = hist.loc[i - 1, 'FPSAR'] - 0.02 * hist.loc[i, 'Prior_low_count'] * (hist.loc[i - 1, 'FPSAR'] - hist.loc[i, 'Prior_low'])
					if hist.loc[i, 'FPSAR'] < hist.loc[i, 'Close']:
						set_RPSAR(hist, i)
				else:
					set_low(hist, i)
					hist.loc[i, 'Prior_low'] = hist.loc[i - 1, 'Prior_low']
					hist.loc[i, 'Prior_low_count'] = hist.loc[i - 1, 'Prior_low_count']
					hist.loc[i, 'FPSAR'] = hist.loc[i - 1, 'FPSAR'] - 0.02 * hist.loc[i, 'Prior_low_count'] * (hist.loc[i - 1, 'FPSAR'] - hist.loc[i, 'Prior_low'])
					if hist.loc[i, 'FPSAR'] < hist.loc[i, 'Close']:
						set_RPSAR(hist, i)
	hist['PSAR'] = hist[['FPSAR', 'RPSAR']].max(axis = 1)

def	set_FPSAR(hist, i):
	hist.loc[i, 'RPSAR'] = 0
	hist.loc[i, 'Prior_high'] = 0
	hist.loc[i, 'Prior_high_count'] = 0
	max_high = 0
	prior_low = 999999999
	for high in range(6):
		if hist.loc[i + high - 5, 'High'] > max_high:
			max_high = hist.loc[i+high - 5, 'High']
	for low in range(6):
		if hist.loc[i + low - 5, 'Low'] < prior_low:
			prior_low = hist.loc[i + low - 5, 'Low']
	hist.loc[i, 'FPSAR'] = max_high
	hist.loc[i, 'Prior_low'] = prior_low
	hist.loc[i, 'Prior_low_count'] = 1

def	set_RPSAR(hist, i):
	hist.loc[i, 'FPSAR'] = 0
	hist.loc[i, 'Prior_low'] = 0
	hist.loc[i, 'Prior_low_count'] = 0
	max_low = 99999999
	prior_high = 0
	for low in range(6):
		if hist.loc[i + low - 5, 'Low'] < max_low:
			max_low = hist.loc[i + low - 5, 'Low']
	for high in range(6):
		if hist.loc[i + high - 5, 'High'] > prior_high:
			prior_high = hist.loc[i + low - 5, 'High']
	hist.loc[i, 'RPSAR'] = max_low
	hist.loc[i, 'Prior_high'] = prior_high
	hist.loc[i, 'Prior_high_count'] = 1

def	set_high(hist, i):
	hist.loc[i, 'Prior_low'] = 0
	hist.loc[i, 'Prior_low_count'] = 0
	hist.loc[i, 'FPSAR'] = 0

def	set_low(hist, i):
	hist.loc[i, 'Prior_high'] = 0
	hist.loc[i, 'Prior_high_count'] = 0
	hist.loc[i, 'RPSAR'] = 0
