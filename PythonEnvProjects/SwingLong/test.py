import yfinance as yf
import ta

# List of stocks
stocks = ["AAPL", "MSFT", "GOOGL", "AMZN", "FB"]


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
        df["Close"], window_slow=24, window_fast=52, window_sign=9
    ).macd()
    df["MACD Signal"] = ta.trend.MACD(
        df["Close"], window_slow=24, window_fast=52, window_sign=9
    ).macd_signal()
    df["StochRSI"] = ta.momentum.StochRSIIndicator(
        df["Close"], window=14, smooth1=3, smooth2=3
    ).stochrsi()

    # Check conditions for the last data point
    last_row = df.iloc[-1]

    # Short-term condition
    short_term_condition = (
        last_row["EMA9"] > last_row["EMA15"]
        and last_row["MACD"] > last_row["MACD Signal"]
        and last_row["StochRSI"] < 20
    )

    # Long-term condition
    long_term_condition = (
        last_row["Close"] > last_row["EMA200"]
        and last_row["MACD"] > last_row["MACD Signal"]
        and last_row["StochRSI"] < 20
    )

    return {"short_term": short_term_condition, "long_term": long_term_condition}


# Initialize a trader
trader = PaperTrader()

# Check conditions for each stock
for stock in stocks:
    conditions = check_conditions(stock)
    price = yf.download(stock, period="1d")["Close"][0]  # Get the current price
    if conditions["short_term"] and stock not in trader.positions:
        # If the short-term conditions are met and we don't already have a position, buy the stock
        trader.buy(stock, price)
        print(f"Bought {stock} at {price}.")
    elif not conditions["long_term"] and stock in trader.positions:
        # If we have a position and the long-term conditions are not met, sell the stock
        trader.sell(stock, price)
        print(f"Sold {stock} at {price}.")

# Get the current prices for all stocks
prices = {stock: yf.download(stock, period="1d")["Close"][0] for stock in stocks}

# Print the final value
print(f"Final value: {trader.value(prices)}")
