import pandas as pd
import numpy as np
import pandas_ta as ta
import yfinance as yf


# Function to fetch historical data from Yahoo Finance
def fetch_historical_data(ticker, start_date, end_date):
    data = yf.download(ticker, start=start_date, end=end_date)
    return data


# Function to fetch the current price for a given ticker symbol
def fetch_current_price(ticker):
    current_price = yf.Ticker(ticker).history(period="1d")["Close"].iloc[-1]
    return current_price


# Define trading strategy functions
def ema_signal(df, current_candle, backcandles):
    df_slice = df.reset_index().copy()
    start = max(0, current_candle - backcandles)
    end = current_candle
    relevant_rows = df_slice.iloc[start:end]

    if all(relevant_rows["EMA_fast"] < relevant_rows["EMA_slow"]):
        return 1
    elif all(relevant_rows["EMA_fast"] > relevant_rows["EMA_slow"]):
        return 2
    else:
        return 0


def total_signal(df, current_candle, backcandles):
    if (
        ema_signal(df, current_candle, backcandles) == 2
        and df.Close.iloc[current_candle] <= df["BBL_15_1.5"].iloc[current_candle]
    ):
        return 2
    if (
        ema_signal(df, current_candle, backcandles) == 1
        and df.Close.iloc[current_candle] >= df["BBU_15_1.5"].iloc[current_candle]
    ):
        return 1
    return 0


# Backtest trading strategy
def backtest_trading_strategy(data, ticker, entry_threshold=60, backcandles=7):
    data["EMA_fast"] = ta.ema(data["Close"], length=30)
    data["EMA_slow"] = ta.ema(data["Close"], length=50)
    data["RSI"] = ta.rsi(data["Close"], length=10)
    my_bbands = ta.bbands(data["Close"], length=15, std=1.5)
    data = data.join(my_bbands)

    signals = [total_signal(data, i, backcandles) for i in range(len(data))]
    data["Signal"] = signals

    # Backtest
    positions = []
    in_position = False
    trades = []  # Store trade information
    open_position = None  # Store information about open position
    trade_id = 1  # Unique identifier for each trade
    for i, signal in enumerate(signals):
        if signal == 1 and not in_position:
            positions.append("Buy")
            in_position = True
            entry_price = data["Close"].iloc[i]
            trades.append(
                (trade_id, ticker, "Buy", data.index[i], entry_price, None, None)
            )  # Entry
            open_position = {"entry_price": entry_price, "entry_index": i}
        elif signal == 2 and in_position:
            positions.append("Sell")
            in_position = False
            exit_price = data["Close"][i]
            profit_loss = exit_price - open_position["entry_price"]
            trades.append(
                (trade_id, ticker, "Sell", data.index[i], exit_price, profit_loss, None)
            )  # Exit
            trade_id += 1
            open_position = None
        else:
            positions.append(None)

        # Calculate current profit/loss of open position
        if open_position is not None:
            current_price = data["Close"].iloc[i]
            open_position["current_profit_loss"] = (
                current_price - open_position["entry_price"]
            )

    data["Position"] = positions

    return data, trades


# Main function for backtesting
def backtest(ticker_file, start_date, end_date):
    # Read ticker information from CSV file
    tickers_df = pd.read_csv(ticker_file)
    tickers = tickers_df["Symbol"].apply(lambda x: f"{x}.NS").tolist()

    all_trades = []  # Store all trades for all tickers
    for ticker in tickers:
        # Fetch historical data
        data = fetch_historical_data(ticker, start_date, end_date)

        # Fetch current price
        current_price = fetch_current_price(ticker)

        # Backtest trading strategy
        backtest_results, trades = backtest_trading_strategy(
            data, ticker, current_price
        )

        # Store trades for this ticker
        all_trades.extend(trades)

        # Print or save backtest results
        print(f"Backtest results for {ticker}:")
        print(backtest_results)

    # Export all trades to Excel
    trades_df = pd.DataFrame(
        all_trades,
        columns=[
            "Trade ID",
            "Ticker",
            "Trade",
            "Date",
            "Price",
            "Profit/Loss",
            "Current Profit/Loss",
        ],
    )

    # Fill missing values in Profit/Loss column with 0 for open positions
    trades_df["Profit/Loss"] = trades_df["Profit/Loss"].fillna(0)

    # Fill missing values in Current Profit/Loss column with previous value for open positions
    trades_df["Current Profit/Loss"] = trades_df["Current Profit/Loss"].fillna(
        method="ffill"
    )

    trades_df.to_excel("trades.xlsx", index=False)


# Main script
if __name__ == "__main__":
    # Define ticker file and date range
    ticker_file = "ind_nifty100list.csv"  # Provide the path to your CSV file
    start_date = "2024-01-01"
    end_date = "2024-05-30"

    # Perform backtesting for tickers from CSV file
    backtest(ticker_file, start_date, end_date)
