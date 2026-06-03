import pandas as pd
import matplotlib.pyplot as plt

# Load simulation results
df = pd.read_csv("output/monte_carlo_results.csv")

plt.figure(figsize=(8,5))
plt.hist(df["Future_Portfolio_Value"], bins=50)

plt.title("Monte Carlo Portfolio Distribution")
plt.xlabel("Future Portfolio Value")
plt.ylabel("Frequency")

plt.savefig(
    "output/monte_carlo_distribution.png"
)

plt.show()

print("Distribution chart saved successfully")