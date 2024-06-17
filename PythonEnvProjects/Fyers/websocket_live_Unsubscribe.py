import credentials as cd
from fyers_apiv3.FyersWebsocket import data_ws
from fyers_apiv3 import fyersModel
from fyers_model import (
    get_socket_access_token,
)  # Import the function from fyers_model.py
import pandas as pd
import datetime as dt

# Usage
client_id = cd.client_id
token = get_socket_access_token(client_id)


def onmessage(message):
    """
    Callback function to handle incoming messages from the FyersDataSocket WebSocket.

    Parameters:
        message (dict): The received message from the WebSocket.

    """
    print("Response:", message)
    # After processing or when you decide to unsubscribe for specific symbol and data_type
    # you can use the fyers.unsubscribe() method

    # Example of condition: Unsubscribe when a certain condition is met
    if message["symbol"] == "NSE:SBIN-EQ" and message["ltp"] > 610:
        # Unsubscribe from the specified symbols and data type
        data_type = "SymbolUpdate"
        symbols_to_unsubscribe = ["NSE:SBIN-EQ"]
        fyers.unsubscribe(symbols=symbols_to_unsubscribe, data_type=data_type)


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

    # Subscribe to the specified symbols and data type
    symbols = ["NSE:SBIN-EQ", "NSE:ADANIENT-EQ"]
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
fyers.connect()
