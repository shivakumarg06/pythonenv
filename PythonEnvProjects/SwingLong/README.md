# My Custom Strategy

This document describes the custom strategy used for trading. The strategy uses three indicators: EMA (Exponential Moving Average), MACD (Moving Average Convergence Divergence), and Stoch RSI (Stochastic RSI).

## Indicators

### EMA (Exponential Moving Average)

We use three EMAs with periods of 9, 15, and 200. EMAs give more weight to recent prices and are therefore more responsive to recent price changes compared to simple moving averages (SMAs).

### MACD (Moving Average Convergence Divergence)

We use MACD with parameters 24 (fast length), 52 (slow length), and 9 (signal length). The MACD line is the difference between the fast and slow EMAs, and the signal line is an EMA of the MACD line. The MACD histogram represents the difference between the MACD line and the signal line.

### Stoch RSI (Stochastic RSI)

We use Stoch RSI with parameters 140 (RSI length), 140 (Stoch length), 10 (K smoothing), and 10 (D smoothing). The Stoch RSI is an indicator of an indicator that measures the level of the RSI relative to its high-low range over a set period of time.

## Entry Conditions

1. The EMA9 crosses above the EMA15. This is a bullish signal that indicates the short-term trend is moving upwards.
2. The MACD line crosses above the signal line. This is also a bullish signal that indicates increasing upward momentum.
3. The Stoch RSI is below 20. This indicates that the asset is oversold, and there may be a potential upward price correction.

When all these conditions are met, the strategy enters a long position.

## Exit Conditions

The strategy exits the long position when the MACD line crosses below the signal line. This is a bearish signal that indicates decreasing upward momentum.

## Alerts:

Alerts are set up to notify when the conditions for a long entry or a long exit are met. These alerts can be configured in TradingView to send notifications via email, SMS, or pop-up messages.

# Note:

This strategy is a simple example and may need to be adjusted based on your specific trading strategy or requirements. Always backtest your strategies before live trading.