import pandas as pd
import numpy as np
import os

RAW_DATA_FOLDER = "data/raw"

# Load stock data
file_path = os.path.join(RAW_DATA_FOLDER, "AAPL.csv")

data = pd.read_csv(file_path)

data.rename(columns={"Price": "Date"}, inplace=True)

data["Date"] = pd.to_datetime(data["Date"])

data["Daily_Return"] = np.log(
    data["Close"] / data["Close"].shift(1)
)

data["Rolling_Volatility"] = (
    data["Daily_Return"]
    .rolling(window=30)
    .std()
)

print(
    data[
        ["Date",
         "Daily_Return",
         "Rolling_Volatility"]
    ].tail()
)