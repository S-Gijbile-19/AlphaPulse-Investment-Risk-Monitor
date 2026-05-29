import os
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.ticker as mticker

TICKERS = [
    "AAPL", "META", "JPM", "JNJ", "XOM",
    "AMZN", "PG",   "NEE", "CAT", "NVDA"
]
BENCHMARK  = "GSPC"
RAW_FOLDER = "data/raw"

COLOURS = {
    "AAPL": "#2196F3",  # blue
    "META": "#FF9800",  # orange
    "JPM" : "#9C27B0",  # purple
    "JNJ" : "#F44336",  # red
    "XOM" : "#795548",  # brown
    "AMZN": "#FF5722",  # deep orange
    "PG"  : "#E91E63",  # pink
    "NEE" : "#8BC34A",  # light green
    "CAT" : "#FFC107",  # amber
    "NVDA": "#00BCD4",  # cyan
    "GSPC": "#212121",  # black
}

def load_csv(ticker):
    filepath = os.path.join(RAW_FOLDER, f"{ticker}.csv")
    df = pd.read_csv(filepath, index_col=0, parse_dates=True)
    if isinstance(df.columns, pd.MultiIndex):
        df.columns = ['_'.join(col).strip() for col in df.columns.values]
    for col in df.columns:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    return df

# Raw Close Prices
def plot_raw(all_data):
    tickers_only = {k: v for k, v in all_data.items() if k != "GSPC"}

    fig, axes = plt.subplots(5, 2, figsize=(16, 18))
    fig.patch.set_facecolor("#FAFAFA")
    fig.suptitle("AlphaPulse — Raw Adjusted Close Prices (2019–2024)",
                 fontsize=14, fontweight="bold", y=1.01)

    axes_flat = axes.flatten()
    for i, (ticker, df) in enumerate(tickers_only.items()):
        ax = axes_flat[i]
        ax.set_facecolor("#FAFAFA")
        ax.plot(df.index, df["Close"].dropna(),
                color=COLOURS[ticker], linewidth=1.2)
        ax.set_title(ticker, fontsize=11, fontweight="bold",
                     color=COLOURS[ticker])
        ax.set_xlabel("")
        ax.set_ylabel("Price (USD)", fontsize=8)
        ax.grid(True, alpha=0.3, linestyle="--")
        ax.tick_params(axis='x', rotation=30, labelsize=7)
        ax.yaxis.set_major_formatter(
            mticker.FuncFormatter(lambda x, _: f"${x:.0f}"))

    plt.tight_layout()
    path = os.path.join(RAW_FOLDER, "plot_raw_prices.png")
    plt.savefig(path, dpi=150, bbox_inches="tight")
    plt.close()
    
def plot_prices(cleaned_data):
    fig, ax = plt.subplots(figsize=(14, 6))
    for ticker, df in cleaned_data.items():
        if "Close" not in df.columns:
            continue
        series     = df["Close"].dropna()
        normalised = (series / series.iloc[0]) * 100
        label = "S&P 500" if ticker == "GSPC" else ticker
        lw    = 2.5 if ticker == "GSPC" else 1.2
        ls    = "--" if ticker == "GSPC" else "-"
        ax.plot(normalised.index, normalised.values, label=label, linewidth=lw, linestyle=ls)

    ax.set_title("AlphaPulse — Normalised Adjusted Close Prices (Base = 100)", fontsize=13)
    ax.set_xlabel("Date")
    ax.set_ylabel("Normalised Price (Base 100)")
    ax.legend(loc="upper left", fontsize=8, ncol=2)
    ax.grid(True, alpha=0.3)
    plt.tight_layout()

    chart_path = os.path.join(RAW_FOLDER, "price_chart.png")
    plt.savefig(chart_path, dpi=150)
    plt.close()

if __name__ == "__main__":

    all_data = {}
    for ticker in TICKERS + [BENCHMARK]:
        all_data[ticker] = load_csv(ticker)
        print(f"  Loaded {ticker}")

    plot_raw(all_data)     
    plot_prices(all_data)     

