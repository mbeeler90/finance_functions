import dash
import dash_bootstrap_components as dbc
from dash import dcc, html, callback
from dash.dependencies import Input, Output, State
import dash_loading_spinners as dls
import yfinance as yf
import pandas as pd
import json
from datetime import datetime

import srcs.download_data as download
import srcs.indicators as indi
import srcs.get_chart as get_chart

external_stylesheets = [dbc.themes.FLATLY]

# defining header data of the webpage
app = dash.Dash(__name__,
	external_stylesheets = external_stylesheets,
	meta_tags=[
		{
			'name':'viewport',
			'content':'width=device-width, initial-scale=1.0, maximum-scale=1.2, minimum-scale=0.5'
		},
		{
			'name':'descripiton',
			'content':'Stock monitoring'
		}
	],
	title = 'Stock monitoring tool',
	update_title = 'Updating data..'
)

server = app.server

# layout of the page
app.layout = dbc.Container([
	# container for viewport
	html.Div([
		dcc.Location(id = 'url'),
		html.Div(id = 'viewport-container')
	]),

	# title
	dbc.Row([
		dbc.Col(html.H1('Stock monitoring tool'), className = 'title')
	]),

	# introduction text
	dbc.Row(
		dbc.Col(html.P(
			"""
			The stock markets are going crazy nowadays. To not miss any important 
			developments, it's important to stay up to date with what's going on. 
			This tools lets you track some of the most popular stocks and their key indicators.
			To use the tool, just select the stock and indicator you are interested in 
			and don't miss out on any trend ever again!
			"""
		), xs = 10)
	, justify = 'center'),

	# selection of stock and indicator
	html.Div([dbc.Row([

		# stocks
		dbc.Col(
			html.Div([
				dbc.Row([
					dbc.Col(html.H4('Stock'))
				]),
				dbc.Row([
					dbc.Col(dcc.Dropdown([], value = 'AAPL', clearable = False, id = 'stocks'))
				]),
				dbc.Row([html.Br()])
			]),
		xs = 10, sm = 8, md = 4, lg = 3, xl = 3),

		# indicator
		dbc.Col(
			html.Div([
				dbc.Row([
					dbc.Col(html.H4('Indicator'))
				]),
				dbc.Row([
					dbc.Col(dcc.Dropdown([], value = '3 / 10 day Chaikin indicator', clearable = False, id = 'indicators'))
				])
			]),
		xs = 10, sm = 8, md = 4, lg = 3, xl = 3),

		# run buttom
		dbc.Col(
			html.Button('Show', n_clicks = 0, id = 'show-stock'),
		xs = 10, sm = 8, md = 2, lg = 3, xl = 3)
	], justify = 'center')]),

	# error message
	dbc.Row([
		dbc.Col(
			dbc.Alert(
					"Data cannot be loaded, try another stock or try later again!",
					id = "alert",
					duration = 3000,
					is_open = False,
					color = 'warning'
				)
			, xs = 10, sm = 8, md = 8, lg = 6, xl = 6),
	], justify = 'center'),

	# dashboard section
	# loading bars
	dls.Bars([
		html.Div([

			# dashboard title
			dbc.Row([
				dbc.Col(html.H2('', id = 'stock-title', className = 'stock-title'))
			], justify = 'center'),

			# field to select period that should be displayed in chart
			dbc.Row([
				dbc.Col(
					dcc.Dropdown(
						['1 year', 'YTD', '1 month', 'MTD'],
						value = '1 year',
						clearable = False,
						id = 'time-period',
						className = 'time-period'
					),
				xs = 10, sm = 10, md = 4, lg = 2, xl = 2)
			]),

			# chart and company information
			dbc.Row([

				# chart section
				dbc.Col(
					html.Div([

						# chart with stock information
						dbc.Row([
							dbc.Col(
								html.Div([
									dcc.Graph(id = 'stock-price')
								])
							)
						], justify = 'center'),

						# chart only for indicators
						dbc.Row([
							dbc.Col(
								html.Div([
									dcc.Graph(id = 'indicator-chart')
								], id = 'show-indicator')
							)
						], justify = 'center')
					]),
				xs = 12, sm = 12, md = 12, lg = 8, xl = 8),
				
				# company information section
				dbc.Col(
					html.Div([
						dbc.Row([

							# company name
							dbc.Col(
								html.Div([
									html.P('Company name', className = 'info-head'),
									html.P('', id = 'company-name', className = 'info-content')
								]),
							xs = 6, sm = 6, md = 4, lg = 6, xl = 6),

							# company industry
							dbc.Col(
								html.Div([
									html.P('Industry', className = 'info-head'),
									html.P('', id = 'industry', className = 'info-content')
								]),
							xs = 6, sm = 6, md = 4, lg = 6, xl = 6),

							# last closing price of the stock
							dbc.Col(
								html.Div([
									html.P('Price', className = 'info-head'),
									html.P('', id = 'price', className = 'info-content-num')
								]),
							xs = 6, sm = 6, md = 4, lg = 6, xl = 6),

							# return for last 12 month period
							dbc.Col(
								html.Div([
									html.P('Return (12 months)', className = 'info-head'),
									html.P('', id = 'return', className = 'info-content-num')
								]),
							xs = 6, sm = 6, md = 4, lg = 6, xl = 6),

							# forward EPS
							dbc.Col(
								html.Div([
									html.P('Forward EPS', className = 'info-head'),
									html.P('', id = 'forward-eps', className = 'info-content-num')
								]),
							xs = 6, sm = 6, md = 4, lg = 6, xl = 6),

							# forward PE ratio
							dbc.Col(
								html.Div([
									html.P('Forward P/E', className = 'info-head'),
									html.P('', id = 'forward-pe', className = 'info-content-num')
								]),
							xs = 6, sm = 6, md = 4, lg = 6, xl = 6),

							# news section
							dbc.Col(
								html.Div([
									html.P('Latest News', className = 'info-head'),
									html.Div([], id = 'news-feed', className = 'news-content'),
								]),
							xs = 12)
						]),
					]),
				xs = 12, sm = 12, md = 10, lg = 4, xl = 4),
			], justify = 'center')
		], id = 'show-dashboard')
	])
])

