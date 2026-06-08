import pandas as pd
import os

# Create output folder
os.makedirs("output", exist_ok=True)

returns = pd.read_csv("main_returns.csv")

if "Date" in returns.columns:
    returns = returns.drop(columns=["Date"])

corr_matrix = returns.corr()

print(corr_matrix)

# Save correlation matrix
corr_matrix.to_csv(
    "output/correlation_matrix.csv"
)

print("Correlation matrix exported successfully")