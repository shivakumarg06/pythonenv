import requests
import pandas as pd
from pandas import json_normalize

class OptionChain():
    def __init__(self, symbol='NIFTY', timeout=5) -> None:
        self.__url = "https://www.nseindia.com/api/option-chain-indices?symbol={}".format(symbol)
        self.__session = requests.Session()
        self.__session.headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9" }
        self.__timeout = timeout
        self.__session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout)
    
    def fetch_data(self, expiry_date=None, starting_strike_price=None, number_of_rows=8):
        try:
            data = self.__session.get(url=self.__url, timeout=self.__timeout)
            data = data.json()
            df = json_normalize(data['records']['data'])
            
            if expiry_date is not None:
                df = df[(df.expiryDate == expiry_date)]
            
            if starting_strike_price is not None:
                df = df[(df.strikePrice >= starting_strike_price)][:number_of_rows]
            
            return df
        
        except Exception as ex:
            print('Error: {}'.format(ex))
            self.__session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout)
            return pd.DataFrame()

if __name__ == "__main__":
    oc = OptionChain()
    data = oc.fetch_data(expiry_date='10-Apr-2024', starting_strike_price=22500)
    if not data.empty:
        print(data.iloc[0])
    else:
        print("The DataFrame is empty.")