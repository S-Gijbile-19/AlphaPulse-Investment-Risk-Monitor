import pandas as pd

print("Rolling volatility module initialized")

def rolling_volatility(returns):
    return returns.rolling(window=30).std()