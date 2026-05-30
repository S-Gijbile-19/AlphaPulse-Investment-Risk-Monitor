# Dataset Documentation

## main_prices.csv

### Purpose

Contains historical daily closing prices for portfolio assets and the S&P 500 benchmark from 2019 to 2024.

### Rows

1509

### Columns

| Column | Description                           |
| ------ | ------------------------------------- |
| Date   | Trading date                          |
| AAPL   | Apple stock closing price             |
| META   | Meta stock closing price              |
| JPM    | JPMorgan Chase stock closing price    |
| JNJ    | Johnson & Johnson stock closing price |
| XOM    | Exxon Mobil stock closing price       |
| AMZN   | Amazon stock closing price            |
| PG     | Procter & Gamble stock closing price  |
| NEE    | NextEra Energy stock closing price    |
| CAT    | Caterpillar stock closing price       |
| NVDA   | NVIDIA stock closing price            |
| SP500  | S&P 500 Index closing value           |

### Usage

* Stock Price Trend Analysis
* Portfolio Performance Tracking
* Benchmark Comparison

---

## main_returns.csv

### Purpose

Contains daily percentage returns for all portfolio assets and the S&P 500 benchmark.

### Rows

1508

### Columns

| Column | Description                       |
| ------ | --------------------------------- |
| Date   | Trading date                      |
| AAPL   | Daily return of Apple             |
| META   | Daily return of Meta              |
| JPM    | Daily return of JPMorgan Chase    |
| JNJ    | Daily return of Johnson & Johnson |
| XOM    | Daily return of Exxon Mobil       |
| AMZN   | Daily return of Amazon            |
| PG     | Daily return of Procter & Gamble  |
| NEE    | Daily return of NextEra Energy    |
| CAT    | Daily return of Caterpillar       |
| NVDA   | Daily return of NVIDIA            |
| SP500  | Daily return of S&P 500           |

### Usage

* Value at Risk (VaR)
* Monte Carlo Simulation
* Correlation Analysis
* Rolling Volatility Analysis

---

## data_summary.csv

### Purpose

Provides summary statistics and data quality metrics for each portfolio asset.

### Rows

11

### Columns

| Column           | Description                   |
| ---------------- | ----------------------------- |
| Ticker           | Stock Symbol                  |
| Rows             | Number of records             |
| Start            | First available date          |
| End              | Last available date           |
| Start Price      | Initial stock price           |
| End Price        | Final stock price             |
| Total Return %   | Overall return percentage     |
| Null Count       | Number of missing values      |
| Avg Daily Return | Average daily return          |
| Volatility (Std) | Standard deviation of returns |

### Usage

* Data Validation
* Portfolio Summary
* Risk Assessment
* Performance Evaluation
