import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from dash import html

def create_chart(hist, indicator, include_indicator, date):
	displayed_lines = ['Close']
	hist['Date'] = pd.to_datetime(hist['Date'], format='%Y-%m-%d')
	df = hist.loc[(hist['Date'] >= date)]

	if include_indicator and not indicator == 'Fibonacci levels' and not indicator == 'Parabolic SAR':
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

	if (indicator == 'Fibonacci levels'):	
		min_fib = min(df['Price'])
		max_fib = max(df['Price'])
		fig.add_hline(y=min_fib)
		fig.add_hline(y=min_fib + (max_fib - min_fib) * 0.236)
		fig.add_hline(y=min_fib + (max_fib - min_fib) * 0.382)
		fig.add_hline(y=min_fib + (max_fib - min_fib) * 0.5)
		fig.add_hline(y=min_fib + (max_fib - min_fib) * 0.618)
		fig.add_hline(y=min_fib + (max_fib - min_fib) * 0.764)
		fig.add_hline(y=max_fib)

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

	if indicator == '21 day Bollinger bands':
		fig2 = go.Figure()
		fig2.add_traces(go.Scatter(x=df['Date'], y = df[indicator+'_low'],
			line = dict(color='black')))

		fig2.add_traces(go.Scatter(x=df['Date'], y = df[indicator+'_high'],
			line = dict(color='black'),
			fill='tonexty', 
			fillcolor = 'yellow'))
		
		fig2.add_traces(data=fig.data)
		fig = fig2

	if indicator == 'Parabolic SAR':
		fig2 = px.scatter(x=df['Date'], y=df['PSAR'])
		fig = go.Figure(data=fig.data+fig2.data)

	return fig

def create_indicator_chart(hist, indicator, date):
	hist['Date'] = pd.to_datetime(hist['Date'], format='%Y-%m-%d')
	df = hist.loc[(hist['Date'] >= date)]

	indicator_list = [indicator]
	if indicator == '12 / 26 day MACD':
		indicator_list.append(indicator+' moving average')
	if indicator == '25 day Aroon indicator':
		indicator_list = [indicator+' up', indicator+' down']
	if indicator == '14 day stochastic oscillator':
		indicator_list.append(indicator+' moving average')
	fig = px.line(
		df,
		x='Date',
		y=indicator_list,
		title='',
		labels={
			'Date': '',
			'value': ''
		},
	)

	fig.update_layout(
		showlegend=False,
		margin=dict(l=50, r=50, t=10, b=0),
		height=250
	)	

	return fig

def news_feed(news):
	if len(news) > 5:
		num_news = 5
	else:
		num_news = len(news)
	news_list = []
	for i in range(num_news):
		news_item = html.Li(
			html.P([
				news[i]['title'],
				' (',
				html.I(news[i]['publisher']),
				') \U0001F449 ',
				html.A('read more', href=news[i]['link'], target='_blank')
			], className='news-list')
		)
		news_list.append(news_item)
	news_feed = html.Div([
		html.Ul(news_list)
	])
	return news_feed
