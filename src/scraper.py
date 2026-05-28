import os
import time
import yfinance as yf
import pandas as pd

# Settings (from config.py)
TICKERS = [
    "AAPL", "META", "JPM", "JNJ", "XOM",
    "AMZN", "PG",   "NEE", "CAT", "NVDA"
]
BENCHMARK  = "^GSPC"
START_DATE = "2019-01-01"
END_DATE   = "2024-12-31"

RAW_DATA_FOLDER = "data/raw"

os.makedirs(RAW_DATA_FOLDER, exist_ok=True)

# Download function with retry logic
def download_ticker(ticker, start, end, retries=3, wait=5):
    """
    Downloads historical OHLCV data for a single ticker.
    Retries up to 3 times if the download fails (e.g. API rate limit).

    Parameters:
        ticker  : stock symbol e.g. "AAPL"
        start   : start date string "YYYY-MM-DD"
        end     : end date string   "YYYY-MM-DD"
        retries : number of retry attempts
        wait    : seconds to wait between retries
    """
    for attempt in range(1, retries + 1):
        try:
            print(f"  Downloading {ticker} attempt {attempt}")

            data = yf.download(
                ticker,
                start=start,
                end=end,
                auto_adjust=True,   # uses Adjusted Close automatically
                progress=False      # suppresses yfinance's own progress bar
            )

            # Check if data came back empty
            if data.empty:
                print(f"No data returned for {ticker}")
                return None

            # Add a column to identify which ticker this row belongs to
            data["Ticker"] = ticker

            print(f"{ticker}: {len(data)} rows | "
                  f"{data.index[0].date()} → {data.index[-1].date()}")
            return data

        except Exception as e:
            print(f"Attempt {attempt} failed for {ticker}: {e}")
            if attempt < retries:
                print(f"     Waiting {wait}s before retry...")
                time.sleep(wait)
            else:
                print(f"  ✗ All {retries} attempts failed for {ticker}. Skipping.")
                return None

# Loop through all tickers and download
def run_scraper():
    all_tickers = TICKERS + [BENCHMARK]
    failed      = []   # track any tickers that couldn't be downloaded
    summary     = []   # collect summary info for the report

    for ticker in all_tickers:
        data = download_ticker(ticker, START_DATE, END_DATE)

        if data is not None:
            # Save each ticker as its own CSV file
            # Replace ^ in filename (^GSPC → GSPC.csv)
            safe_name = ticker.replace("^", "") + ".csv"
            filepath  = os.path.join(RAW_DATA_FOLDER, safe_name)
            data.to_csv(filepath)
            print(f"     Saved → {filepath}\n")

            summary.append({
                "Ticker"    : ticker,
                "Rows"      : len(data),
                "Start"     : str(data.index[0].date()),
                "End"       : str(data.index[-1].date()),
                "Null Count": int(data.isnull().sum().sum()),
                "Status"    : "OK"
            })
        else:
            failed.append(ticker)
            summary.append({
                "Ticker" : ticker,
                "Rows"   : 0,
                "Start"  : "—",
                "End"    : "—",
                "Null Count": "—",
                "Status" : "FAILED"
            })

        # Small pause between downloads to avoid rate limiting
        time.sleep(1)


    summary_df = pd.DataFrame(summary)
    print(summary_df.to_string(index=False))

    # Save summary report as CSV
    summary_path = os.path.join(RAW_DATA_FOLDER, "_download_summary.csv")
    summary_df.to_csv(summary_path, index=False)

    if failed:
        print(f"  {len(failed)} ticker(s) failed: {failed}")
    else:
        print(f"All {len(all_tickers)} tickers downloaded successfully")


if __name__ == "__main__":
    run_scraper()
