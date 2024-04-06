import requests
import pandas as pd
from pandas import json_normalize
import xlwings as xw
import time

class OptionChain():
    def __init__(self, symbol='NIFTY', timeout=5) -> None:
        self.__url = "https://www.nseindia.com/api/option-chain-indices?symbol={}".format(symbol)
        self.__session = requests.Session()
        self.__session.headers = { "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/123.0.0.0 Safari/537.36", "Accept": "*/*", "Accept-Language": "en-US,en;q=0.9" }
        self.__timeout = timeout
        self.__session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout)
    
    def fetch_data(self):
        try:
            data = self.__session.get(url=self.__url, timeout=self.__timeout)
            data = data.json()
            df = json_normalize(data['records']['data'])
            return df
        
        
        except Exception as ex:
            print('Error: {}'.format(ex))
            self.__session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout)
            return pd.DataFrame()

if __name__ == "__main__":
    oc = OptionChain()
    while True:
        data = oc.fetch_data()
        if not data.empty:
            # Open the existing workbook and clear the contents of the first sheet
            wb = xw.Book('nifty_option_chain_data.xlsx')
            sheet = wb.sheets[0]
            sheet.clear_contents()
            # Write the data to the first cell
            sheet['A1'].options(index=False).value = data
            wb.save()
            print("Data has been written to 'nifty_option_chain_data.xlsx'")
        else:
            print("The DataFrame is empty.")
        time.sleep(180)  # Wait for 3 minutes