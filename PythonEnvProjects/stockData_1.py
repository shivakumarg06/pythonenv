import pandas as pd
import numpy as np
import yfinance as yf


def download_historical_prices(tickers, start_date, end_date):
    historical_data = {}
    errors = {}
    for ticker in tickers:
        if ".NS" not in ticker:
            ticker += ".NS"
        try:
            print(f"Downloading historical data for {ticker}...")
            data = yf.download(ticker, start=start_date, end=end_date)
            # Resample to weekly data
            data = data.resample("W").last()
            historical_data[ticker] = data
        except Exception as e:
            errors[ticker] = str(e)
    return historical_data, errors


# Function to backtest trading strategy
def backtest_trading_strategy(
    historical_data, ticker, entry_threshold=60, trailing_stop_loss_percentage=0.05
):
    data = historical_data[ticker].copy()

    # Calculate weekly RSI
    data["Close_Shifted"] = data["Close"].shift(1)
    data["Change"] = data["Close"] - data["Close_Shifted"]
    data["Gain"] = np.where(data["Change"] > 0, data["Change"], 0)
    data["Loss"] = np.where(data["Change"] < 0, abs(data["Change"]), 0)
    data["Avg_Gain"] = data["Gain"].rolling(window=14).mean()
    data["Avg_Loss"] = data["Loss"].rolling(window=14).mean()
    data["RS"] = data["Avg_Gain"] / data["Avg_Loss"]
    data["RSI"] = 100 - (100 / (1 + data["RS"]))

    # Calculate previous candle high
    data["Previous_Candle_High"] = data["High"].shift(1)

    # Entry signals
    data["Entry_Signal"] = np.where(
        (data["RSI"] > entry_threshold)
        | (data["Close"] > data["Previous_Candle_High"]),
        1,
        0,
    )
    data["Exit_Signal"] = np.where(
        data["Close"] < data["Close"].rolling(window=20).mean(), -1, 0
    )

    # Update exit condition with trailing stop-loss
    highest_high = data["High"].rolling(window=20).max().shift(1)
    data["Trailing_Stop_Loss"] = highest_high * (1 - trailing_stop_loss_percentage)
    data["Exit_Signal"] = np.where(
        (data["Close"] < data["Trailing_Stop_Loss"]) | (data["Exit_Signal"] == -1),
        -1,
        0,
    )

    # Calculate trade information
    data["Position"] = data["Entry_Signal"].diff().fillna(0)
    data["Entry_Price"] = np.where(data["Position"] == 1, data["Open"], np.nan)
    data["Exit_Price"] = np.where(
        (data["Position"] == -1) | (data["Exit_Signal"] == -1), data["Open"], np.nan
    )  # Update exit price
    data["Trade_Type"] = np.where(
        data["Position"] == 1, "Buy", np.where(data["Position"] == -1, "Sell", "Hold")
    )

    return data


# Main script
if __name__ == "__main__":
    print("Starting script...")

    # Read the CSV file containing stock symbols and dates
    print("Reading CSV file...")
    stock_data = pd.read_csv(
        "Backtest Copy - WEEKLY RSI crossing 60, Technical Analysis Scanner.csv"
    )

    # Extract unique tickers from the CSV file
    print("Extracting unique tickers...")
    tickers = stock_data["symbol"].unique()

    # Download historical prices for the extracted tickers
    print("Downloading historical prices...")
    start_date = "2024-01-01"
    end_date = "2024-05-30"
    historical_data, errors = download_historical_prices(tickers, start_date, end_date)

    # Save error messages to a file
    print("Saving error messages...")
    with open("errors.txt", "w") as f:
        for ticker, error in errors.items():
            f.write(f"Error for ticker {ticker}: {error}\n")

    # Backtest trading strategy for each ticker
    print("Backtesting trading strategy...")
    backtest_results = {}
    for ticker in tickers:
        if ticker in historical_data:
            backtest_results[ticker] = backtest_trading_strategy(
                historical_data, ticker
            )
    print(f"Number of tickers with backtest results: {len(backtest_results)}")

    # Save backtest results to Excel files
    print("Saving backtest results...")
    for ticker, data in backtest_results.items():
        print(f"Saving backtest results for {ticker} to Excel file...")
        data.to_excel(f"{ticker}_backtest_results.csv", index=True)

    print("Script completed.")
