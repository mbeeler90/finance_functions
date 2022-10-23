import plotly.express as px
import pandas as pd

def create_chart(hist, indicator, include_indicator):
	displayed_lines = ['Price']
	df = pd.DataFrame([])
	df['Date'] = hist['Date']
	df['Price'] = hist['Close']
	if include_indicator:
		df[indicator] = hist[indicator]
		displayed_lines.append(indicator)
	
	fig = px.line(
		df,
		x='Date',
		y=displayed_lines,
		title='',
		labels={
			'Date': '',
			'value': ''
		},
	)

	fig.update_layout(
		showlegend=False,
		margin=dict(l=50, r=50, t=0, b=0)
	)

	if include_indicator == False:
		fig.update_layout(
			xaxis = {
				'visible': False
			}
		)

	return fig

def create_indicator_chart(hist, indicator):
	df = pd.DataFrame([])
	df['Date'] = hist['Date']
	df[indicator] = hist[indicator]

	fig = px.line(
		df,
		x='Date',
		y=indicator,
		title='',
		labels={
			'Date': '',
			indicator: ''
		},
	)

	fig.update_layout(
		showlegend=False,
		margin=dict(l=50, r=50, t=10, b=0),
		height=250
	)	

	return fig
