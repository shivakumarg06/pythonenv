def place_market_order(fyers, data):
    data["productType"] = "INTRADAY"
    try:
        response = fyers.place_order(data=data)
        if response["code"] == 200:
            print(f"Order placed successfully: {response['order']}")
        else:
            print(f"Error placing order: {response['message']}")
    except Exception as e:
        print(f"Error placing order: {e}")


def place_cnc_market_order(fyers, data):
    data["productType"] = "CNC"
    try:
        response = fyers.place_order(data=data)
        if response["code"] == 200:
            print(f"CNC Order placed successfully: {response['order']}")
        else:
            print(f"Error placing CNC order: {response['message']}")
    except Exception as e:
        print(f"Error placing CNC order: {e}")


def place_limit_order(fyers, data):
    data["productType"] = "INTRADAY"
    data["type"] = 1  # Limit order
    try:
        response = fyers.place_order(data=data)
        if response["code"] == 200:
            print(f"Limit Order placed successfully: {response['order']}")
        else:
            print(f"Error placing Limit order: {response['message']}")
    except Exception as e:
        print(f"Error placing Limit order: {e}")


def place_stop_order(fyers, data):
    data["productType"] = "INTRADAY"
    data["type"] = 3  # Stop order
    try:
        response = fyers.place_order(data=data)
        if response["code"] == 200:
            print(f"Stop Order placed successfully: {response['order']}")
        else:
            print(f"Error placing Stop order: {response['message']}")
    except Exception as e:
        print(f"Error placing Stop order: {e}")


def place_stop_limit_order(fyers, data):
    data["productType"] = "INTRADAY"
    data["type"] = 4  # Stop limit order
    try:
        response = fyers.place_order(data=data)
        if response["code"] == 200:
            print(f"Stop Limit Order placed successfully: {response['order']}")
        else:
            print(f"Error placing Stop Limit order: {response['message']}")
    except Exception as e:
        print(f"Error placing Stop Limit order: {e}")


def place_cover_order(fyers, data):
    data["productType"] = "CO"
    data["type"] = 2  # Cover order
    try:
        response = fyers.place_order(data=data)
        if response["code"] == 200:
            print(f"Cover Order placed successfully: {response['order']}")
        else:
            print(f"Error placing Cover order: {response['message']}")
    except Exception as e:
        print(f"Error placing Cover order: {e}")


def place_bracket_order(fyers, data):
    data["productType"] = "BO"
    data["type"] = 2  # Bracket order
    try:
        response = fyers.place_order(data=data)
        if response["code"] == 200:
            print(f"Bracket Order placed successfully: {response['order']}")
        else:
            print(f"Error placing Bracket order: {response['message']}")
    except Exception as e:
        print(f"Error placing Bracket order: {e}")


def place_bracket_order_with_limit(fyers, data):
    data["productType"] = "BO"
    data["type"] = 1  # Limit order
    try:
        response = fyers.place_order(data=data)
        if response["code"] == 200:
            print(
                f"Bracket Order with limit price placed successfully: {response['order']}"
            )
        else:
            print(
                f"Error placing Bracket order with limit price: {response['message']}"
            )
    except Exception as e:
        print(f"Error placing Bracket order with limit price: {e}")


def modify_order(fyers, data):
    try:
        response = fyers.modify_order(data=data)
        if response["code"] == 200:
            print(f"Order modified successfully: {response['order']}")
        else:
            print(f"Error modifying order: {response['message']}")
    except Exception as e:
        print(f"Error modifying order: {e}")


def cancel_order(fyers, data):
    try:
        response = fyers.cancel_order(data=data)
        if response["code"] == 200:
            print(f"Order cancelled successfully: {response['order']}")
        else:
            print(f"Error cancelling order: {response['message']}")
    except Exception as e:
        print(f"Error cancelling order: {e}")
