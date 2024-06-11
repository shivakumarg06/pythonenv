import yfinance as yf
import ta
import pandas as pd

# List of stocks
stocks = ["BHEL.NS", "VEDL.NS", "RECLTD.NS", "TATASTEEL.NS", "PFC.NS"]


def download_stock_data(symbol):
    # Download historical data as dataframe
    df = yf.download(symbol, period="1y")
    return df


def calculate_indicators(df):
    # Calculate indicators
    df["EMA9"] = ta.trend.ema_indicator(df["Close"], window=9)
    df["EMA15"] = ta.trend.ema_indicator(df["Close"], window=15)
    df["EMA200"] = ta.trend.ema_indicator(df["Close"], window=200)
    df["MACD"] = ta.trend.MACD(
        df["Close"], window_slow=52, window_fast=24, window_sign=9
    ).macd()
    df["MACD Signal"] = ta.trend.MACD(
        df["Close"], window_slow=52, window_fast=24, window_sign=9
    ).macd_signal()
    df["RSI"] = ta.momentum.rsi(df["Close"], window=140)
    df["Stoch RSI"] = ta.momentum.stochrsi(
        df["RSI"], window=140, smooth1=10, smooth2=10
    )
    return df


def check_conditions(df):
    # Initialize empty list to store results
    results = []
    # Loop through dataframe
    for i in range(1, len(df)):
        # Get current and previous row
        row = df.iloc[i]
        prev_row = df.iloc[i - 1]
        # Check entry conditions
        entry_condition = (
            row["EMA9"] > row["EMA15"]
            and row["MACD"] > row["MACD Signal"]
            # and row["Stoch RSI"] < 20
        )
        # Check exit conditions
        exit_condition = row["MACD"] < row["MACD Signal"]
        # Append results
        results.append(
            {
                "Date": row.name,
                "Close": row["Close"],
                "Entry": entry_condition,
                "Exit": exit_condition,
            }
        )
    return pd.DataFrame(results)


def process_stock(symbol):
    df = download_stock_data(symbol)
    df = calculate_indicators(df)
    results_df = check_conditions(df)
    results_df["Stock"] = symbol
    print(results_df)
    results_df.to_csv(f"{symbol}_results.csv", index=False)
    return results_df


for stock in stocks:
    process_stock(stock)
