# Importing the required libraries
import sys

sys.path.insert(0, "F:\\GitHub\\pythonenv\\PythonEnvProjects\\Fyers")


import credentials as cd
from fyers_apiv3 import fyersModel
import ta
import pandas as pd
import numpy as np
import datetime as dt
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import mplfinance as mpf
import fyers_model
import indicators
from strategy import (
    calculate_sma_crossover_signals,
    calculate_ema_crossover_signals,
    calculate_rsi_with_ema_signals,
)
from fyers_get_orders import FyersDataFetcher
from fyers_execute_orders import place_market_order, place_cnc_market_order

print(cd.client_id)

# Read the symbols from the CSV file
df_listofStocks = pd.read_csv("symbols.csv")

# Get the symbols as a list
symbols = df_listofStocks["Symbol"].tolist()


for symbol in symbols:
    data = {
        "symbol": "NSE:"
        + symbol
        + "-EQ",  # add the "NSE:" prefix and "-EQ" suffix to each symbol
        "resolution": "5",
        "date_format": "1",
        "range_from": "2024-04-01",
        "range_to": "2024-05-30",
        "cont_flag": "1",
    }

    # Initialize historical_data
    historical_data = fyers_model.initialize_fyersApi_historical_data(data)
    if historical_data is None:
        print(f"Could not fetch historical data for symbol: {symbol}")
        continue
    # print(historical_data)

    # Process and save historical_data
    processed_data = fyers_model.process_and_save_data(historical_data)
    if processed_data is None:
        print(f"Could not process and save data for symbol: {symbol}")
        continue
    # print(processed_data)

    # Initialize the FyersModel instance
    fyers = fyers_model.initialize_fyers_model()

    data = {
        "symbol": "NSE:HATHWAY-EQ",
        "qty": 1,
        "type": 2,
        "side": 1,
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "stopLoss": 0,
        "takeProfit": 0,
        "offlineOrder": False,
        "disclosedQty": 0,
    }

    place_market_order(fyers, data)
    place_cnc_market_order(fyers, data)
    place_limit_order(fyers, data)
    place_stop_order(fyers, data)
###############################################################################################################

# # Calculate EMA for the 'CLOSE' column
# ema = indicators.calculate_ema(processed_data["CLOSE"], window=14)

# print(ema)

# # Calculate signals
# sma_crossover = calculate_sma_crossover_signals(processed_data)

# # Print data with signals
# print(sma_crossover)

# # Calculate signals
# ema_crossover = calculate_ema_crossover_signals(
#     processed_data, short_window=9, long_window=13
# )

# # Print data with signals
# print(ema_crossover)

###############################################################################################################


# with pd.ExcelWriter("weekly_RSI_backtest_result.xlsx", engine="xlsxwriter") as writer:
#     # Assuming processed_data is a DataFrame containing the processed historical data
#     data = processed_data

#     # Calculate signals
#     stock_data = calculate_rsi_with_ema_signals(
#         data,
#         ema_short_period=9,
#         ema_long_period=15,
#         rsi_period=14,
#         rsi_threshold=55,
#         macd_fastperiod=12,
#         macd_slowperiod=26,
#         macd_signalperiod=9,
#     )

#     if stock_data is not None:
#         # Rename the columns to the format expected by mplfinance
#         stock_data.rename(
#             columns={
#                 "OPEN": "Open",
#                 "HIGH": "High",
#                 "LOW": "Low",
#                 "CLOSE": "Close",
#                 "VOLUME": "Volume",  # If you have a volume column
#             },
#             inplace=True,
#         )

#         # Sort the DataFrame by date
#         stock_data.sort_index(inplace=True)

#         # Save the DataFrame to an Excel file
#         stock_data.to_excel(writer, sheet_name=symbol)

#         # Calculate the signals based on your strategy
#         stock_data["Signal"] = np.where(
#             (
#                 (stock_data["ema_short"] > stock_data["ema_long"])
#                 & (stock_data["rsi"] > 55)
#                 & (stock_data["MACD_line"] > stock_data["Signal_line"])
#                 & (stock_data["Close"] > stock_data["Close"].rolling(window=50).mean())
#             ),
#             1.0,
#             0.0,
#         )

