import pandas as pd
import os


returns = pd.read_csv("main_returns.csv")


if "Date" in returns.columns:
    returns = returns.drop(columns=["Date"])

returns = returns.apply(pd.to_numeric, errors="coerce")
returns = returns.fillna(0)


if returns.empty:
    raise ValueError("Dataset is empty")

if len(returns) < 30:
    raise ValueError("Not enough data for 30-day volatility")


rolling_volatility = returns.rolling(window=30, min_periods=1).std()


base_dir = os.path.dirname(os.path.abspath(__file__))
output_dir = os.path.join(base_dir, "..", "outputs")
os.makedirs(output_dir, exist_ok=True)

output_path = os.path.join(output_dir, "rolling_volatility.csv")
rolling_volatility.to_csv(output_path, index=False)


print(rolling_volatility.tail())
print(f"Saved at: {output_path}")