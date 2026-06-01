import pandas as pd

returns = pd.read_csv("../main_returns.csv")

returns = returns.drop(columns=["Date"])

corr_matrix = returns.corr()

print(corr_matrix)