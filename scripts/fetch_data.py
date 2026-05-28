import yfinance as yf
import pandas as pd

stocks = ['AAPL', 'MSFT', 'TSLA']

for stock in stocks:
    data = yf.download(stock, start="2023-01-01", end="2024-12-31")
    
    data.to_csv(f"data/{stock}.csv")
    
    print(f"{stock} data saved!")