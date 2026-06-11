import pandas as pd

returns = pd.read_csv("data/clean/master_returns.csv")

if "Date" in returns.columns:
    returns = returns.drop(columns=["Date"])

portfolio_returns = returns.mean(axis=1)

summary = pd.DataFrame({
    "Metric": [
        "Average Return",
        "Maximum Return",
        "Minimum Return",
        "Volatility"
    ],
    "Value": [
        portfolio_returns.mean(),
        portfolio_returns.max(),
        portfolio_returns.min(),
        portfolio_returns.std()
    ]
})

summary.to_csv(
    "output/portfolio_summary.csv",
    index=False
)

print("Portfolio summary exported")