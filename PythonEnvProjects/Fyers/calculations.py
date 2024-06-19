import datetime, time


# Function to calculate ATM strike price based on the current market price
def calculate_atm_strike_price(current_market_price):
    strike_price_increment = 100
    atm_strike_price = (
        round(current_market_price / strike_price_increment) * strike_price_increment
    )
    return atm_strike_price


# Function to get the nearest weekly expiry date
def get_nearest_weekly_expiry():
    today = datetime.date.today()
    weekday = today.weekday()

    if weekday >= 2:  # If today is Thursday or later
        expiry = today + datetime.timedelta(days=(2 - weekday) + 7)
    else:
        expiry = today + datetime.timedelta(days=(2 - weekday))

    # Check if expiry is in the last week of the month
    if expiry.month != (expiry + datetime.timedelta(days=7)).month:
        return expiry.strftime("%y%b").upper()
    else:
        return f"{expiry.year % 100}{expiry.month}{expiry.day}"
