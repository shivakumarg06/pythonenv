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
    macd = ta.trend.MACD(df["Close"], window_slow=52, window_fast=24, window_sign=9)
    df["MACD"] = macd.macd()
    df["MACD Signal"] = macd.macd_signal()
    df["RSI"] = ta.momentum.rsi(df["Close"], window=140)
    df["Stoch RSI"] = ta.momentum.stochrsi(
        df["RSI"], window=140, smooth1=10, smooth2=10
    )
    return df


def check_conditions(df):
    # Calculate entry and exit conditions
    df["Entry"] = (df["EMA9"] > df["EMA15"]) & (df["MACD"] > df["MACD Signal"])
    df["Exit"] = df["MACD"] < df["MACD Signal"]
    # Create results dataframe
    results_df = df[["Close", "Entry", "Exit"]].copy()
    results_df["Date"] = df.index
    return results_df


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
