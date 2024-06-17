import credentials as cd
from fyers_apiv3.FyersWebsocket import data_ws
from fyers_apiv3 import fyersModel
import fyers_model
from fyers_model import (
    get_socket_access_token,
)  # Import the function from fyers_model.py
from strategy import (
    calculate_signals,
)
import pandas as pd
import datetime as dt

# Usage
client_id = cd.client_id
token = get_socket_access_token(client_id)


symbols = ["NSE:NIFTY50-INDEX"]
for symbol in symbols:
    data = {
        "symbol": symbol,  # add the "NSE:" prefix and "-EQ" suffix to each symbol
        "resolution": "5",
        "date_format": "1",
        "range_from": "2024-05-01",
        "range_to": "2024-06-30",
        "cont_flag": "0",
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

    data = calculate_signals(processed_data)
    print(data)


def calculate_atm_strike_price(live_data):
    # Extract the current market price from the live data
    current_market_price = live_data["ltp"]

    # Define the strike price increment
    strike_price_increment = 50

    # Calculate the ATM strike price by rounding the current market price to the nearest strike price increment
    atm_strike_price = (
        round(current_market_price / strike_price_increment) * strike_price_increment
    )

    return atm_strike_price


def onmessage(message):
    """
    Callback function to handle incoming messages from the FyersDataSocket WebSocket.

    Parameters:
        message (dict): The received message from the WebSocket.

    """
    # Parse the message to extract the live data
    live_data = message["data"]

    # Append the live data to your historical data
    historical_data.append(live_data)

    # Process the updated historical data
    processed_data = fyers_model.process_and_save_data(historical_data)

    # Calculate signals using the updated data
    signals = calculate_signals(processed_data)

    # Calculate ATM Strike price based on the live data
    atm_strike_price = calculate_atm_strike_price(live_data)
    # print(atm_strike_price)

    # Set the date and strike price
    date_str = "24620"
    # Set the target and stop loss points
    target = 20
    stop_loss = 10

    # Buy ATM Strike price for Long Call when Call_Buy_Signal is 1
    if signals["Call_Buy_Signal"] == 1:
        long_call_atm_strike_price = (
            f"NSE:NIFTY{date_str}{int(atm_strike_price.iloc[-1])}CE"
        )
        print(f"Long Call ATM Strike Price: {long_call_atm_strike_price}")
        print(f"Target: {target}")
        print(f"Stop Loss: {stop_loss}")

    # Buy ATM Strike price for Long Put when Put_Buy_Signal is 1
    if signals["Put_Buy_Signal"] == 1:
        long_put_atm_strike_price = (
            f"NSE:NIFTY{date_str}{int(atm_strike_price.iloc[-1])}PE"
        )
        print(f"Long Put ATM Strike Price: {long_put_atm_strike_price}")
        print(f"Target: {target}")
        print(f"Stop Loss: {stop_loss}")

    print(signals)
    print("Response:", message)


def onerror(message):
    """
    Callback function to handle WebSocket errors.

    Parameters:
        message (dict): The error message received from the WebSocket.


    """
    print("Error:", message)


def onclose(message):
    """
    Callback function to handle WebSocket connection close events.
    """
    print("Connection closed:", message)


def onopen():
    """
    Callback function to subscribe to data type and symbols upon WebSocket connection.

    """
    # Specify the data type and symbols you want to subscribe to
    data_type = "SymbolUpdate"

    # # Subscribe to the specified symbols and data type
    # symbols = ["NSE:NIFTY50-INDEX", "NSE:NIFTYBANK-INDEX"]
    fyers.subscribe(symbols=symbols, data_type=data_type)

    # Keep the socket running to receive real-time data
    fyers.keep_running()


# Create a FyersDataSocket instance with the provided parameters
fyers = data_ws.FyersDataSocket(
    access_token=token,  # Access token in the format "appid:accesstoken"
    log_path="",  # Path to save logs. Leave empty to auto-create logs in the current directory.
    litemode=False,  # Lite mode disabled. Set to True if you want a lite response.
    write_to_file=False,  # Save response in a log file instead of printing it.
    reconnect=True,  # Enable auto-reconnection to WebSocket on disconnection.
    on_connect=onopen,  # Callback function to subscribe to data upon connection.
    on_close=onclose,  # Callback function to handle WebSocket connection close events.
    on_error=onerror,  # Callback function to handle WebSocket errors.
    on_message=onmessage,  # Callback function to handle incoming messages from the WebSocket.
)

# Establish a connection to the Fyers WebSocket
# fyers.connect()
