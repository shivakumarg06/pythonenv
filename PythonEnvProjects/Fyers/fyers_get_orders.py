import credentials as cd
from fyers_apiv3 import fyersModel
import pandas as pd
import datetime as dt


class FyersDataFetcher:
    def __init__(self, fyers):
        self.fyers = fyers

    def get_orderbook(fyers):
        try:
            # Fetch the order book
            response = fyers.orderbook()

            # Check if the request was successful
            if response["code"] == 200:
                # Convert the order book to a DataFrame
                order_df = pd.DataFrame(response["orderBook"])

                return order_df
            else:
                print(f"Error fetching order book: {response['message']}")
                return None
        except Exception as e:
            print(f"Error fetching order book: {e}")
            return None

    def get_positions(fyers):
        try:
            # Fetch the net positions
            response = fyers.positions()

            # Check if the request was successful
            if response["code"] == 200:
                # Convert the net positions to a DataFrame
                pos_df = pd.DataFrame(response["netPositions"])

                return pos_df
            else:
                print(f"Error fetching net positions: {response['message']}")
                return None
        except Exception as e:
            print(f"Error fetching net positions: {e}")
            return None

    def get_tradebook(fyers):
        try:
            # Fetch the trade book
            response = fyers.tradebook()

            # Check if the request was successful
            if response["code"] == 200:
                # Convert the trade book to a DataFrame
                trade_df = pd.DataFrame(response["tradeBook"])

                return trade_df
            else:
                print(f"Error fetching trade book: {response['message']}")
                return None
        except Exception as e:
            print(f"Error fetching trade book: {e}")
            return None
