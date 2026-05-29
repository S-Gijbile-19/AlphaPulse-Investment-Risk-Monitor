import yfinance as yf
from config import TICKERS, START_DATE, END_DATE

data = yf.download("AAPL", start=START_DATE, end=END_DATE)

print("Rows downloaded :", len(data))
print("Columns         :", list(data.columns))
print(data.head())


#output

# [*********************100%***********************]  1 of 1 completed
# Rows downloaded : 1509
# Columns         : [('Close', 'AAPL'), ('High', 'AAPL'), ('Low', 'AAPL'), ('Open', 'AAPL'), ('Volume', 'AAPL')]
# Price           Close       High        Low       Open     Volume
# Ticker           AAPL       AAPL       AAPL       AAPL       AAPL
# 2019-01-02  37.469200  37.689860  36.593684  36.750281  148158800
# 2019-01-03  33.736988  34.574540  33.691907  34.161694  365248800
# 2019-01-04  35.177208  35.246017  34.118999  34.292203  234428400
# 2019-01-07  35.098919  35.312461  34.617267  35.281616  219111200
# 2019-01-08  35.767990  36.021867  35.238886  35.485642  164101200