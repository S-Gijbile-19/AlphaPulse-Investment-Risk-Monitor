import pandas as pd

# Load returns data
returns = pd.read_csv("main_returns.csv")

# Remove Date column
returns = returns.drop(columns=["Date"])

# Calculate 30-day rolling volatility
rolling_volatility = returns.rolling(window=30).std()

print(rolling_volatility.tail())
returns = pd.read_csv("main_returns.csv")
returns = returns.drop(columns=["Date"])
returns.rolling(window=30).std()