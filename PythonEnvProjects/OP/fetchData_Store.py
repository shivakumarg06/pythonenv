import requests
import pandas as pd
import sqlite3
from pandas import json_normalize  # Corrected import statement
import time
from datetime import datetime

# Fetch data from the NSE API.
# Extract the Option Chain data, Underline_Value, and Expiry Date from the fetched data.
# Save the extracted data to a CSV file.
# Save the extracted data to a local SQLite database.


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

            # print(data)

            # Extract the Option Chain data, underlyingValue, and Expiry Date
            df = json_normalize(data['records']['data'])
            # print(df)

            # underlyingValue = data['records']['underlyingValue']
            expiry_date = data['records']['expiryDates']

            # print(underlyingValue)
            # print(expiry_date)

            # Save the extracted data to a CSV file
            df.to_csv('option_chain.csv', index=False)

            # Create a connection to the SQLite database
            conn = sqlite3.connect('data.db')

            # Save the extracted data to the SQLite database
            df.to_sql('OptionChain', conn, if_exists='append')  # Changed 'replace' to 'append'

            # Close the connection to the SQLite database
            conn.close()

            return df

        except Exception as ex:
            print('Error: {}'.format(ex))
            self.__session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout)
            return pd.DataFrame()



# Create an instance of the OptionChain class and fetch data
option_chain = OptionChain()

while True:
    current_time = datetime.now().time()  # Get the current time
    # Check if the current time is within the desired range
    if current_time >= time(9, 15) and current_time <= time(15, 30):
        option_chain.fetch_data()
    time.sleep(300)  # Pause for 300 seconds (5 minutes)