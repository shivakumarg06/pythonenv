from flask import Flask, render_template
import pandas as pd
import requests
from pandas import json_normalize

app = Flask(__name__)

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

@app.route('/')
def home():
    oc = OptionChain()
    data = oc.fetch_data()
    return render_template('index.html', tables=[data.to_html(classes='data')], titles=data.columns.values)

if __name__ == "__main__":
    app.run(debug=True)