
import os
import numpy as np
import pandas as pd

CLEAN_FOLDER = "data/clean"
TICKERS = [
    "AAPL", "META", "JPM", "JNJ", "XOM",
    "AMZN", "PG",   "NEE", "CAT", "NVDA", "SP500"
]

# ── Helper ────────────────────────────────────
def check(label, passed, detail=""):
    status = " PASS" if passed else " FAIL"
    print(f"  {status}  |  {label}")
    if detail:
        print(f"            {detail}")
    return passed

# ── Main ──────────────────────────────────────
def run_validation():
    results = []
    # ── Load files ────────────────────────────
    print("\n── Loading clean files")
    prices_path  = os.path.join(CLEAN_FOLDER, "master_prices.csv")
    returns_path = os.path.join(CLEAN_FOLDER, "master_returns.csv")

    results.append(check("master_prices.csv exists",
                         os.path.exists(prices_path)))
    results.append(check("master_returns.csv exists",
                         os.path.exists(returns_path)))

    if not all(results):
        print("\n  Files missing — did cleaner.py run?")
        return

    prices  = pd.read_csv(prices_path,  index_col=0, parse_dates=True)
    returns = pd.read_csv(returns_path, index_col=0, parse_dates=True)

    # ── Section 1: Shape checks ───────────────
    print("\n── SECTION 1: Shape & Structure")
    results.append(check("Prices has 11 columns (10 stocks + SP500)",
                         prices.shape[1] == 11,
                         f"Actual: {prices.shape[1]} columns"))

    results.append(check("Returns has 11 columns",
                         returns.shape[1] == 11,
                         f"Actual: {returns.shape[1]} columns"))

    results.append(check("Returns has one less row than prices (log return shift)",
                         returns.shape[0] == prices.shape[0] - 1,
                         f"Prices: {prices.shape[0]} rows | Returns: {returns.shape[0]} rows"))

    results.append(check("All expected tickers present in prices",
                         all(t in prices.columns for t in TICKERS),
                         f"Columns: {list(prices.columns)}"))

    results.append(check("All expected tickers present in returns",
                         all(t in returns.columns for t in TICKERS),
                         f"Columns: {list(returns.columns)}"))

    # ── Section 2: Date checks ─────────────────
    print("\n── SECTION 2: Date Range")
    results.append(check("Prices start date is 2019-01-02",
                         str(prices.index[0].date()) == "2019-01-02",
                         f"Actual start: {prices.index[0].date()}"))

    results.append(check("Prices end date is 2024-12-30",
                         str(prices.index[-1].date()) == "2026-06-02",
                         f"Actual end: {prices.index[-1].date()}"))

    results.append(check("No duplicate dates in prices",
                         prices.index.duplicated().sum() == 0,
                         f"Duplicates: {prices.index.duplicated().sum()}"))

    results.append(check("No duplicate dates in returns",
                         returns.index.duplicated().sum() == 0,
                         f"Duplicates: {returns.index.duplicated().sum()}"))

    results.append(check("Prices index is sorted chronologically",
                         prices.index.is_monotonic_increasing))

    # ── Section 3: Data integrity ──────────────
    print("\n── SECTION 3: Data Integrity")
    results.append(check("No null values in prices",
                         prices.isnull().sum().sum() == 0,
                         f"Total nulls: {prices.isnull().sum().sum()}"))

    results.append(check("No null values in returns",
                         returns.isnull().sum().sum() == 0,
                         f"Total nulls: {returns.isnull().sum().sum()}"))

    results.append(check("No negative prices",
                         (prices < 0).sum().sum() == 0))

    results.append(check("No zero prices",
                         (prices == 0).sum().sum() == 0))

    results.append(check("All prices are numeric (float)",
                         all(prices[c].dtype in [np.float64, np.float32]
                             for c in prices.columns)))

    results.append(check("All returns are numeric (float)",
                         all(returns[c].dtype in [np.float64, np.float32]
                             for c in returns.columns)))

    # ── Section 4: Financial sanity ────────────
    print("\n── SECTION 4: Financial Sanity Checks")

    # NVDA should have highest total return
    total_returns = (prices.iloc[-1] / prices.iloc[0] - 1) * 100
    best = total_returns.idxmax()
    results.append(check("NVDA is the best performing stock (expected)",
                         best == "NVDA",
                         f"Best: {best} at {total_returns[best]:.1f}%"))

    # JNJ should be lowest volatility stock
    vols = returns.std()
    lowest_vol = vols.idxmin()
    results.append(check("JNJ or SP500 is lowest volatility (defensive stock)",
                         lowest_vol in ["JNJ", "SP500"],
                         f"Lowest vol: {lowest_vol} at {vols[lowest_vol]*100:.3f}%"))

    # Returns should be near zero mean (efficient market)
    mean_ret = returns.mean().mean()
    results.append(check("Mean daily return is small and positive (market drift)",
                         0 < mean_ret < 0.005,
                         f"Portfolio mean daily return: {mean_ret*100:.4f}%"))

    # All stocks should have positive 5yr return
    all_positive = (total_returns > 0).all()
    results.append(check("All stocks have positive 5-year total return",
                         all_positive,
                         f"Negative returns: {list(total_returns[total_returns<=0].index)}"))

    # ── Section 5: Week 2 readiness ────────────
    print("\n── SECTION 5: Week 2 Readiness")

    # Can we compute covariance matrix? (needed for portfolio variance)
    try:
        cov = returns.cov()
        results.append(check("Covariance matrix computable (needed for VaR)",
                             cov.shape == (11, 11),
                             f"Cov matrix shape: {cov.shape}"))
    except Exception as e:
        results.append(check("Covariance matrix computable", False, str(e)))

    # Can we compute correlation matrix? (needed for heatmap)
    try:
        corr = returns.corr()
        results.append(check("Correlation matrix computable (needed for heatmap)",
                             corr.shape == (11, 11)))
    except Exception as e:
        results.append(check("Correlation matrix computable", False, str(e)))

    # Check returns are usable for Monte Carlo (no inf values)
    has_inf = np.isinf(returns.values).sum()
    results.append(check("No infinite values in returns (Monte Carlo safe)",
                         has_inf == 0,
                         f"Inf count: {has_inf}"))

    # ── Final summary ──────────────────────────
    passed = sum(results)
    total  = len(results)
    print("\n" + "="*60)
    print(f"  FINAL SCORE: {passed} / {total} checks passed")
    print("="*60)

    if passed == total:
        print("   ALL CHECKS PASSED ")
        print("   master_prices.csv ")
        print("   master_returns.csv ")
    else:
        failed = total - passed
        print(f"  ⚠ {failed} check(s) failed")



if __name__ == "__main__":
    run_validation()
