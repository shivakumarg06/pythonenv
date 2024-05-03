import pandas as pd
import yfinance as yf
from backtesting import Strategy, Backtest
import pandas_ta as ta
import numpy as np


# Function to fetch historical data from Yahoo Finance
def fetch_historical_data(tickers, start_date, end_date):
    all_data = {}
    for ticker in tickers:
        try:
            # Append ".NS" for NSE stocks
            ticker_ns = f"{ticker}.NS"
            data = yf.download(ticker_ns, start=start_date, end=end_date)
            data.drop(["Volume"], axis=1, inplace=True)
            all_data[ticker] = data
        except Exception as e:
            print(f"An error occurred for ticker {ticker}: {e}")
    return all_data


# Custom strategy class
class CustomStrategy(Strategy):
    def init(self):
        # Initialize Heiken Ashi candlesticks
        self.heiken_close = (
            self.data.Open + self.data.Close + self.data.High + self.data.Low
        ) / 4
        self.heiken_open = self.data["Open"].copy()
        self.heiken_open[0] = (self.data["Open"][0] + self.data["Close"][0]) / 2

        self.heiken_high = pd.Series(index=self.data.index)
        self.heiken_low = pd.Series(index=self.data.index)

        # Calculate Heiken Ashi High and Low
        for i in range(len(self.data)):
            self.heiken_high[i] = max(
                self.data["High"][i], self.heiken_open[i], self.heiken_close[i]
            )
            self.heiken_low[i] = min(
                self.data["Low"][i], self.heiken_open[i], self.heiken_close[i]
            )

        # Calculate EMAs and RSI
        self.ema20 = ta.ema(self.data.Close, length=20)
        self.ema50 = ta.ema(self.data.Close, length=50)
        self.rsi = ta.rsi(self.data.Close, length=12)

        print("EMA20:", self.ema20)
        print("EMA50:", self.ema50)

        if self.ema20 is None or self.ema50 is None:
            raise ValueError("EMA calculation failed. Check your data.")

        # Generate custom signal
        self.ordersignal = np.zeros(len(self.data))
        for i in range(len(self.data)):
            if (
                self.ema20[i] > self.ema50[i]
                and self.heiken_open[i] < self.ema20[i]
                and self.heiken_close[i] > self.ema20[i]
            ):
                self.ordersignal[i] = 2
            elif (
                self.ema20[i] < self.ema50[i]
                and self.heiken_open[i] > self.ema20[i]
                and self.heiken_close[i] < self.ema20[i]
            ):
                self.ordersignal[i] = 1

        # Calculate stop loss levels
        SLbackcandles = 1
        self.sl_signal = np.zeros(len(self.data))
        for row in range(SLbackcandles, len(self.data)):
            mi = 1e10
            ma = -1e10
            if self.ordersignal[row] == 1:
                for i in range(row - SLbackcandles, row + 1):
                    ma = max(ma, self.data.High[i])
                self.sl_signal[row] = ma
            if self.ordersignal[row] == 2:
                for i in range(row - SLbackcandles, row + 1):
                    mi = min(mi, self.data.Low[i])
                self.sl_signal[row] = mi

    def next(self):
        TPSLRatio = 1.5

        if len(self.trades) > 0:
            if (
                self.trades[-1].is_long
                and self.heiken_open[self.index] >= self.heiken_open[self.index]
            ):
                self.trades[-1].close()
            elif (
                self.trades[-1].is_short
                and self.heiken_open[self.index] <= self.heiken_open[self.index]
            ):
                self.trades[-1].close()

        if self.ordersignal[self.index] == 2 and len(self.trades) == 0:
            sl1 = self.sl_signal[self.index]
            tp1 = (
                self.data.Close[self.index]
                + (self.data.Close[self.index] - sl1) * TPSLRatio
            )
            self.buy(sl=sl1, tp=tp1, size=self.initsize)

        elif self.ordersignal[self.index] == 1 and len(self.trades) == 0:
            sl1 = self.sl_signal[self.index]
            tp1 = (
                self.data.Close[self.index]
                - (sl1 - self.data.Close[self.index]) * TPSLRatio
            )
            self.sell(sl=sl1, tp=tp1, size=self.initsize)


# Example usage
ticker_file = "ind_nifty100list.csv"  # Provide the path to your CSV file
start_date = "2024-01-01"
end_date = "2024-05-30"

# Read tickers from CSV file
tickers_df = pd.read_csv(ticker_file)
tickers = tickers_df["Symbol"].tolist()

# Fetch historical data for all tickers
all_data = fetch_historical_data(tickers, start_date, end_date)

# Backtest the custom strategy for each ticker
for ticker, data in all_data.items():
    bt = Backtest(data, CustomStrategy, commission=0)
    stats = bt.run()
    bt.plot()
