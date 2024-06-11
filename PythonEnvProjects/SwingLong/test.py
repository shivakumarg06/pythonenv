import yfinance as yf
import ta
import pandas as pd
from datetime import datetime, date


# List of stocks
stocks = ["BHEL.NS", "VEDL.NS", "RECLTD.NS", "TATASTEEL.NS", "PFC.NS"]


class PaperTrader:
    def __init__(self):
        self.cash = 10000  # Starting cash
        self.positions = {}  # Dictionary to hold the number of shares for each stock

    def buy(self, symbol, price):
        if self.cash > price:
            self.positions[symbol] = (
                self.cash // price
            )  # Buy as many shares as possible
            self.cash -= self.positions[symbol] * price  # Update cash

    def sell(self, symbol, price):
        if symbol in self.positions:
            self.cash += self.positions[symbol] * price  # Sell all shares
            del self.positions[symbol]  # Remove the position

    def value(self, prices):
        return self.cash + sum(
            self.positions[symbol] * price for symbol, price in prices.items()
        )  # Total value of cash and positions


def check_conditions(symbol):
    # Download historical data as dataframe
    df = yf.download(symbol, period="1y")

    # Calculate indicators
    df["EMA9"] = ta.trend.ema_indicator(df["Close"], window=9)
    df["EMA15"] = ta.trend.ema_indicator(df["Close"], window=15)
    df["EMA200"] = ta.trend.ema_indicator(df["Close"], window=200)
    df["MACD"] = ta.trend.MACD(
        df["Close"], window_slow=26, window_fast=52, window_sign=9
    ).macd()
    df["MACD Signal"] = ta.trend.MACD(
        df["Close"], window_slow=26, window_fast=52, window_sign=9
    ).macd_signal()

    # Calculate RSI
    df["lengthRSI"] = ta.momentum.rsi(df["Close"], window=140)

    # Calculate Stochastic values of RSI
    df["lengthStoch"] = ta.momentum.stoch(
        df["lengthRSI"], df["lengthRSI"], df["lengthRSI"], window=140
    )

    # Smooth the Stochastic values with a Simple Moving Average
    df["smoothK"] = ta.trend.sma_indicator(df["lengthStoch"], window=30)

    # Smooth the SmoothK values with a Simple Moving Average to get the final StochRSI values
    df["smoothD"] = ta.trend.sma_indicator(df["smoothK"], window=30)

    # Check conditions for the last data point
    last_row = df.iloc[-1]

    # Short-term condition
    short_term_condition = (
        last_row["EMA9"] > last_row["EMA15"]
        and last_row["MACD"] > last_row["MACD Signal"]
        and last_row["smoothK"] > last_row["smoothD"]
    )

    # Long-term condition
    long_term_condition = (
        last_row["Close"] > last_row["EMA200"]
        and last_row["EMA9"] > last_row["EMA15"]
        and last_row["MACD"] > last_row["MACD Signal"]
        and last_row["smoothK"] > last_row["smoothD"]
    )

    return {"short_term": short_term_condition, "long_term": long_term_condition}


# Initialize a trader
trader = PaperTrader()

# Initialize output DataFrame with the same columns as new_row DataFrame
output = pd.DataFrame(
    columns=[
        "Date",
        "Stock",
        "Bought",
        "Buy Price",
        "Current Price",
        "Price Diff",
        "Price Diff %",
        "Short-term Condition",
        "Long-term Condition",
    ]
)


# Check conditions for each stock
for stock in stocks:
    conditions = check_conditions(stock)
    price = yf.download(stock, period="1d")["Close"].iloc[0]  # Get the current price
    # Print the conditions
    print(f"Conditions for {stock}:")
    print(f"  Short-term: {conditions['short_term']}")
    print(f"  Long-term: {conditions['long_term']}")
    if conditions["short_term"] or conditions["long_term"]:
        print(f"Condition '{conditions}' met at: {datetime.now()}")
        # If the short-term conditions are met and we don't already have a position, buy the stock
        if stock not in trader.positions:
            trader.buy(stock, price)
            print(f"Bought {stock} at {price}.")
            new_row = pd.DataFrame(
                {
                    "Date": [datetime.now()],
                    "Stock": [stock],
                    "Bought": [True],
                    "Buy Price": [price],
                    "Current Price": [price],
                    "Price Diff": [0],
                    "Price Diff %": [0],
                    "Short-term Condition": [conditions["short_term"]],
                    "Long-term Condition": [conditions["long_term"]],
                }
            )
        else:
            # If the DataFrame is empty, set "Bought" to False and fill the other fields with default values
            new_row = pd.DataFrame(
                {
                    "Date": [datetime.now()],
                    "Stock": [stock],
                    "Bought": [False],
                    "Buy Price": [0],
                    "Current Price": [price],
                    "Price Diff": [0],
                    "Price Diff %": [0],
                    "Short-term Condition": [False],
                    "Long-term Condition": [False],
                }
            )

        # Concatenate the new row with the output DataFrame
        output = pd.concat([output, new_row], ignore_index=True)

    elif (
        not (conditions["short_term"] or conditions["long_term"])
        and stock in trader.positions
    ):
        # If we have a position and the long-term conditions are not met, sell the stock
        trader.sell(stock, price)
        print(f"Sold {stock} at {price}.")
        if stock in output["Stock"].values:  # Check if the stock has been bought before
            output.loc[output["Stock"] == stock, "Current Price"] = price
            output.loc[output["Stock"] == stock, "Price Diff"] = (
                price - output.loc[output["Stock"] == stock, "Buy Price"]
            )
            output.loc[output["Stock"] == stock, "Price Diff %"] = (
                (price - output.loc[output["Stock"] == stock, "Buy Price"])
                / output.loc[output["Stock"] == stock, "Buy Price"]
            ) * 100

# Get the current prices for all stocks in positions
prices = {
    symbol: yf.download(symbol, period="1d")["Close"].iloc[0]
    for symbol in trader.positions.keys()
}

# Print the current date and time
print(f"Current date and time: {datetime.now()}")

# Print the initial value
print(f"Initial value: {trader.value(prices)}")

# Print the current prices for all stocks
for symbol, price in prices.items():
    print(f"Current price of {symbol}: {price}")

# Print the current positions
for symbol, position in trader.positions.items():
    print(f"Current position in {symbol}: {position}")

# Print the final value
print(f"Final value: {trader.value(prices)}")

# Print the final positions
for symbol, position in trader.positions.items():
    print(f"Final position in {symbol}: {position}")


# Write the output DataFrame to an Excel file
# The file name includes today's date
output.to_excel(f"output_{date.today()}.xlsx")

#####################################################################################################
#####################################################################################################
#####################################################################################################
