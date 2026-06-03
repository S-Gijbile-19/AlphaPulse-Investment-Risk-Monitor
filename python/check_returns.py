import pandas as pd

df = pd.read_csv("data/clean/main_returns.csv")

print(df.head())
print()
print(df.describe())