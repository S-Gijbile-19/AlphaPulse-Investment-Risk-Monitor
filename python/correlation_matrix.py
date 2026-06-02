import pandas as pd

# Load returns data
returns = pd.read_csv("main_returns.csv")

# Remove Date column if present
if "Date" in returns.columns:
    returns = returns.drop(columns=["Date"])

# Calculate correlation matrix
correlation_matrix = returns.corr()

# Save output
correlation_matrix.to_csv("outputs/correlation_matrix.csv")

print("Correlation matrix saved successfully.")