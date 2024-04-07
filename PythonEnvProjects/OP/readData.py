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
    # print(df.columns)
    # df = df.sort_values('PE.underlyingValue')

    # Round current_price to the nearest 50
    current_price = round(current_price / 50) * 50

    # Calculate the upper and lower bounds for strikePrice
    lower_bound = current_price - number_of_rows * 50
    upper_bound = current_price + number_of_rows * 50

    # Filter the DataFrame to include only the rows where strikePrice is within the bounds
    df = df[df['strikePrice'].between(lower_bound, upper_bound)]

    # Close the connection to the SQLite database
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






   # Render the HTML template with the data and expiry dates
    return render_template('index.html', data=df.to_html(table_id='data_table'), current_price=current_price, expiry_dates=expiry_dates['expiryDate'].tolist(), zoneLevels=zoneLevels.to_html(table_id='zoneLevels'), total_open_interest=total_open_interest)

if __name__ == "__main__":
    app.run(debug=True)


