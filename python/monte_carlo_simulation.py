import pandas as pd
import numpy as np

returns = pd.read_csv("main_returns.csv")

returns = returns.drop(columns=["Date"])

portfolio_returns = returns.mean(axis=1)

mean_return = portfolio_returns.mean()
volatility = portfolio_returns.std()

num_simulations = 1000

forecast_days = 30

simulation_results = []

for i in range(num_simulations):

    simulated_returns = np.random.normal(
        mean_return,
        volatility,
        forecast_days
    )

    future_value = (1 + simulated_returns).prod()

    simulation_results.append(future_value)

print("Monte Carlo Simulation Complete")
print("Number of Simulations:", num_simulations)
print("Average Future Portfolio Value:", np.mean(simulation_results))