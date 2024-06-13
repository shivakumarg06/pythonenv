import credentials as cd
from fyers_apiv3 import fyersModel
import pandas as pd
import datetime as dt


def initialize_fyers_model():
    try:
        with open("F:\\GitHub\\pythonenv\\PythonEnvProjects\\access.txt", "r") as a:
            access_token = a.read()
        client_id = cd.client_id

        # Initialize the FyersModel instance with your client_id, access_token, and enable async mode
        fyers = fyersModel.FyersModel(
            client_id=client_id, is_async=False, token=access_token, log_path=""
        )

        return fyers
    except Exception as e:
        print(f"Error initializing fyers model: {e}")
        return None


def initialize_fyersApi_historical_data(data):
    try:
        fyers = initialize_fyers_model()
        response = fyers.history(data=data)
        data = response["candles"]
        historical_data = pd.DataFrame(data)
        return historical_data
    except Exception as e:
        print(f"Error initializing historical data: {e}")
        return None


def process_and_save_data(df):
    try:
        df.columns = ["DATE", "OPEN", "HIGH", "LOW", "CLOSE", "VOLUME"]
        df["DATE"] = pd.to_datetime(df["DATE"], unit="s")
        df.DATE = df.DATE.dt.tz_localize("UTC").dt.tz_convert("Asia/Kolkata")
        # print(df)
        df["DATE"] = df["DATE"].dt.tz_localize(None)
        df = df.set_index("DATE")
        df.to_csv("data.csv")
        print(dt.datetime.now())
        return df
    except Exception as e:
        print(f"Error processing and saving data: {e}")
        return None
