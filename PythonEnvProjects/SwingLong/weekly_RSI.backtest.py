import yfinance as yf
import ta
import pandas as pd


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


def process_stock_data(symbol):
    try:
        # Download historical data as dataframe
        df = yf.download(symbol, period="1y")

        # Resample the data to the weekly timeframe
        df = df.resample("W").last()

        # Calculate weekly RSI
        df["RSI"] = ta.momentum.RSIIndicator(df["Close"], window=14).rsi()

        # Calculate 20-period EMA on the weekly timeframe
        df["EMA_20"] = ta.trend.EMAIndicator(df["Close"], window=20).ema_indicator()

        # Create a column for the high of the previous candle
        df["Prev_High"] = df["High"].shift(1)

        # Create a column for the previous day's volume
        df["Prev_Volume"] = df["Volume"].shift(1)

        # Create a column to hold the signals
        df["Signal"] = 0

        # Generate signals based on the strategy
        df.loc[(df["RSI"] > 55) & (df["Volume"] > df["Prev_Volume"]), "Signal"] = (
            1  # Entry signal
        )
        # Set the buffer size (e.g., 3%)
        buffer = 0.03

        # Modify the exit condition
        df.loc[df["Close"] < df["EMA_20"] * (1 - buffer), "Signal"] = -1  # Exit signal

        # Create columns to track trades
        df["Position"] = (
            df["Signal"].replace(-1, 0).cumsum().clip(upper=1)
        )  # Long position is 1, no position is 0
        df["Entry_Price"] = df.loc[df["Signal"] == 1, "Close"]
        df["Exit_Price"] = df.loc[df["Signal"] == -1, "Close"]
        df["PnL"] = (df["Exit_Price"] - df["Entry_Price"].shift()) * df[
            "Position"
        ].shift()

        df["Stock"] = symbol

        return df
    except Exception as e:
        print(f"Failed to process data for {symbol}: {e}")
        return None


# Process each stock and write the results to a different sheet
with pd.ExcelWriter("weekly_RSI_backtest_result.xlsx", engine="xlsxwriter") as writer:
    for stock in stocks:
        stock_data = process_stock_data(stock)
        if stock_data is not None:
            stock_data.to_excel(writer, sheet_name=stock)
