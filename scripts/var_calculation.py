import pandas as pd
import numpy as np

# Load returns
returns = pd.read_csv("data\clean\main_returns.csv")

if "Date" in returns.columns:
    returns = returns.drop(columns=["Date"])

# Portfolio return
portfolio_returns = returns.mean(axis=1)

# Confidence Level
confidence_level = 95

# Historical VaR
var_95 = np.percentile(portfolio_returns, 100 - confidence_level)

print(f"{confidence_level}% Historical VaR: {var_95:.4f}")

# Save result
var_df = pd.DataFrame({
    "Confidence_Level": [confidence_level],
    "VaR": [var_95]
})

var_df.to_csv(
    "output/var_report.csv",
    index=False
)

print("VaR report exported successfully")