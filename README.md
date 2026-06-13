# AlphaPulse-Investment-Risk-Monitor
Financial analytics project for portfolio risk, volatility, and Monte Carlo simulation using Python and Tableau.




# **Week 1:** Data Acquisition & Cleaning


##  Portfolio Overview

| Ticker | Company | Sector | 5yr Return |
|--------|---------|--------|------------|
| AAPL | Apple | Technology | 568.8% |
| META | Meta Platforms | Communication | 337.4% |
| JPM | JPMorgan Chase | Financials | 187.1% |
| JNJ | Johnson & Johnson | Healthcare | 32.5% |
| XOM | ExxonMobil | Energy | 102.7% |
| AMZN | Amazon | Consumer | 187.6% |
| PG | Procter & Gamble | Consumer | 112.9% |
| NEE | NextEra Energy | Utilities | 94.7% |
| CAT | Caterpillar | Industrials | 229.6% |
| NVDA | NVIDIA | Technology | 3970.1% |
| ^GSPC | S&P 500 Index | Benchmark | 135.3% |

**Date Range:** 2019-01-02 → 2026-06-03  
**Trading Days:** 1,865 rows per ticker  
**Source:** Yahoo Finance via `yfinance` (auto-adjusted for splits & dividends)

---

##  Folder Structure

```
alphapulse/
├── data/
│   ├── raw/                        ← Individual ticker CSVs
│   │   ├── AAPL.csv
│   │   ├── AMZN.csv
│   │   ├── CAT.csv
│   │   ├── JNJ.csv
│   │   ├── JPM.csv
│   │   ├── META.csv
│   │   ├── NEE.csv
│   │   ├── NVDA.csv
│   │   ├── PG.csv
│   │   ├── XOM.csv
│   │   ├── GSPC.csv                ← S&P 500 benchmark
│   │   ├── plots/ 
│   │   │    ├── master_prices.csv       ← All 11 tickers, adjusted close prices
│   │   │     ├── master_returns.csv      ← Daily log returns for all tickers
│   │   │     ├── data_summary.csv        ← Summary stats per ticker
│   │   │     └── sanity_check.png
│   │   │ 
│   │   ├── price_chart.png        ← Normalised price chart
│   │   └── plot_raw_prices.png    ← Daily returns distribution
│   └── clean/                      
│       ├── master_prices.csv       ← All 11 tickers, adjusted close prices
│       ├── master_returns.csv      ← Daily log returns for all tickers
│       ├── data_summary.csv        ← Summary stats per ticker
│       └── sanity_check.png  ← Cumulative returns + correlation preview
└── src/
    ├── config.py                   ← Tickers, dates, settings
    ├── scraper.py                  ←  downloads raw data
    ├── corporate_actions.py        ←  verifies adjustments
    ├── plot_prices.py              ←  generates charts
    └── cleaner.py                
```

---


##  Key Statistics

| Ticker | Mean Daily Return | Daily Volatility | Worst Day | Best Day |
|--------|------------------|-----------------|-----------|----------|
| AAPL | 0.126% | 1.943% | -13.77% | +11.32% |
| META | 0.098% | 2.706% | -30.64% | +20.93% |
| JPM | 0.070% | 1.927% | -16.21% | +16.56% |
| JNJ | 0.019% | 1.205% | -7.58% | +7.69% |
| XOM | 0.047% | 2.032% | -13.04% | +11.94% |
| AMZN | 0.070% | 2.150% | -15.14% | +12.70% |
| PG | 0.050% | 1.276% | -9.14% | +11.34% |
| NEE | 0.044% | 1.792% | -14.41% | +12.83% |
| CAT | 0.079% | 1.997% | -15.41% | +9.83% |
| NVDA | 0.246% | 3.251% | -20.40% | +21.81% |
| SP500 | 0.057% | 1.274% | -12.77% | +8.97% |

---

##  Data Quality Checks Completed

| Check | Result |
|-------|--------|
| Stock split adjustments (AAPL, NVDA, AMZN) | ✅ Verified |
| Dividend adjustments (META, JPM, etc.) | ✅ Auto-adjusted |
| Anomalous price moves > 30% | ✅ Zero found |
| Date alignment across all tickers | ✅ 1865 common dates |
| Null values | ✅ Zero |
| Negative or zero prices | ✅ Zero |
| Duplicate dates | ✅ Zero |
| Covariance matrix computable | ✅ Ready |
| Correlation matrix computable | ✅ Ready |

---

##  Important Notes for Week 2

1. **NVDA dominates** — at 3.251% daily volatility it is 2.7x more volatile than JNJ. Use **equal weighting** carefully; consider volatility-weighted or custom portfolio weights for VaR.

2. **META's worst day (-30.64%)** was Feb 3, 2022 (first-ever user count decline reported). This is a real event — not a data error. It is an important tail risk input for VaR.

3. **Log returns** (not % returns) are already computed in `master_returns.csv`. Use these directly for Monte Carlo — do not recompute from prices.

4. **S&P 500 is stored as `SP500`** in both CSVs.

5. **Date range note:** Markets were closed Jan 1 and Dec 31, so actual data runs 2019-01-02 → 2026-06-03.

---

##  Tech Stack Used in Week 1

| Tool | Purpose |
|------|---------|
| `yfinance` | Download historical OHLCV data from Yahoo Finance |
| `pandas` | Data manipulation and DataFrame operations |
| `numpy` | Log return calculations and matrix operations |
| `matplotlib` | Price charts and return distribution plots |

---

*Week 1 complete. All clean data files are in `data/clean/` and ready for Week 2 Monte Carlo simulation and Tableau visualisation.*

GitHub-க்கு **detailed version** வேணும்னா இதைப் போடலாம்:

**Week 4 – Finalization**

In the final phase of the project, I automated the complete market data refresh process by developing `refresh_data.py`. This script downloads the latest stock prices for all 11 selected tickers, calculates daily log returns, and updates the master datasets (`master_prices.csv` and `master_returns.csv`). To eliminate manual intervention, the process was scheduled to run automatically every Sunday using Windows Task Scheduler.

To provide high-level business insights, I developed `executive_summary.py`, which calculates key risk metrics such as Value at Risk (VaR 95%) and Maximum Drawdown for all 11 stocks. The results are exported into `executive_summary.csv`, enabling quick executive-level analysis of portfolio risk.

To ensure the reliability and accuracy of all calculations, I built `accuracy_check.py`, which validates important financial metrics including Sharpe Ratio, Annual Return, and Volatility across the entire dataset. The validation process successfully achieved a **100% pass rate**, with **zero null values** detected across **1,508 trading days**, confirming the integrity and consistency of the data pipeline.

**Outcome:** Successfully delivered a fully automated end-to-end financial risk analytics workflow, covering data collection, risk metric generation, executive reporting, validation, and scheduled execution with high accuracy and reliability.




