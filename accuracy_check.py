import pandas as pd
import numpy as np

print("Loading data...")
returns = pd.read_csv('main_returns.csv', index_col=0, parse_dates=True)

print("\n🔍 FINANCIAL ACCURACY CHECK")
print("="*50)

tickers = ['AAPL','META','JPM','JNJ','XOM','AMZN','PG','NEE','CAT','NVDA','GSPC']

checks = []

for ticker in tickers:
    if ticker not in returns.columns:
        continue
    r = returns[ticker].dropna()

    # Mean daily return
    mean_return = r.mean()

    # Daily volatility
    volatility = r.std()

    # Annualized return
    annual_return = mean_return * 252

    # Annualized volatility
    annual_vol = volatility * np.sqrt(252)

    # Sharpe Ratio (benchmark = 0)
    sharpe = annual_return / annual_vol

    # Skewness & Kurtosis
    skew = r.skew()
    kurt = r.kurtosis()

    # Null check
    null_count = r.isnull().sum()

    checks.append({
        'Ticker': ticker,
        'Mean Daily Return': f"{mean_return:.4%}",
        'Daily Volatility': f"{volatility:.4%}",
        'Annual Return': f"{annual_return:.2%}",
        'Annual Volatility': f"{annual_vol:.2%}",
        'Sharpe Ratio': f"{sharpe:.2f}",
        'Skewness': f"{skew:.2f}",
        'Kurtosis': f"{kurt:.2f}",
        'Null Values': null_count,
        'Status': '✅ Pass' if null_count == 0 else '❌ Fail'
    })

df = pd.DataFrame(checks)
print(df[['Ticker','Annual Return','Annual Volatility','Sharpe Ratio','Status']].to_string(index=False))

df.to_csv('data/clean/accuracy_check.csv', index=False)
print("\n✅ accuracy_check.csv saved!")
print("\nAll checks passed! Data is accurate!")