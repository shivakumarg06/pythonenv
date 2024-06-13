import pandas as pd
import numpy as np
from scipy.stats import linregress


def calculate_sma(data: pd.Series, window: int) -> pd.Series:
    """Calculate Simple Moving Average (SMA)."""
    return data.rolling(window=window).mean()


def calculate_ema(data: pd.Series, window: int) -> pd.Series:
    """Calculate Exponential Moving Average (EMA)."""
    return data.ewm(span=window, adjust=False).mean()


def calculate_rsi(data: pd.Series, window: int) -> pd.Series:
    """Calculate Relative Strength Index (RSI)."""
    delta = data.diff()
    up, down = delta.copy(), delta.copy()
    up[up < 0] = 0
    down[down > 0] = 0
    average_gain = up.rolling(window=window).mean()
    average_loss = abs(down.rolling(window=window).mean())
    rs = average_gain / average_loss
    return 100 - (100 / (1 + rs))


def calculate_stoch_rsi(rsi: pd.Series, window: int) -> pd.Series:
    """Calculate Stochastic RSI."""
    min_rsi = rsi.rolling(window=window).min()
    max_rsi = rsi.rolling(window=window).max()
    return (rsi - min_rsi) / (max_rsi - min_rsi)


def calculate_macd(data: pd.Series, short_window: int, long_window: int) -> pd.Series:
    """Calculate Moving Average Convergence Divergence (MACD)."""
    ema_short = calculate_ema(data, window=short_window)
    ema_long = calculate_ema(data, window=long_window)
    return ema_short - ema_long


def calculate_vwap(data: pd.DataFrame) -> pd.Series:
    """Calculate Volume Weighted Average Price (VWAP)."""
    vwap = np.cumsum(data["volume"] * (data["high"] + data["low"]) / 2) / np.cumsum(
        data["volume"]
    )
    return vwap
