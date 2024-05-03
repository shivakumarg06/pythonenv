import yfinance as yf
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np


# Function to download historical prices for stocks
def download_historical_prices(tickers, start_date, end_date):
    for ticker in tickers:
        try:
            data = yf.download(ticker, start=start_date, end=end_date)
            data.to_excel(f"{ticker}_historical_prices.xlsx")
        except Exception as e:
            print(f"An error occurred for ticker {ticker}: {e}")


# Function to perform technical analysis
def calculate_technical_indicators(data):
    # Calculate technical indicators (e.g., moving averages, RSI, MACD)
    # Example:
    data["MA_50"] = data["Close"].rolling(50).mean()  # 50-day moving average
    data["MA_200"] = data["Close"].rolling(200).mean()  # 200-day moving average
    data["RSI"] = calculate_rsi(data["Close"])  # Relative Strength Index (RSI)
    return data


def calculate_rsi(close_prices, window=14):
    delta = close_prices.diff()
    gain = (delta.where(delta > 0, 0)).rolling(window).mean()
    loss = (-delta.where(delta < 0, 0)).rolling(window).mean()
    rs = gain / loss
    rsi = 100 - (100 / (1 + rs))
    return rsi


# Function to perform sentiment analysis (placeholder)
def perform_sentiment_analysis(data):
    # Placeholder for sentiment analysis logic
    # You can implement sentiment analysis using NLP techniques, sentiment scores from news articles or social media, etc.
    # For now, we'll just return the input data as is
    return data


# Function to backtest trading strategy
def backtest_trading_strategy(data):
    # Implement trading strategy logic based on technical indicators and sentiment analysis
    # Example strategy:
    # Buy when short-term MA crosses above long-term MA and RSI is below 30 (oversold)
    # Sell when short-term MA crosses below long-term MA or RSI is above 70 (overbought)
    data["Signal"] = 0
    data.loc[(data["MA_50"] > data["MA_200"]) & (data["RSI"] < 30), "Signal"] = (
        1  # Buy signal
    )
    data.loc[(data["MA_50"] < data["MA_200"]) | (data["RSI"] > 70), "Signal"] = (
        -1
    )  # Sell signal
    data["Position"] = data["Signal"].diff().fillna(0)
    data["Returns"] = data["Close"].pct_change() * data["Position"].shift(1)
    data["Cumulative_Returns"] = (1 + data["Returns"]).cumprod()

    # Calculate trade details
    entry_index = data[data["Position"] == 1].index
    exit_index = data[data["Position"] == -1].index
    entry_prices = data.loc[entry_index, "Close"].values
    exit_prices = data.loc[exit_index, "Close"].values

    data["Entry_Price"] = np.nan
    data.loc[entry_index, "Entry_Price"] = entry_prices
    data["Entry_Price"].ffill(inplace=True)

    data["Exit_Price"] = np.nan
    data.loc[exit_index, "Exit_Price"] = exit_prices

    data["Entry_Time"] = np.nan
    data["Exit_Time"] = np.nan
    data.loc[entry_index, "Entry_Time"] = entry_index
    data.loc[exit_index, "Exit_Time"] = exit_index
    # Calculate Profit_Loss only at the sell signals
    data["Profit_Loss"] = np.where(
        data["Signal"] == -1, data["Exit_Price"] - data["Entry_Price"], 0
    )
    data["Total_Profit_Loss"] = data["Profit_Loss"].cumsum()

    return data


# Function to plot buy and sell signals
def plot_signals(data, ticker):
    plt.figure(figsize=(12, 6))
    plt.plot(data.index, data["Close"], label="Close Price", color="black")
    plt.plot(data.index, data["MA_50"], label="50-Day MA", linestyle="--", color="blue")
    plt.plot(
        data.index, data["MA_200"], label="200-Day MA", linestyle="--", color="red"
    )

    plt.scatter(
        data.index[data["Signal"] == 1],
        data["Close"][data["Signal"] == 1],
        marker="^",
        color="green",
        label="Buy Signal",
    )
    plt.scatter(
        data.index[data["Signal"] == -1],
        data["Close"][data["Signal"] == -1],
        marker="v",
        color="red",
        label="Sell Signal",
    )
    plt.title(f"{ticker} - Price Chart with Buy/Sell Signals")
    plt.xlabel("Date")
    plt.ylabel("Price")
    plt.legend()
    plt.grid(True)
    plt.savefig(f"{ticker}_price_chart.png")
    plt.plot(data["Profit_Loss"])
    plt.show()


# Main script
tickers = ["SWANENERGY.NS", "NTPC.NS", "VEDL.NS", "PFC.NS", "RECLTD.NS"]
start_date = "2024-01-01"
end_date = "2024-05-30"

# Download historical prices
download_historical_prices(tickers, start_date, end_date)

# Perform technical analysis
for ticker in tickers:
    data = pd.read_excel(f"{ticker}_historical_prices.xlsx", index_col=0)
    data = calculate_technical_indicators(data)
    data.to_excel(f"{ticker}_technical_analysis.xlsx")

# Perform sentiment analysis
for ticker in tickers:
    data = pd.read_excel(f"{ticker}_technical_analysis.xlsx", index_col=0)
    data = perform_sentiment_analysis(data)
    # data.to_excel(f"{ticker}_sentiment_analysis.xlsx")

# Backtest trading strategy
for ticker in tickers:
    data = pd.read_excel(f"{ticker}_sentiment_analysis.xlsx", index_col=0)
    data = backtest_trading_strategy(data)
    # data.to_excel(f"{ticker}_backtest_results.xlsx")
    plot_signals(data, ticker)
