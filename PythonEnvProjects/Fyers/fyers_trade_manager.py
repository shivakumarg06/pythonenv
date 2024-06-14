import fyers_model
from fyers_get_orders import FyersDataFetcher

# Initialize the FyersModel instance
fyers = fyers_model.initialize_fyers_model()

# Create a FyersDataFetcher instance
fetcher = FyersDataFetcher(fyers)

# Fetch the order book, net positions, and trade book
order_df = fetcher.get_orderbook()
pos_df = fetcher.get_positions()
trade_df = fetcher.get_tradebook()

# Print the fetched data
if order_df is not None:
    print(order_df.to_string())
if pos_df is not None:
    print(pos_df.to_string())
if trade_df is not None:
    print(trade_df.to_string())
