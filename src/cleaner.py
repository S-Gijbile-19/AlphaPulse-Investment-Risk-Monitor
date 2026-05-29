import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

TICKERS = [
    "AAPL", "META", "JPM", "JNJ", "XOM",
    "AMZN", "PG",   "NEE", "CAT", "NVDA"
]
BENCHMARK  = "GSPC"
RAW_FOLDER   = "data/raw"
CLEAN_FOLDER = "data/clean"

def load_csv(ticker):
    filepath = os.path.join(RAW_FOLDER, f"{ticker}.csv")
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    df.index = pd.to_datetime(df.index, errors='coerce')
    df = df[df.index.notna()]
    return df

# Build master prices DataFrame
def build_master_prices():

    price_dict = {}
    all_tickers = TICKERS + [BENCHMARK]

    for ticker in all_tickers:
        df = load_csv(ticker)
        if "Close" not in df.columns:
            print(f"  {ticker}: Close column missing!")
            continue
        label = "SP500" if ticker == "GSPC" else ticker
        price_dict[label] = df["Close"]
        print(f"  Loaded {ticker:6s} — {len(df)} rows")

    # Merge all into one DataFrame (inner join = common dates only)
    master = pd.DataFrame(price_dict)
    master.index.name = "Date"
    master = master.sort_index()
    return master

# Remove duplicate rows 
def remove_duplicates(master):
    dupes = master.index.duplicated().sum()
    if dupes > 0:
        print(f"  Found {dupes} duplicate date(s) — removing...")
        master = master[~master.index.duplicated(keep='first')]
        print(f" Duplicates removed. New shape: {master.shape}")
    else:
        print("No duplicate dates found.")

    return master

# Data integrity checks
def integrity_checks(master):

    all_passed = True

    # Check 1: No negative prices
    neg = (master < 0).sum()
    neg_tickers = neg[neg > 0]
    if not neg_tickers.empty:
        print("Negative prices found: {neg_tickers.to_dict()}")
        all_passed = False
    else:
        print("No negative prices")

    # Check 2: No zero prices
    zeros = (master == 0).sum()
    zero_tickers = zeros[zeros > 0]
    if not zero_tickers.empty:
        print(f"Zero prices found: {zero_tickers.to_dict()}")
        all_passed = False
    else:
        print("No zero prices")

    # Check 3: Null count per ticker
    nulls = master.isnull().sum()
    null_tickers = nulls[nulls > 0]
    if not null_tickers.empty:
        print(f"  Null values found:")
        for t, n in null_tickers.items():
            print(f"     {t}: {n} nulls — forward filling...")
        master = master.ffill().bfill()
        print("Nulls filled.")
    else:
        print("No null values in any column")

    # Check 4: All tickers present
    expected = set(TICKERS + ["SP500"])
    actual   = set(master.columns)
    missing  = expected - actual
    if missing:
        print(f" Missing tickers: {missing}")
        all_passed = False
    else:
        print(f" All {len(actual)} tickers present")

    if all_passed:
        print("\n All integrity checks passed!")

    return master

# Compute daily log returns 
def compute_log_returns(master):
    """
    Log return = ln(Price_today / Price_yesterday)
    This is the standard input for Monte Carlo simulations.
    """
    log_returns = np.log(master / master.shift(1))
    log_returns = log_returns.dropna()   # first row is NaN (no previous price)

    print(f"     Shape : {log_returns.shape}")
    print(f"     Range : {log_returns.index[0].date()} → {log_returns.index[-1].date()}")
    print()

    # Print basic stats for each ticker
    stats = log_returns.describe().T[["mean","std","min","max"]]
    stats.columns = ["Mean Return", "Std Dev", "Min (Worst Day)", "Max (Best Day)"]
    stats = stats * 100  # convert to percentage

    return log_returns


# Export clean data 
def export_clean(master, log_returns):
    os.makedirs(CLEAN_FOLDER, exist_ok=True)

    # Export master prices
    prices_path = os.path.join(CLEAN_FOLDER, "master_prices.csv")
    master.to_csv(prices_path)

    # Export log returns
    returns_path = os.path.join(CLEAN_FOLDER, "master_returns.csv")
    log_returns.to_csv(returns_path)




if __name__ == "__main__":
    master      = build_master_prices()
    master      = remove_duplicates(master)
    master      = integrity_checks(master)
    log_returns = compute_log_returns(master)
    export_clean(master, log_returns)
    # plot_returns_sanity(log_returns)
