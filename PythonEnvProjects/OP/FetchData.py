def fetch_data(self):
    try:
        response = self.__session.get(url=self.__url, timeout=self.__timeout)
        response.raise_for_status()  # Raise an exception if the API request fails
        data = response.json()

        if 'records' in data and 'data' in data['records'] and data['records']['data']:
            df = json_normalize(data['records']['data'])

            # Create a connection to the SQLite database
            conn = sqlite3.connect('data.db')

            # Save the DataFrame to the SQLite database as a table named 'OptionChain'
            df.to_sql('OptionChain', conn, if_exists='replace')

            # Close the connection to the SQLite database
            conn.close()

            return df
        else:
            print('No data returned from the API')
            return pd.DataFrame()

    except Exception as ex:
        print('Error: {}'.format(ex))
        self.__session.get("https://www.nseindia.com/option-chain", timeout=self.__timeout)
        return pd.DataFrame()