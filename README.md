# Stock market monitoring webpage

## Description
This project creates a webpage in Dash (python / plotly) to follow the development of stocks and technical indicators. For every stock, data can be displayed for either:
- 1 year;
- year-to-date;
- 1 month; or
- month-to-date.

## Usage
Run `python main.py` to start a local server to access the webpage. Select the stock, indicator and time period you are interested in.

![Example for Apple stock and simple moving average](./assets/example.png)

## Requirements
The following python modules are required to run the program. Install the modules with `pip install [module]` or `conda install [module]`:
- `dash`
- `dash_bootstrap_components`
- `dash_loading_spinners`
- `yfinance`
