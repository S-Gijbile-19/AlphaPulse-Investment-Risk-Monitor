import pandas as pd

print("Correlation analysis module initialized")

def correlation_matrix(returns):
    return returns.corr()