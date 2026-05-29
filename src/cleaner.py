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
    prices_path = os.path.join(CLEAN_FOLDER, "main_prices.csv")
    master.to_csv(prices_path)

    # Export log returns
    returns_path = os.path.join(CLEAN_FOLDER, "main_returns.csv")
    log_returns.to_csv(returns_path)


def plot_returns_sanity(log_returns):

    fig, axes = plt.subplots(1, 2, figsize=(16, 5))
    fig.patch.set_facecolor("#FAFAFA")

    ax1 = axes[0]
    ax1.set_facecolor("#FAFAFA")
    cum_returns = log_returns.cumsum()
    for col in cum_returns.columns:
        lw = 2 if col == "SP500" else 1.2
        ls = "--" if col == "SP500" else "-"
        ax1.plot(cum_returns.index, cum_returns[col], label=col,
                 linewidth=lw, linestyle=ls)
    ax1.set_title("Cumulative Log Returns (2019–2024)", fontsize=12, fontweight="bold")
    ax1.set_xlabel("Date")
    ax1.set_ylabel("Cumulative Log Return")
    ax1.legend(fontsize=8, ncol=2)
    ax1.grid(True, alpha=0.3, linestyle="--")

    # Right: Correlation matrix heatmap (preview for Week 2)
    ax2 = axes[1]
    corr = log_returns.corr()
    im   = ax2.imshow(corr.values, cmap="RdYlGn", vmin=-1, vmax=1)
    ax2.set_xticks(range(len(corr.columns)))
    ax2.set_yticks(range(len(corr.columns)))
    ax2.set_xticklabels(corr.columns, rotation=45, ha="right", fontsize=8)
    ax2.set_yticklabels(corr.columns, fontsize=8)
    plt.colorbar(im, ax=ax2, shrink=0.8)
    # Annotate cells
    for i in range(len(corr)):
        for j in range(len(corr.columns)):
            ax2.text(j, i, f"{corr.values[i,j]:.2f}",
                     ha="center", va="center", fontsize=7,
                     color="black" if abs(corr.values[i,j]) < 0.7 else "white")
    ax2.set_title("Correlation Matrix — Preview for Week 2", fontsize=12, fontweight="bold")

    plt.tight_layout()
    path = os.path.join(CLEAN_FOLDER, "sanity_check.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()



if __name__ == "__main__":
    master      = build_master_prices()
    master      = remove_duplicates(master)
    master      = integrity_checks(master)
    log_returns = compute_log_returns(master)
    export_clean(master, log_returns)
    plot_returns_sanity(log_returns)
