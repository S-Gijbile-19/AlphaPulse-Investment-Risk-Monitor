import pandas as pd

# Load returns data
returns = pd.read_csv("main_returns.csv")

# Remove Date column
returns = returns.drop(columns=["Date"])

# Calculate 30-day rolling volatility
rolling_volatility = returns.rolling(window=30).std()

rolling_volatility.to_csv("output/rolling_volatility.csv", index=False)

print(rolling_volatility.tail())

print("Rolling volatility exported successfully")
