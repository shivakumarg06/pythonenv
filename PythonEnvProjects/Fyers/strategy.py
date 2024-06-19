import pandas as pd
import numpy as np
import pandas_ta as pta
from indicators import calculate_sma
from ta.trend import EMAIndicator, MACD
from ta.momentum import StochasticOscillator
from ta.trend import ADXIndicator


def calculate_sma_crossover_signals(data, short_window=50, long_window=200):
    # Calculate the short and long simple moving averages
    data["short_sma"] = calculate_sma(data["CLOSE"], window=short_window)
    data["long_sma"] = calculate_sma(data["CLOSE"], window=long_window)

    # Create a column 'signal' such that if short-term SMA is greater than long-term SMA then signal is 1 else 0
    data["signal"] = 0.0
    data.iloc[short_window:, data.columns.get_loc("signal")] = np.where(
        data["short_sma"][short_window:] > data["long_sma"][short_window:], 1.0, 0.0
    )

    # Generate trading orders based on the signals
    data["positions"] = data["signal"].diff()

    return data


def calculate_ema_crossover_signals(data, short_window=12, long_window=26):
    # Calculate the short and long EMA
    data["short_ema"] = data["CLOSE"].ewm(span=short_window, adjust=False).mean()
    data["long_ema"] = data["CLOSE"].ewm(span=long_window, adjust=False).mean()

    # Create a column 'signal' with all zeros
    data["signal"] = 0.0

    data.iloc[short_window:, data.columns.get_loc("signal")] = np.where(
        data["short_ema"][short_window:] > data["long_ema"][short_window:], 1.0, 0.0
    )

    # Generate trading orders based on the signals
    data["positions"] = data["signal"].diff()

    return data


def calculate_rsi_with_ema_signals(
    data,
    ema_short_period=9,
    ema_long_period=15,
    rsi_period=14,
    rsi_threshold=55,
    macd_fastperiod=24,
    macd_slowperiod=52,
    macd_signalperiod=9,
):
    # Calculate the short and long EMA
    data["ema_short"] = pta.ema(data["CLOSE"], length=ema_short_period)
    data["ema_long"] = pta.ema(data["CLOSE"], length=ema_long_period)

    # Calculate 5-period EMA
    data["5_ema"] = data["CLOSE"].ewm(span=5, adjust=False).mean()

    # Calculate MACD
    macd = pta.macd(
        data["CLOSE"],
        fastperiod=macd_fastperiod,
        slowperiod=macd_slowperiod,
        signalperiod=macd_signalperiod,
    )
    # Rename the columns
    macd.columns = ["MACD_line", "Signal_line", "Histogram"]
    data = pd.concat([data, macd], axis=1)

    # Calculate RSI
    data["rsi"] = pta.rsi(data["CLOSE"], length=rsi_period)

    # Calculate volume change
    data["volume_change"] = data["VOLUME"].diff()

    # Create a new DataFrame for the signals
    signals = pd.DataFrame(index=data.index)
    signals["signal"] = 0.0

    # Assign the signals to the appropriate rows in the new DataFrame
    signals["signal"] = np.where(
        (
            (data["ema_short"] > data["ema_long"])
            & (data["rsi"] > rsi_threshold)
            & (data["MACD_line"] > data["Signal_line"])
            & (data["CLOSE"] > data["CLOSE"].rolling(window=50).mean())
        ),
        1.0,
        0.0,
    )

    # Add a condition to check if the closing price is below the 5-period EMA
    signals["exit_signal"] = np.where(data["CLOSE"] < data["5_ema"], 1, 0)

    # Merge the signals DataFrame with the original DataFrame
    data = pd.concat([data, signals], axis=1)

    # Now you should be able to calculate the positions
    data["positions"] = data["signal"].diff()

    return data


def calculate_signals(data):
    # Calculate EMAs
    data["5_EMA"] = EMAIndicator(close=data["Close"], window=5).ema_indicator()
    data["20_EMA"] = EMAIndicator(close=data["Close"], window=20).ema_indicator()

    # Calculate ADX
    adx = ADXIndicator(
        high=data["High"], low=data["Low"], close=data["Close"], window=7
    )
    data["ADX"] = adx.adx()

    # Calculate MACD
    macd = MACD(close=data["Close"], window_slow=13, window_fast=6, window_sign=5)
    data["MACD"] = macd.macd()
    data["MACD_Signal"] = macd.macd_signal()
    data["MACD_Hist"] = macd.macd_diff()

    # Calculate Stochastic RSI
    stoch = StochasticOscillator(
        high=data["High"],
        low=data["Low"],
        close=data["Close"],
        window=14,
        smooth_window=3,
    )
    data["Stoch_RSI"] = stoch.stoch()
    data["Stoch_RSI_Signal"] = stoch.stoch_signal()

    # Generate buy signals for long calls (CE)
    data["Call_Buy_Signal"] = np.where(
        (data["5_EMA"] > data["20_EMA"])
        & (data["MACD"] > data["MACD_Signal"])
        & (data["Stoch_RSI"] > 20)
        & (data["Stoch_RSI"] < 80)
        & (data["Stoch_RSI"] > data["Stoch_RSI_Signal"])
        & (data["ADX"] > 25),
        1,
        0,
    )

    # Generate buy signals for long puts (PE)
    data["Put_Buy_Signal"] = np.where(
        (data["5_EMA"] < data["20_EMA"])
        & (data["MACD"] < data["MACD_Signal"])
        & (data["Stoch_RSI"] < 80)
        & (data["Stoch_RSI"] > 20)
        & (data["Stoch_RSI"] < data["Stoch_RSI_Signal"])
        & (data["ADX"] > 25),
        1,
        0,
    )
    return data  # data = calculate_signals(data)
