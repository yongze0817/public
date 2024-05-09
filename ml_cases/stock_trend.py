# Retrieve historical closing price data for NVIDIA Corporation (NVDA) from Yahoo Finance for the past 5 years.
import pandas as pd
import yfinance as yf
from datetime import datetime, timedelta

# Define the ticker symbol
tickerSymbol = 'NVDA'

# Get data on this ticker
tickerData = yf.Ticker(tickerSymbol)

# Define the end date as today
end_date = datetime.today().strftime('%Y-%m-%d')

# Define the start date as 5 years from the end date
start_date = (datetime.today() - timedelta(days=5*365)).strftime('%Y-%m-%d')

# Get the historical prices for this ticker
nvda_data = tickerData.history(period='1d', start=start_date, end=end_date)

# Only keep the closing prices
nvda_closing_prices = nvda_data['Close'].copy()

# Display the first few rows of the closing prices
nvda_closing_prices.head()

import numpy as np

# Calculate summary statistics for the closing prices
descriptive_stats = nvda_closing_prices.describe()

# Calculate additional statistics
variance = np.var(nvda_closing_prices)
skewness = nvda_closing_prices.skew()
kurtosis = nvda_closing_prices.kurt()

# Display the summary statistics
descriptive_stats['variance'] = variance
descriptive_stats['skewness'] = skewness
descriptive_stats['kurtosis'] = kurtosis
descriptive_stats
