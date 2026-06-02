import pandas as pd
import numpy as np

returns = pd.read_csv("main_returns.csv")
returns = returns.drop(columns=["Date"])

portfolio_returns = returns.mean(axis=1)

var_95 = np.percentile(portfolio_returns, 5)

var_df = pd.DataFrame({
    "Confidence_Level": [95],
    "VaR": [var_95]
})

var_df.to_csv("outputs/var_results.csv", index=False)

print("VaR results saved.")