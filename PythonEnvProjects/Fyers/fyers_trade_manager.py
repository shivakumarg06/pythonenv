import fyers_model
from fyers_get_orders import FyersDataFetcher
from fyers_execute_orders import place_market_order

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


# order_details = {
#     "symbol": "NSE:RELIANCE-EQ",
#     "qty": 10,
# }
# place_market_order(fyers, order_details)

# order_details = {
#     "symbol": "NSE:RELIANCE-EQ",
#     "qty": 10,
# }
# place_cnc_market_order(fyers, order_details)


# order_details = {
#     "symbol": "NSE:RELIANCE-EQ",
#     "qty": 10,
#     "limitPrice": 2200,
# }
# place_limit_order(fyers, order_details)

# order_details = {
#     "symbol": "NSE:RELIANCE-EQ",
#     "qty": 10,
#     "stopPrice": 2200,
# }
# place_stop_order(fyers, order_details)

# order_details = {
#     "symbol": "NSE:RELIANCE-EQ",
#     "qty": 10,
#     "limitPrice": 2200,
#     "stopPrice": 2300,
# }
# place_stop_limit_order(fyers, order_details)

# order_details = {
#     "symbol": "NSE:RELIANCE-EQ",
#     "qty": 10,
#     "stopLoss": 5,
# }
# place_cover_order(fyers, order_details)


# order_details = {
#     "symbol": "NSE:RELIANCE-EQ",
#     "qty": 10,
#     "stopLoss": 5,
#     "takeProfit": 10,
# }
# place_bracket_order(fyers, order_details)

# order_details = {
#     "symbol": "NSE:RELIANCE-EQ",
#     "qty": 10,
#     "limitPrice": 2200,
#     "stopLoss": 5,
#     "takeProfit": 10,
# }
# place_bracket_order_with_limit(fyers, order_details)

# order_details = {
#     "id": "24022300385687",
#     "limitPrice": 335,
#     "qty": 2,
# }
# modify_order(fyers, order_details)


# order_id = "24022300382793-BO-1"
# cancel_order(fyers, order_id)
