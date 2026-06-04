import pandas as pd
import numpy as np

print("Loading data...")
returns = pd.read_csv('data/clean/master_returns.csv', index_col=0, parse_dates=True)

tickers = ['AAPL','META','JPM','JNJ','XOM','AMZN','PG','NEE','CAT','NVDA','GSPC']

print("\n📊 EXECUTIVE SUMMARY")
print("="*50)

summary = []

for ticker in tickers:
    if ticker not in returns.columns:
        continue
    r = returns[ticker].dropna()

    # VaR (95% confidence)
    var_95 = np.percentile(r, 5)

    # Max Drawdown
    prices = (1 + r).cumprod()
    rolling_max = prices.cummax()
    drawdown = (prices - rolling_max) / rolling_max
    max_drawdown = drawdown.min()

    summary.append({
        'Ticker': ticker,
        'Current VaR (95%)': f"{var_95:.2%}",
        'Max Drawdown': f"{max_drawdown:.2%}"
    })

df = pd.DataFrame(summary)
print(df.to_string(index=False))

df.to_csv('data/clean/executive_summary.csv', index=False)
print("\n✅ executive_summary.csv saved!")
print("Executive Summary Complete!")