#         # Calculate the exit signals based on your strategy
#         stock_data["Exit_Signal"] = np.where(
#             stock_data["Close"] < stock_data["5_ema"], 1, 0
#         )

#         # Create a custom market colors scheme
#         mc = mpf.make_marketcolors(up="g", down="r", inherit=True)

#         # Create a custom style based on the market colors
#         s = mpf.make_mpf_style(marketcolors=mc)

#         # Create an additional plot for the buy signals
#         ap1 = mpf.make_addplot(
#             np.where(stock_data["Signal"] == 1, stock_data["Close"], np.nan),
#             panel=0,
#             type="scatter",
#             marker="^",
#             markersize=100,
#             color="green",
#         )

#         # Create an additional plot for the sell signals
#         ap2 = mpf.make_addplot(
#             np.where(stock_data["Exit_Signal"] == 1, stock_data["Close"], np.nan),
#             panel=0,
#             type="scatter",
#             marker="v",
#             markersize=100,
#             color="red",
#         )

#         # Plot the candlestick chart with the additional plots
#         mpf.plot(
#             stock_data,
#             type="candle",
#             mav=(9, 15),
#             volume=True,
#             style=s,
#             addplot=[ap1, ap2],
#         )

#         import seaborn as sns
#         import matplotlib.pyplot as plt

#         # Calculate the correlation matrix
#         corr = stock_data.corr()

#         # Create a heatmap
#         plt.figure(figsize=(10, 10))
#         sns.heatmap(corr, annot=True, fmt=".2f", cmap="coolwarm")

#         # Show the plot
#         plt.show()

###############################################################################################################
#  # print(initialize_fyersApi_historical_data(data))


# # List of stocks
# stocks = [
#     "NSE:360ONE",
#     "NSE:ADANIPORTS",
#     # ... rest of the stocks
# ]

# # Fyers API session
# session = fyersModel.FyersModel(is_async=False)


# def process_stock_data(symbol):
#     try:
#         # Download historical data as dataframe
#         data = session.get_historical_OHLCV(
#             symbol=symbol, data_format="df", period="1D", duration="365D"
#         )
#         df = pd.DataFrame(
#             data["candles"], columns=["date", "open", "high", "low", "close", "volume"]
#         )

#         # Convert date to datetime and set as index
#         df["date"] = pd.to_datetime(df["date"])
#         df.set_index("date", inplace=True)

#         # Resample the data to the weekly timeframe
#         df = df.resample("W").last()

#         # Calculate weekly RSI
#         df["RSI"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()

#         # Calculate 20-period EMA on the weekly timeframe
#         df["EMA_20"] = ta.trend.EMAIndicator(df["close"], window=20).ema_indicator()

#         # Create a column for the high of the previous candle
#         df["Prev_High"] = df["high"].shift(1)

#         # Create a column for the previous day's volume
#         df["Prev_Volume"] = df["volume"].shift(1)

#         # Create a column to hold the signals
#         df["Signal"] = 0

#         # Generate signals based on the strategy
#         df.loc[(df["RSI"] > 55) & (df["volume"] > df["Prev_Volume"]), "Signal"] = (
#             1  # Entry signal
#         )

#         # Set the buffer size (e.g., 3%)
#         buffer = 0.03

#         # Modify the exit condition
#         df.loc[df["close"] < df["EMA_20"] * (1 - buffer), "Signal"] = -1  # Exit signal

#         # Create columns to track trades
#         df["Position"] = (
#             df["Signal"].replace(-1, 0).cumsum().clip(upper=1)
#         )  # Long position is 1, no position is 0
#         df["Entry_Price"] = df.loc[df["Signal"] == 1, "close"]
#         df["Exit_Price"] = df.loc[df["Signal"] == -1, "close"]
#         df["PnL"] = (df["Exit_Price"] - df["Entry_Price"].shift()) * df[
#             "Position"
#         ].shift()

#         df["Stock"] = symbol

#         return df
#     except Exception as e:
#         print(f"Failed to process data for {symbol}: {e}")
#         return None


# # Process each stock and write the results to a different sheet
# with pd.ExcelWriter("weekly_RSI_backtest_result.xlsx", engine="xlsxwriter") as writer:
#     for stock in stocks:
#         stock_data = process_stock_data(stock)
#         if stock_data is not None:
#             stock_data.to_excel(writer, sheet_name=stock)
