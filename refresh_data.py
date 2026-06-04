import yfinance as yf
import pandas as pd
import numpy as np
from datetime import datetime

tickers = ['AAPL','META','JPM','JNJ','XOM','AMZN','PG','NEE','CAT','NVDA','^GSPC']

print("Downloading latest stock data...")
data = yf.download(tickers, start='2019-01-02', 
                   end=datetime.today().strftime('%Y-%m-%d'))['Close']

data.columns = [c.replace('^','') for c in data.columns]

# Save prices
data.to_csv('data/clean/master_prices.csv')
print("master_prices.csv updated!")

# Calculate log returns
log_returns = np.log(data/data.shift(1)).dropna()
log_returns.to_csv('data/clean/master_returns.csv')
print("master_returns.csv updated!")

print(f"Data refreshed! Total rows: {len(data)}")
print("Refresh complete!")