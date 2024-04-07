from flask import Flask, render_template, request
import sqlite3
import pandas as pd

app = Flask(__name__)

@app.route('/', methods=['GET', 'POST'])
def home():
    # Get the number_of_rows parameter from the request
    number_of_rows = request.args.get('number_of_rows', default=4, type=int)


    # Connect to the SQLite database
    conn = sqlite3.connect('data.db')

    # Retrieve the unique expiry dates from the 'OptionChain' table
    expiry_dates = pd.read_sql_query("SELECT DISTINCT expiryDate FROM OptionChain", conn)

    # Retrieve the unique underlyingValue from the 'OptionChain' table
    current_price = pd.read_sql_query("""SELECT DISTINCT "PE.underlyingValue" FROM OptionChain""", conn)
    # Check if the DataFrame is not empty
    if not current_price.empty:
        # Get the first value
        current_price = current_price.iloc[0, 0]
    else:
        current_price = None  # or some default value


    # Check if current_price is a number
    if current_price is not None and pd.isna(current_price):
        current_price = None  # or some default value

    # Retrieve the data from the 'OptionChain' table
    df = pd.read_sql_query("""SELECT expiryDate, "Positions_CE", "Direction_CE", "CE.openInterest", "CE.changeinOpenInterest", "CE.impliedVolatility", "CE.lastPrice", "CE.change", "CE.impliedVolatility", "strikePrice", "PE.openInterest", "PE.changeinOpenInterest", "PE.impliedVolatility", "PE.lastPrice", "PE.change", "PE.impliedVolatility", "Direction_PE", "Positions_PE" FROM OptionChain""", conn)


    # Define the conditions for 'Direction_CE'
    def calculate_direction(row):
        if row['CE.changeinOpenInterest'] > 0 and row['CE.change'] > 0:
            return 'Bullish'
        elif row['CE.changeinOpenInterest'] > 0 and row['CE.change'] < 0:
            return 'Bearish'
        elif row['CE.changeinOpenInterest'] < 0 and row['CE.change'] > 0:
            return 'Bullish'
        elif row['CE.changeinOpenInterest'] < 0 and row['CE.change'] < 0:
            return 'Bearish'
        else:
            return 'Neutral'

    # Create the 'Direction_CE' column
    df['Direction_CE'] = df.apply(calculate_direction, axis=1)

    # Check if the 'Direction_CE' column exists
    res = conn.execute("PRAGMA table_info(OptionChain)")
    column_names = [column[1] for column in res]
    if 'Direction_CE' not in column_names:
        # Add the 'Direction_CE' column to the 'OptionChain' table
        conn.execute("ALTER TABLE OptionChain ADD COLUMN Direction_CE TEXT")

    # Update the 'Direction_CE' column in the 'OptionChain' table
    for index, row in df.iterrows():
        conn.execute(f"UPDATE OptionChain SET Direction_CE = '{row['Direction_CE']}' WHERE expiryDate = '{row['expiryDate']}' AND strikePrice = {row['strikePrice']}")

    # Define the conditions for 'Direction_PE'
    def calculate_direction_pe(row):
        if row['PE.changeinOpenInterest'] < 0 and row['PE.change'] < 0:
            return 'Bullish'
        elif row['PE.changeinOpenInterest'] < 0 and row['PE.change'] > 0:
            return 'Bearish'
        elif row['PE.changeinOpenInterest'] > 0 and row['PE.change'] < 0:
            return 'Bullish'
        elif row['PE.changeinOpenInterest'] > 0 and row['PE.change'] > 0:
            return 'Bearish'
        else:
            return 'Neutral'

    # Create the 'Direction_PE' column
    df['Direction_PE'] = df.apply(calculate_direction_pe, axis=1)

    # Check if the 'Direction_PE' column exists in the SQLite database
    res = conn.execute("PRAGMA table_info(OptionChain)")
    column_names = [column[1] for column in res]
    if 'Direction_PE' not in column_names:
        # Add the 'Direction_PE' column to the 'OptionChain' table
        conn.execute("ALTER TABLE OptionChain ADD COLUMN Direction_PE TEXT")

    # Update the 'Direction_PE' column in the 'OptionChain' table
    for index, row in df.iterrows():
        conn.execute(f"UPDATE OptionChain SET Direction_PE = '{row['Direction_PE']}' WHERE expiryDate = '{row['expiryDate']}' AND strikePrice = {row['strikePrice']}")


    # Define the conditions for 'Positions_CE'
    def calculate_positions_ce(row):
        if row['CE.changeinOpenInterest'] > 0 and row['CE.change'] > 0:
            return 'Call Buying'
        elif row['CE.changeinOpenInterest'] > 0 and row['CE.change'] < 0:
            return 'Writing'
        elif row['CE.changeinOpenInterest'] < 0 and row['CE.change'] > 0:
            return 'Short Covering'
        elif row['CE.changeinOpenInterest'] < 0 and row['CE.change'] < 0:
            return 'Call Unwinding'
        else:
            return ''

    # Create the 'Positions_CE' column
    df['Positions_CE'] = df.apply(calculate_positions_ce, axis=1)

    # Check if the 'Positions_CE' column exists in the SQLite database
    res = conn.execute("PRAGMA table_info(OptionChain)")
    column_names = [column[1] for column in res]
    if 'Positions_CE' not in column_names:
        # Add the 'Positions_CE' column to the 'OptionChain' table
        conn.execute("ALTER TABLE OptionChain ADD COLUMN Positions_CE TEXT")

    # Update the 'Positions_CE' column in the 'OptionChain' table
    for index, row in df.iterrows():
        conn.execute(f"UPDATE OptionChain SET Positions_CE = '{row['Positions_CE']}' WHERE expiryDate = '{row['expiryDate']}' AND strikePrice = {row['strikePrice']}")

    # Define the conditions for 'Positions_PE'
    def calculate_positions_pe(row):
        if row['PE.changeinOpenInterest'] < 0 and row['PE.change'] < 0:
            return 'Put Unwinding'
        elif row['PE.changeinOpenInterest'] < 0 and row['PE.change'] > 0:
            return 'Short Covering'
        elif row['PE.changeinOpenInterest'] > 0 and row['PE.change'] < 0:
            return 'Writing'
        elif row['PE.changeinOpenInterest'] > 0 and row['PE.change'] > 0:
            return 'Put Buying'
        else:
            return ''

    # Create the 'Positions_PE' column
    df['Positions_PE'] = df.apply(calculate_positions_pe, axis=1)

    # Check if the 'Positions_PE' column exists in the SQLite database
    res = conn.execute("PRAGMA table_info(OptionChain)")
    column_names = [column[1] for column in res]
    if 'Positions_PE' not in column_names:
        # Add the 'Positions_PE' column to the 'OptionChain' table
        conn.execute("ALTER TABLE OptionChain ADD COLUMN Positions_PE TEXT")

    # Update the 'Positions_PE' column in the 'OptionChain' table
    for index, row in df.iterrows():
        conn.execute(f"UPDATE OptionChain SET Positions_PE = '{row['Positions_PE']}' WHERE expiryDate = '{row['expiryDate']}' AND strikePrice = {row['strikePrice']}")


    # Round current_price to the nearest 50
    current_price_df = round(current_price / 50) * 50

    # Calculate the upper and lower bounds for strikePrice
    lower_bound = current_price_df - number_of_rows * 50
    upper_bound = current_price_df + number_of_rows * 50

    # Filter the DataFrame to include only the rows where strikePrice is within the bounds
    df = df[df['strikePrice'].between(lower_bound, upper_bound)]


    # Close the connection to the SQLite database
    conn.commit()
    conn.close()

    # Calculate the total of the 'CE.openInterest' column
    total_open_interest = df['CE.openInterest'].sum()

    # Select the highest value in the 'CE.openInterest' column
    R1 = df['CE.openInterest'].max()
    R2 = df['CE.openInterest'].nlargest(2).iloc[-1]
    R3 = df['CE.openInterest'].nlargest(3).iloc[-1]

    # Select the highest value in the 'PE.openInterest' column
    S1 = df['PE.openInterest'].max()
    S2 = df['PE.openInterest'].nlargest(2).iloc[-1]
    S3 = df['PE.openInterest'].nlargest(3).iloc[-1]

    # Create a new DataFrame with two rows and four columns
    zoneLevels = pd.DataFrame({
        'Zone': ['Resistance', 'Support'],
        '1': [R1, S1],
        '2': [R2, S2],
        '3': [R3, S3],
    })

    # Define a dictionary mapping the old column names to the new ones
    column_names = {
        "expiryDate": "Expiry",
        "Positions_CE": "Positions CE",
        "Direction_CE": "Direction CE",
        "CE.openInterest": "CE_OI",
        "CE.changeinOpenInterest": "CE_OI_C",
        "CE.impliedVolatility": "CE_IV",
        "CE.lastPrice": "CE_LTP",
        "CE.change": "CE_LTP_C",
        "strikePrice": "Strike_Price",
        "PE.openInterest": "PE_OI",
        "PE.changeinOpenInterest": "PE_OI_C",
        "PE.impliedVolatility": "PE_IV",
        "PE.lastPrice": "PE_LTP",
        "PE.change": "PE_LTP_C",
        "Direction_PE": "Direction PE",
        "Positions_PE": "Positions PE"
    }

    # Create a copy of the DataFrame with renamed columns
    df_html = df.rename(columns=column_names)
    

    # Render the HTML template with the data and expiry dates
    return render_template('index.html', data=df_html.to_html(table_id='data_table', index=False), current_price=current_price, expiry_dates=expiry_dates['expiryDate'].tolist(), zoneLevels=zoneLevels.to_html(table_id='zoneLevels', index=False), total_open_interest=total_open_interest)
    # return render_template('index.html', data=df.to_html(table_id='data_table'), current_price=current_price, expiry_dates=expiry_dates['expiryDate'].tolist(), zoneLevels=zoneLevels.to_html(table_id='zoneLevels'), total_open_interest=total_open_interest)

if __name__ == "__main__":
    app.run(debug=True)


