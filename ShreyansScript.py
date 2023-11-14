import backtrader as bt
import yfinance as yf
import pandas as pd
from datetime import datetime

# Define the ticker symbols in an array for multiple stocks
ticker_symbols = ["COALINDIA.NS", "	SBFC.NS", "BEL.NS", "FEDERALBNK.NS", "TATAPOWER.NS"]

# Set the start and end dates for historical data
start_date = "2022-01-01"
end_date = "2023-11-14"

# Create a dictionary to store backtest results
backtest_results = []

for symbol in ticker_symbols:
    # Download historical Data
    data = yf.download(symbol, start=start_date, end=end_date)

    # Save the data to a CSV file if needed
    data.to_csv(f"{symbol}.csv")

    class MyStrategy(bt.Strategy):
        params = (
            ("rsi_period", 21),
            ("fast_sma_period", 50),
            ("slow_sma_period", 100),
        )

        def __init__(self):
            # initializing rsi, slow and fast sma
            self.rsi = bt.indicators.RSI(self.data.close, period=self.params.rsi_period)
            self.fast_sma = bt.indicators.SMA(self.data.close, period=self.params.fast_sma_period)
            self.slow_sma = bt.indicators.SMA(self.data.close, period=self.params.slow_sma_period)
            self.crossup = bt.ind.CrossUp(self.fast_sma, self.slow_sma)

        def next(self):
            if not self.position:
                if self.rsi > 30 and self.fast_sma > self.slow_sma:
                    self.buy(size=100)
            else:
                if self.rsi < 70:
                    self.sell(size=100)

    cerebro = bt.Cerebro()

    cerebro.addstrategy(MyStrategy)

    # Get data from CSV
    data = bt.feeds.YahooFinanceCSVData(
        dataname=f"{symbol}.csv",
        fromdate=datetime(2022, 1, 1),
        todate=datetime(2023, 11, 14)
    )

    cerebro.adddata(data)

    cerebro.broker.setcommission(commission=0.002)

    cerebro.broker.setcash(100000)

    cerebro.run()

    port_value = cerebro.broker.getvalue()
    pnl = port_value - 100000

    # Append backtest results to the list
    backtest_results.append({
        "Symbol": symbol,
        "Final Portfolio Value": port_value,
        "P/L": pnl
    })

    # Export executed lines to Excel
    trades_df = cerebro.runstrats[0].result.df
    trades_df.to_excel(f"trades_{symbol}.xlsx")

# Create a strategy backtest report in table format
backtest_report_df = pd.DataFrame(backtest_results)
backtest_report_df.to_excel("backtest_report.xlsx")

# Printing out the final results for each symbol
for result in backtest_results:
    print(f"Symbol: {result['Symbol']}")
    print(f"Final Portfolio Value: ${result['Final Portfolio Value']}")
    print(f"P/L: ${result['P/L']}")
    print("-" * 30)
