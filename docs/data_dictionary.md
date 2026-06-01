# Data Dictionary

## main_prices.csv

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

## main_returns.csv

Contains daily percentage returns for all assets.

Columns:

* Date
* AAPL
* META
* JPM
* JNJ
* XOM
* AMZN
* PG
* NEE
* CAT
* NVDA
* SP500

## data_summary.csv

Contains summary statistics and risk metrics.

Columns:

* Ticker
* Rows
* Start Date
* End Date
* Start Price
* End Price
* Total Return %
* Null Count
* Average Daily Return
* Volatility
