import pandas as pd
import numpy as np
import os

from scipy.stats import skew, kurtosis

os.makedirs("output", exist_ok=True)

returns = pd.read_csv("data/clean/main_returns.csv")

if "Date" in returns.columns:
    returns = returns.drop(columns=["Date"])

portfolio_returns = returns.mean(axis=1)

mean_return = portfolio_returns.mean()
volatility = portfolio_returns.std()

num_simulations = 10000
forecast_days = 30

simulation_results = []

for _ in range(num_simulations):

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


# Distribution validation

simulation_skewness = skew(simulation_results)
simulation_kurtosis = kurtosis(simulation_results)

print("\nDistribution Validation")
print("Skewness:", round(simulation_skewness, 4))
print("Kurtosis:", round(simulation_kurtosis, 4))

simulation_df = pd.DataFrame({
    "Future_Portfolio_Value": simulation_results
})

simulation_df.to_csv(
    "output/monte_carlo_results.csv",
    index=False
)


validation_df = pd.DataFrame({
    "Metric": ["Skewness", "Kurtosis"],
    "Value": [
        simulation_skewness,
        simulation_kurtosis
    ]
})

validation_df.to_csv(
    "output/validation_report.csv",
    index=False
)

print("Results exported successfully")