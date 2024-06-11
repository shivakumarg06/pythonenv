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


def calculate_indicators(df):
    df["EMA9"] = ta.trend.ema_indicator(df["Close"], window=9)
    df["EMA15"] = ta.trend.ema_indicator(df["Close"], window=15)
    df["EMA200"] = ta.trend.ema_indicator(df["Close"], window=200)
    df["MACD"] = ta.trend.MACD(
        df["Close"], window_slow=52, window_fast=24, window_sign=9
    ).macd()
    df["MACD Signal"] = ta.trend.MACD(
        df["Close"], window_slow=52, window_fast=24, window_sign=9
    ).macd_signal()
    return df


def check_conditions(symbol):
    df = yf.download(symbol, period="1y")
    df = calculate_indicators(df)
    last_row = df.iloc[-1]
    short_term_condition = (
        last_row["EMA9"] > last_row["EMA15"]
        and last_row["MACD"] > last_row["MACD Signal"]
        # and last_row["smoothK"] > last_row["smoothD"]
    )
    long_term_condition = (
        last_row["Close"] > last_row["EMA200"]
        and last_row["EMA9"] > last_row["EMA15"]
        and last_row["MACD"] > last_row["MACD Signal"]
        # and last_row["smoothK"] > last_row["smoothD"]
    )
    return {"short_term": short_term_condition, "long_term": long_term_condition}


def get_current_price(symbol):
    return yf.download(symbol, period="1d")["Close"].iloc[0]


def print_conditions(symbol, conditions):
    print(f"Conditions for {symbol}:")
    print(f"  Short-term: {conditions['short_term']}")
    print(f"  Long-term: {conditions['long_term']}")


def create_new_row(stock, price, conditions, bought=False):
    return pd.DataFrame(
        {
            "Date": [datetime.now()],
            "Stock": [stock],
            "Bought": [bought],
            "Buy Price": [price if bought else 0],
            "Current Price": [price],
            "Price Diff": [0],
            "Price Diff %": [0],
            "Short-term Condition": [conditions["short_term"]],
            "Long-term Condition": [conditions["long_term"]],
        }
    )


def update_output(output, stock, price):
    if stock in output["Stock"].values:  # Check if the stock has been bought before
        output.loc[output["Stock"] == stock, "Current Price"] = price
        output.loc[output["Stock"] == stock, "Price Diff"] = (
            price - output.loc[output["Stock"] == stock, "Buy Price"]
        )
        output.loc[output["Stock"] == stock, "Price Diff %"] = (
            (price - output.loc[output["Stock"] == stock, "Buy Price"])
            / output.loc[output["Stock"] == stock, "Buy Price"]
        ) * 100
    return output


def print_positions(prices, trader):
    print(f"Current date and time: {datetime.now()}")
    print(f"Initial value: {trader.value(prices)}")
    for symbol, price in prices.items():
        print(f"Current price of {symbol}: {price}")
    for symbol, position in trader.positions.items():
        print(f"Current position in {symbol}: {position}")
    print(f"Final value: {trader.value(prices)}")
    for symbol, position in trader.positions.items():
        print(f"Final position in {symbol}: {position}")


def main():
    trader = PaperTrader()
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
    for stock in stocks:
        conditions = check_conditions(stock)
        price = get_current_price(stock)
        print_conditions(stock, conditions)
        if conditions["short_term"] or conditions["long_term"]:
            print(f"Condition '{conditions}' met at: {datetime.now()}")
            if stock not in trader.positions:
                trader.buy(stock, price)
                print(f"Bought {stock} at {price}.")
                new_row = create_new_row(stock, price, conditions, bought=True)
            else:
                new_row = create_new_row(stock, price, conditions)
            output = pd.concat([output, new_row], ignore_index=True)
        elif (
            not (conditions["short_term"] or conditions["long_term"])
            and stock in trader.positions
        ):
            trader.sell(stock, price)
            print(f"Sold {stock} at {price}.")
            output = update_output(output, stock, price)
    prices = {symbol: get_current_price(symbol) for symbol in trader.positions.keys()}
    print_positions(prices, trader)
    output.to_excel(f"output_{date.today()}.xlsx")


if __name__ == "__main__":
    main()
