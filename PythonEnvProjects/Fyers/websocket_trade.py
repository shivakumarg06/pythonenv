import credentials as cd
from fyers_apiv3.FyersWebsocket import order_ws
from fyers_apiv3 import fyersModel
from fyers_model import (
    get_socket_access_token,
)  # Import the function from fyers_model.py
import pandas as pd
import datetime as dt

# Usage
client_id = cd.client_id
token = get_socket_access_token(client_id)


def onTrade(message):
    """
    Callback function to handle incoming messages from the FyersDataSocket WebSocket.

    Parameters:
        message (dict): The received message from the WebSocket.

    """
    print("Trade Response:", message)


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
    data_type = "OnTrades"

    # data_type = "OnOrders"
    # data_type = "OnPositions"
    # data_type = "OnGeneral"
    # data_type = "OnOrders,OnTrades,OnPositions,OnGeneral"

    fyers.subscribe(data_type=data_type)

    # Keep the socket running to receive real-time data
    fyers.keep_running()


# Create a FyersDataSocket instance with the provided parameters
fyers = order_ws.FyersOrderSocket(
    access_token=token,  # Your access token for authenticating with the Fyers API.
    write_to_file=False,  # A boolean flag indicating whether to write data to a log file or not.
    log_path="",  # The path to the log file if write_to_file is set to True (empty string means current directory).
    on_connect=onopen,  # Callback function to be executed upon successful WebSocket connection.
    on_close=onclose,  # Callback function to be executed when the WebSocket connection is closed.
    on_error=onerror,  # Callback function to handle any WebSocket errors that may occur.
    on_trades=onTrade,  # Callback function to handle trade-related events from the WebSocket.
)


# Establish a connection to the Fyers WebSocket
fyers.connect()
