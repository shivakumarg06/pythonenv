# Import Fyers API credentials
import credentials as cd

# Importing the required libraries and modules from the custom wrote files
import fyers_model
from fyers_model import (
    get_socket_access_token,
)  # Import the function from fyers_model.py
from fyers_execute_orders import place_bracket_order
from calculations import (
    calculate_atm_strike_price,
    get_nearest_weekly_expiry,
)
from strategy import (
    calculate_signals,
)

# Importing the required libraries
import pandas as pd
import datetime, time
from fyers_apiv3.FyersWebsocket import data_ws
from fyers_apiv3 import fyersModel


# Global variables
CLIENT_ID = cd.client_id
TARGET = 50
STOP_LOSS = 20
SYMBOLS = ["NSE:NIFTYBANK-INDEX"]
OPTIONS_STRING = "NSE:BANKNIFTY"

# Usage
token = get_socket_access_token(CLIENT_ID)


# Initialize the FyersModel instance
fyers = fyers_model.initialize_fyers_model()


# while True:
for symbol in SYMBOLS:
    data = {
        "symbol": symbol,  # add the "NSE:" prefix and "-EQ" suffix to each symbol
        "resolution": "5",
        "date_format": "1",
        "range_from": "2024-05-01",
        "range_to": "2024-06-30",
        "cont_flag": "1",
    }
    # Initialize historical_data
    historical_data = fyers_model.initialize_fyersApi_historical_data(data)
    if historical_data is None:
        print(f"Could not fetch historical data for symbol: {symbol}")
        continue
    # print(historical_data)

    # Process and save historical_data
    processed_data = fyers_model.process_and_save_data(historical_data)
    if processed_data is None:
        print(f"Could not process and save data for symbol: {symbol}")
        continue
    # print(processed_data)

    # Calculate trading signals
    data = calculate_signals(processed_data)
    # print(data)

    # Calculate ATM strike price based on the latest closing price
    current_market_price = data["Close"].iloc[-1]
    atm_strike_price = calculate_atm_strike_price(current_market_price)
    nearest_expiry = get_nearest_weekly_expiry()

    # Check for buy signals and execute trades
    if data["Call_Buy_Signal"].iloc[-1] == 1:
        long_call_atm_strike_price = (
            f"{OPTIONS_STRING}{nearest_expiry}{int(atm_strike_price)}CE"
        )
        long_call_target = current_market_price + TARGET
        long_call_stop_loss = current_market_price - STOP_LOSS
        print(
            f"Call Buy Signal Generated. Placing order for {long_call_atm_strike_price}. Target: {long_call_target}, Stop Loss: {long_call_stop_loss}"
        )

        # Place order for Call Option
        order_details = {
            "symbol": long_call_atm_strike_price,
            "qty": 15,
            "type": 2,
            "side": 1,
            "productType": "BO",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": False,
            "stopLoss": 10,
            "takeProfit": 30,
        }
        place_bracket_order(fyers, order_details)

    if data["Put_Buy_Signal"].iloc[-1] == 1:
        long_put_atm_strike_price = (
            f"{OPTIONS_STRING}{nearest_expiry}{int(atm_strike_price)}PE"
        )
        long_put_target = current_market_price - TARGET
        long_put_stop_loss = current_market_price + STOP_LOSS
        print(
            f"Put Buy Signal Generated. Placing order for {long_put_atm_strike_price}. Target: {long_put_target}, Stop Loss: {long_put_stop_loss}"
        )

        # Place order for Call Option
        order_details = {
            "symbol": long_put_atm_strike_price,
            "qty": 15,
            "type": 2,
            "side": 1,
            "productType": "BO",
            "limitPrice": 0,
            "stopPrice": 0,
            "validity": "DAY",
            "disclosedQty": 0,
            "offlineOrder": False,
            "stopLoss": STOP_LOSS,
            "takeProfit": TARGET,
        }
        place_bracket_order(fyers, order_details)

    # Save the data with signals to a CSV file
    data.to_csv("signals.csv", index=True)
    # print(data)

# def onmessage(message):
#     """
#     Callback function to handle incoming messages from the FyersDataSocket WebSocket.

#     Parameters:
#         message (dict): The received message from the WebSocket.

#     """
#     # Parse the message to extract the live data
#     live_data = message["message"]

#     # Process the updated historical data
#     processed_data = fyers_model.process_and_save_data(historical_data)

#     # Calculate signals using the updated data
#     signals = calculate_signals(processed_data)

#     # Calculate ATM Strike price based on the live data
#     atm_strike_price = calculate_atm_strike_price(live_data)
#     # print(atm_strike_price)

#     # Set the date and strike price
#     date_str = "24620"
#     # Set the target and stop loss points
#     target = 20
#     stop_loss = 10

#     # Buy ATM Strike price for Long Call when Call_Buy_Signal is 1
#     if signals["Call_Buy_Signal"] == 1:
#         long_call_atm_strike_price = (
#             f"NSE:NIFTY{date_str}{int(atm_strike_price.iloc[-1])}CE"
#         )
#         print(f"Long Call ATM Strike Price: {long_call_atm_strike_price}")
#         print(f"Target: {target}")
#         print(f"Stop Loss: {stop_loss}")

#     # Buy ATM Strike price for Long Put when Put_Buy_Signal is 1
#     if signals["Put_Buy_Signal"] == 1:
#         long_put_atm_strike_price = (
#             f"NSE:NIFTY{date_str}{int(atm_strike_price.iloc[-1])}PE"
#         )
#         print(f"Long Put ATM Strike Price: {long_put_atm_strike_price}")
#         print(f"Target: {target}")
#         print(f"Stop Loss: {stop_loss}")

#     print(signals)
#     print("Response:", message)


# def onerror(message):
#     """
#     Callback function to handle WebSocket errors.

#     Parameters:
#         message (dict): The error message received from the WebSocket.


#     """
#     print("Error:", message)


# def onclose(message):
#     """
#     Callback function to handle WebSocket connection close events.
#     """
#     print("Connection closed:", message)


# def onopen():
#     """
#     Callback function to subscribe to data type and symbols upon WebSocket connection.

#     """
#     # Specify the data type and symbols you want to subscribe to
#     data_type = "SymbolUpdate"

#     # # Subscribe to the specified symbols and data type
#     # symbols = ["NSE:NIFTY50-INDEX", "NSE:NIFTYBANK-INDEX"]
#     fyers.subscribe(symbols=symbols, data_type=data_type)

#     # Keep the socket running to receive real-time data
#     fyers.keep_running()


# # Create a FyersDataSocket instance with the provided parameters
# fyers = data_ws.FyersDataSocket(
#     access_token=token,  # Access token in the format "appid:accesstoken"
#     log_path="",  # Path to save logs. Leave empty to auto-create logs in the current directory.
#     litemode=False,  # Lite mode disabled. Set to True if you want a lite response.
#     write_to_file=False,  # Save response in a log file instead of printing it.
#     reconnect=True,  # Enable auto-reconnection to WebSocket on disconnection.
#     on_connect=onopen,  # Callback function to subscribe to data upon connection.
#     on_close=onclose,  # Callback function to handle WebSocket connection close events.
#     on_error=onerror,  # Callback function to handle WebSocket errors.
#     on_message=onmessage,  # Callback function to handle incoming messages from the WebSocket.
# )

# # Establish a connection to the Fyers WebSocket
# fyers.connect()
