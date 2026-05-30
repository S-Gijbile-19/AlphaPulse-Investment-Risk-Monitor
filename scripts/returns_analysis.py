import pandas as pd
import numpy as np
import os

RAW_DATA_FOLDER = "data/raw"

print("Returns analysis module initialized")

# Load one stock file
file_path = os.path.join(RAW_DATA_FOLDER, "AAPL.csv")

data = pd.read_csv(file_path)

# Calculate daily log returns
data["Daily_Return"] = np.log(data["Close"] / data["Close"].shift(1))

print(data[["Date", "Close", "Daily_Return"]].head())