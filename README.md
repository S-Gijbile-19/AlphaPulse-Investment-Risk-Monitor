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

## Project Workflow

1. Data Collection
   - Historical stock data fetched using yFinance.

2. Returns Analysis
   - Daily log returns calculated for each asset.

3. Risk Analytics
   - Rolling Volatility
   - Correlation Analysis
   - Monte Carlo Simulation
   - Value at Risk (VaR)

4. Dashboard & Reporting
   - Tableau / Power BI visualizations
   - Risk monitoring outputs

5. Decision Support
   - Portfolio risk assessment
   - Diversification insights

*Week 1 complete. All clean data files are in `data/clean/` and ready for Week 2 Monte Carlo simulation and Tableau visualisation.*



# Week 3: Portfolio Risk Analytics & Visualization

## Overview

Week 3 focused on evaluating portfolio risk and developing visual analytics to support investment decision-making. Various statistical techniques were applied to measure risk exposure, analyze asset relationships, and monitor portfolio performance under different market conditions.

## Objectives

* Analyze relationships between portfolio assets.
* Measure potential portfolio losses using Value at Risk (VaR).
* Evaluate portfolio return behavior and volatility.
* Develop visual dashboards for risk monitoring and reporting.

## Key Activities

### Asset Correlation Analysis

An asset correlation matrix was generated to understand how portfolio assets move relative to one another. This analysis helps identify diversification opportunities and assess concentration risk.

**Deliverable:**

* Asset Correlation Matrix Heatmap

### Value at Risk (VaR) Analysis

Historical Value at Risk (VaR) at a 95% confidence level was calculated to estimate the maximum expected portfolio loss during adverse market movements.

**Deliverable:**

* Portfolio VaR (95%) Report
* VaR Visualization

### Return Distribution Analysis

Daily portfolio returns were analyzed to understand return patterns, identify extreme outcomes, and evaluate overall return behavior.

**Deliverable:**

* Return Distribution Histogram

### Rolling Volatility Analysis

Rolling volatility was calculated to monitor changes in portfolio risk over time and identify periods of increased market uncertainty.

**Deliverable:**

* Rolling Portfolio Volatility Visualization

### Executive Dashboard Development

A consolidated executive dashboard was developed to provide a high-level overview of portfolio performance and risk metrics. The dashboard integrates key indicators, charts, and risk analytics into a single monitoring interface.

**Deliverable:**

* Executive Portfolio Dashboard

## Tools & Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Tableau
* Git & GitHub

## Key Outputs

* Asset Correlation Matrix
* Portfolio Value at Risk (95%)
* Return Distribution Analysis
* Rolling Volatility Monitoring
* Executive Risk Dashboard

## Learning Outcomes

* Applied quantitative risk measurement techniques.
* Improved understanding of portfolio diversification and risk exposure.
* Developed financial data visualization skills.
* Created executive-level reporting dashboards for investment analysis.

## Project Status

Week 3 successfully enhanced the AlphaPulse Investment Risk Monitor by introducing portfolio risk analytics, advanced visualizations, and executive reporting capabilities.
Week 4-ku GitHub README/documentation-la podura maari professional-a detailed content:

# Week 4: Portfolio Automation & Executive Reporting

## Overview

Week 4 focused on automating the complete investment risk monitoring workflow and creating executive-level reporting capabilities. The objective was to eliminate manual intervention in data processing, ensure regular portfolio updates, and provide decision-makers with a concise summary of key portfolio risk indicators. The entire analytics pipeline was scheduled to run automatically, generating updated risk metrics and visual reports whenever new market data became available.

---

## Objectives

* Automate end-to-end portfolio risk analysis workflow.
* Schedule periodic market data refreshes.
* Generate updated portfolio risk metrics automatically.
* Develop executive-level summary reporting.
* Improve monitoring and maintenance capabilities.
* Validate the accuracy of all calculated risk measures.

---

## Key Activities

### Workflow Automation

The complete AlphaPulse Investment Risk Monitor pipeline was automated to perform all required tasks without manual execution. The workflow includes:

* Market data collection
* Data cleaning and preprocessing
* Portfolio return calculations
* Risk metric generation
* Visualization updates
* Dashboard refresh

Automation ensures that portfolio analytics remain current and available for continuous monitoring.

**Deliverable:**

* Automated End-to-End Risk Analytics Pipeline

---

### Scheduled Data Refresh

A scheduling mechanism was implemented to refresh market data at predefined intervals. This allows the system to continuously collect the latest stock prices and update all portfolio calculations automatically.

Key features include:

* Scheduled execution
* Automated data retrieval
* Refresh status monitoring
* Failure detection and logging

**Deliverable:**

* Automated Market Data Refresh System

---

### Executive Summary Dashboard

A dedicated executive reporting section was developed to provide a high-level overview of portfolio performance and risk exposure.

The dashboard includes:

* Portfolio Value
* Total Return
* Portfolio Volatility
* Value at Risk (VaR)
* Maximum Drawdown
* Diversification Metrics
* Risk Trend Indicators

The objective is to help stakeholders quickly assess portfolio health and make informed investment decisions.

**Deliverable:**

* Executive Summary Dashboard

---

### Performance Monitoring & Error Handling

System monitoring capabilities were added to track workflow execution and identify operational issues.

Key functionalities include:

* Refresh status validation
* Error logging
* Data quality verification
* Recovery procedures for failed executions

This improves reliability and minimizes downtime.

**Deliverable:**

* Refresh Monitoring & Error Handling Framework

---

### Financial Accuracy Validation

All portfolio risk calculations were reviewed and validated against standard financial methodologies to ensure accuracy and consistency.

Validation checks included:

* Portfolio Return Calculations
* Volatility Metrics
* Value at Risk (VaR)
* Maximum Drawdown
* Correlation Analysis

Results were compared against benchmark financial calculations to verify correctness.

**Deliverable:**

* Financial Accuracy Validation Report

---

## Tools & Technologies

* Python
* Pandas
* NumPy
* Matplotlib
* Seaborn
* Tableau
* Git & GitHub
* Windows Task Scheduler / Cron Jobs

---

## Key Outputs

* Fully Automated Risk Analytics Pipeline
* Scheduled Market Data Refresh System
* Executive Summary Dashboard
* Workflow Monitoring Framework
* Error Handling Procedures
* Financial Accuracy Validation Report

---

## Learning Outcomes

* Gained experience in workflow automation and scheduling.
* Improved understanding of production-ready analytics systems.
* Learned techniques for monitoring and maintaining automated pipelines.
* Developed executive reporting and KPI presentation skills.
* Applied financial validation methods to verify risk calculations.

---

Week 4 successfully completed the AlphaPulse Investment Risk Monitor project by transforming the analytics workflow into a fully automated and production-ready system. Automated data refreshes, executive dashboards, monitoring capabilities, and financial validation processes were integrated to ensure reliable portfolio risk analysis and decision support.

### Final Project Deliverables

✅ Historical Market Data Pipeline

✅ Portfolio Return Analysis

✅ Monte Carlo Simulation Model

✅ Asset Correlation Analysis

✅ Value at Risk (VaR) Estimation

✅ Rolling Volatility Monitoring

✅ Executive Risk Dashboard

✅ Automated Data Refresh System

✅ Financial Validation Framework

✅ Production-Ready AlphaPulse Investment Risk Monitor





