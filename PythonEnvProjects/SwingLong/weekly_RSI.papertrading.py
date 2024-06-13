from fyers_api import fyersModel
import ta
import pandas as pd
import time

# List of stocks
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB"]

# Initialize a DataFrame to hold the current position for each stock
positions = pd.DataFrame(index=stocks, columns=["Position", "Entry_Price"])
positions.fillna(0, inplace=True)

# Initialize Fyers API
fyers = fyersModel.FyersModel(is_async=False)


def process_stock_data(symbol):
    try:
        # Download historical data as dataframe
        data = fyers.get_historical_data(
            symbol=symbol, period="5minute", data_range="1day"
        )
        df = pd.DataFrame(
            data["candles"], columns=["date", "open", "high", "low", "close", "volume"]
        )

        # Calculate RSI
        df["RSI"] = ta.momentum.RSIIndicator(df["close"], window=14).rsi()

        # Calculate 20-period EMA
        df["EMA_20"] = ta.trend.EMAIndicator(df["close"], window=20).ema_indicator()

        # Create a column for the high of the previous candle
        df["Prev_High"] = df["high"].shift(1)

        # Create a column for the previous day's volume
        df["Prev_Volume"] = df["volume"].shift(1)

        # Generate signals based on the strategy
        df["Signal"] = 0
        df.loc[(df["RSI"] > 55) & (df["volume"] > df["Prev_Volume"]), "Signal"] = (
            1  # Entry signal
        )
        buffer = 0.03
        df.loc[df["close"] < df["EMA_20"] * (1 - buffer), "Signal"] = -1  # Exit signal

        return df
    except Exception as e:
        print(f"Failed to process data for {symbol}: {e}")
        return None


while True:
    for stock in stocks:
        stock_data = process_stock_data(stock)
        if stock_data is not None:
            # Get the last signal
            signal = stock_data["Signal"].iloc[-1]

            # If the signal is 1 and we don't have a position, buy
            if signal == 1 and positions.loc[stock, "Position"] == 0:
                positions.loc[stock, "Position"] = 1
                positions.loc[stock, "Entry_Price"] = stock_data["close"].iloc[-1]
                print(f"Buy signal for {stock} at {stock_data['close'].iloc[-1]}")

            # If the signal is -1 and we have a position, sell
            elif signal == -1 and positions.loc[stock, "Position"] > 0:
                positions.loc[stock, "Position"] = 0
                print(f"Sell signal for {stock} at {stock_data['close'].iloc[-1]}")

    # Sleep for 5 minutes before the next iteration
    time.sleep(300)