# callback functions

# function to get the screen size on page load
app.clientside_callback(
	"""
	function(href) {
		var w = window.innerWidth;
		var h = window.innerHeight;
		return {'height': h, 'width': w};
	}
	""",
	Output('viewport-container', 'children'),
	Input('url', 'href')
)

# function to set the list of stocks that can be selected at page load
app.clientside_callback(
	"""
	function(href) {
		return ['AAPL', 'ABNB', 'AMD', 'AMZN', 'BA', 'CSCO', 'DIS', 'DKNG', 'GM', 'GOOGL', 'IBM', 'INT', 'JNJ', 'KO', 'META', 'MSFT', 'NKE', 'VZ', 'WMT'];
	}
	""",
	Output('stocks', 'options'),
	Input('url', 'refresh')
)

# function to set the list of inidcators that can be selected at page load
app.clientside_callback(
	"""
	function(href) {
		return ['3 / 10 day Chaikin indicator', '12 / 26 day MACD', '14 day ADX', '14 day RSI', '14 day stochastic oscillator', '21 day Bollinger bands', '21 day DEMA', '21 day EMA', '21 day LWMA', '21 day simple MA', '25 day Aroon indicator', 'Fibonacci levels', 'Parabolic SAR'];
	}
	""",
	Output('indicators', 'options'),
	Input('url', 'refresh')
)

# download and set data to be displayed for stock / indicator
@callback(
	Output('stock-price', 'figure'),
	Output('show-dashboard', 'style'),
	Output('indicator-chart', 'figure'),
	Output('show-indicator', 'style'),
	Output('stock-title', 'children'),
	Output('company-name', 'children'),
	Output('industry', 'children'),
	Output('price', 'children'),
	Output('return', 'children'),
	Output('forward-eps', 'children'),
	Output('forward-pe', 'children'),
	Output('news-feed', 'children'),
	Output('alert', 'is_open'),
	Input('show-stock', 'n_clicks'),
	Input('time-period', 'value'),
	State('stocks', 'value'),
	State('indicators', 'value'),
	State('viewport-container', 'children'),
	prevent_initial_call = True
	)
def show_data(n_clicks, time_period, ticker, indicator, size):
	width = size['width']
	display_dashboard = {'display': 'none'}
	display_indicator = {'display': 'none'}

	# indicators that are displayed in a separate chart
	show_indicator_chart = [
		'3 / 10 day Chaikin indicator',
		'12 / 26 day MACD',
		'14 day ADX',
		'14 day RSI',
		'14 day stochastic oscillator',
		'25 day Aroon indicator'
	]

	# ddownload ticker data
	stock = yf.Ticker(ticker)
	hist, stock_info = download.download_data(ticker, stock)
	if hist.empty:
		return dash.no_update, display_dashboard, dash.no_update, display_indicator, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, dash.no_update, True

	# calculate indicator
	indi.add_indicator(hist, ticker, indicator)

	# set date for period that shall be displayed
	now = datetime.now()
	year = now.strftime('%Y')
	month = now.strftime('%m')
	if time_period == '1 year':
		period = hist.loc[0, 'Date']
	elif time_period == 'YTD':
		period = year + '-01-01'
	elif time_period == '1 month':
		period = hist.loc[max(hist.index) - 22, 'Date']
	else:
		period = year + '-' + month + '-01'

	# if indicator is displayed in separate chart, create two charts, ohterwise one
	if indicator in show_indicator_chart:
		chart = get_chart.create_chart(hist, indicator, False, period, width)
		indicator_chart = get_chart.create_indicator_chart(hist, indicator, period, width)
		display_indicator = {'display': 'block'}
	else:
		chart = get_chart.create_chart(hist, indicator, True, period, width)
		indicator_chart = dash.no_update
	news_feed = get_chart.news_feed(stock_info['news'])

	# set margin based on the screen size of the user.
	if width < 992:
		display_dashboard = {'display': 'block', 'margin-right': '0px'}
	else:
		display_dashboard = {'display': 'block', 'margin-right': '75px'}

	return chart, display_dashboard, indicator_chart, display_indicator, ticker, stock_info['name'], stock_info['industry'], stock_info['price'], str(stock_info['return'])+'%', stock_info['forwardEPS'], stock_info['forwardPE'], news_feed, False

if __name__ == '__main__': 
	app.run_server()
