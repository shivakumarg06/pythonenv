from flask import Flask, render_template
import sqlite3
import pandas as pd



import sqlite3
import pandas as pd

# Create a connection to the SQLite database
conn = sqlite3.connect('data.db')


# Fetch the underline value
underline_value = pd.read_sql_query("SELECT underline_value FROM MarketData", conn).iloc[0, 0]


# Execute a SQL query and read the result into a DataFrame
df = pd.read_sql_query("SELECT * FROM OptionChain", conn)


# Close the connection to the SQLite database
conn.close()



app = Flask(__name__)

@app.route('/')
def home():
    # Number of records per page
    records_per_page = 10

    # Create a connection to the SQLite database
    conn = sqlite3.connect('data.db')

    # Fetch the underline value
    underline_value = pd.read_sql_query("SELECT underline_value FROM MarketData", conn).iloc[0, 0]

    # Execute a SQL query and read the result into a DataFrame
    df = pd.read_sql_query("SELECT * FROM OptionChain", conn)

    # Calculate the total number of pages
    total_pages = (len(df) - 1) // records_per_page + 1

    # Close the connection to the SQLite database
    conn.close()

    return render_template('index.html', tables=[df.to_html(classes='data')], titles=df.columns.values, total_pages=total_pages, underline_value=underline_value)

if __name__ == "__main__":
    app.run(debug=True)
