import yfinance as yf
import ta
import pandas as pd
from datetime import datetime, date

# List of stocks
stocks = [
    "360ONE.NS",
    "ADANIPORTS.NS",
    "ARE&M.NS",
    "ASHOKLEY.NS",
    "BALMLAWRIE.NS",
    "BEL.NS",
    "BEPL.NS",
    "BHEL.NS",
    "BPCL.NS",
    "CDSL.NS",
    "CENTRALBK.NS",
    "CESC.NS",
    "CHENNPETRO.NS",
    "COALINDIA.NS",
    "DIVISLAB.NS",
    "ELECTCAST.NS",
    "EQUITASBNK.NS",
    "EXIDEIND.NS",
    "GABRIEL.NS",
    "GATEWAY.NS",
    "GMRINFRA.NS",
    "GRINFRA.NS",
    "GSPL.NS",
    "HAVELLS.NS",
    "HBLPOWER.NS",
    "HFCL.NS",
    "HINDALCO.NS",
    "HINDCOPPER.NS",
    "HINDPETRO.NS",
    "HUDCO.NS",
    "IDFC.NS",
    "IEX.NS",
    "IIFLSEC.NS",
    "INDUSTOWER.NS",
    "IPCALAB.NS",
    "IRB.NS",
    "IRCON.NS",
    "IREDA.NS",
    "IRFC.NS",
    "ITC.NS",
    "IVC.NS",
    "JIOFIN.NS",
    "JUBLFOOD.NS",
    "MAFANG.NS",
    "MON100.NS",
    "MONQ50.NS",
    "MOTHERSON.NS",
    "NATIONALUM.NS",
    "NMDC.NS",
    "NTPC.NS",
    "OCCL.NS",
    "OIL.NS",
    "ONGC.NS",
    "PFC.NS",
    "PIIND.NS",
    "PNB.NS",
    "POWERGRID.NS",
    "PRICOLLTD.NS",
    "PTC.NS",
    "RCF.NS",
    "RECLTD.NS",
    "RVNL.NS",
    "SAIL.NS",
    "SJVN.NS",
    "TATACHEM.NS",
    "TATAMOTORS.NS",
    "TATAPOWER.NS",
    "TATASTEEL.NS",
    "TRIDENT.NS",
    "UNOMINDA.NS",
    "VEDL.NS",
    "YESBANK.NS",
]


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


class Trader:
    def __init__(self, initial_balance):
        self.balance = initial_balance
        self.positions = {}

    def buy(self, stock, price, quantity=1):
        self.positions[stock] = quantity
        self.balance -= price * quantity

    def sell(self, stock, price, quantity=1):
        self.positions[stock] -= quantity
        self.balance += price * quantity

    def value(self, prices):
        total_value = self.balance
        for stock, quantity in self.positions.items():
            total_value += prices[stock] * quantity
        return total_value


# Instantiate trader
trader = Trader(10000)


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


def update_output(output, stock, price, conditions, bought=False):
    # If the stock is in the DataFrame, update its row
    if stock in output["Stock"].values:
        output.loc[output["Stock"] == stock, "Current Price"] = price
        output.loc[output["Stock"] == stock, "Price Diff"] = (
            price - output.loc[output["Stock"] == stock, "Buy Price"]
        )
        buy_price = output.loc[output["Stock"] == stock, "Buy Price"].values[0]
        output.loc[output["Stock"] == stock, "Price Diff %"] = (
            (price - buy_price) / buy_price if buy_price != 0 else 0
        ) * 100
        output.loc[output["Stock"] == stock, "Short-term Condition"] = conditions[
            "short_term"
        ]
        output.loc[output["Stock"] == stock, "Long-term Condition"] = conditions[
            "long_term"
        ]
        output.loc[output["Stock"] == stock, "Bought"] = bought
    # If the stock is not in the DataFrame, create a new row for it
    else:
        new_row = {
            "Stock": stock,
            "Buy Price": price if bought else 0,
            "Current Price": price,
            "Price Diff": 0,
            "Price Diff %": 0,
            "Short-term Condition": conditions["short_term"],
            "Long-term Condition": conditions["long_term"],
            "Bought": bought,
        }
        output = output.append(new_row, ignore_index=True)
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
    # Create a row for each stock with initial values
    for stock in stocks:
        conditions = {"short_term": False, "long_term": False}
        new_row = create_new_row(stock, 0, conditions)
        output = pd.concat([output, new_row], ignore_index=True)

    for stock in stocks:
        conditions = check_conditions(stock)
        price = get_current_price(stock)
        print_conditions(stock, conditions)
        if conditions["short_term"] or conditions["long_term"]:
            print(f"Condition '{conditions}' met at: {datetime.now()}")
            if stock not in trader.positions:
                trader.buy(stock, price)
                print(f"Bought {stock} at {price}.")
                output = update_output(output, stock, price, conditions, bought=True)
            else:
                output = update_output(output, stock, price, conditions)
        elif (
            not (conditions["short_term"] or conditions["long_term"])
            and stock in trader.positions
        ):
            trader.sell(stock, price)
            print(f"Sold {stock} at {price}.")
            output = update_output(output, stock, price, conditions)
    prices = {symbol: get_current_price(symbol) for symbol in trader.positions.keys()}
    print_positions(prices, trader)
    output.to_excel(f"output_{date.today()}.xlsx")


if __name__ == "__main__":
    main()
