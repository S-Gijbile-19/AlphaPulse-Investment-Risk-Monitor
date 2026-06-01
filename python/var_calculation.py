import pandas as pd
import numpy as np


returns = pd.read_csv("../main_returns.csv")


portfolio_returns = returns.drop(columns=["Date"])

portfolio_returns = portfolio_returns.mean(axis=1)

var_95 = np.percentile(portfolio_returns, 5)

print("Portfolio VaR (95%):", var_95)