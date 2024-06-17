def place_market_order(fyers, order_details):
    default_order = {
        "symbol": "NSE:HATHWAY-EQ",
        "qty": 1,
        "type": 2,
        "side": 1,
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "stopLoss": 0,
        "takeProfit": 0,
        "offlineOrder": False,
        "disclosedQty": 0,
    }

    # Update default values with user-provided values
    order = {**default_order, **order_details}

    try:
        response = fyers.place_order(data=order)
        if response["code"] == 200:
            print(f"Market Order placed successfully: {response['order']}")
        else:
            print(f"Error placing Market order: {response['message']}")
    except Exception as e:
        print(f"Error placing Market order: {e}")


def place_cnc_market_order(fyers, order_details):
    default_order = {
        "symbol": "NSE:YESBANK-EQ",
        "qty": 1,
        "type": 2,
        "side": 1,
        "productType": "CNC",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "stopLoss": 0,
        "takeProfit": 0,
        "offlineOrder": False,
        "disclosedQty": 0,
    }

    # Update default values with user-provided values
    order = {**default_order, **order_details}

    try:
        response = fyers.place_order(data=order)
        if response["code"] == 200:
            print(f"CNC Order placed successfully: {response['order']}")
        else:
            print(f"Error placing CNC order: {response['message']}")
    except Exception as e:
        print(f"Error placing CNC order: {e}")


def place_limit_order(fyers, order_details):
    default_order = {
        "symbol": "NSE:NTPC-EQ",
        "qty": 1,
        "type": 1,
        "side": 1,
        "productType": "INTRADAY",
        "limitPrice": 333,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        "orderTag": "tag1",
    }

    # Update default values with user-provided values
    order = {**default_order, **order_details}

    try:
        response = fyers.place_order(data=order)
        if response["code"] == 200:
            print(f"Limit Order placed successfully: {response['order']}")
        else:
            print(f"Error placing Limit order: {response['message']}")
    except Exception as e:
        print(f"Error placing Limit order: {e}")


def place_stop_order(fyers, order_details):
    default_order = {
        "symbol": "NSE:HATHWAY-EQ",
        "qty": 1,
        "type": 3,
        "side": -1,
        "productType": "INTRADAY",
        "limitPrice": 0,
        "stopPrice": 22,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        "orderTag": "tag1",
    }

    # Update default values with user-provided values
    order = {**default_order, **order_details}

    try:
        response = fyers.place_order(data=order)
        if response["code"] == 200:
            print(f"Stop Order placed successfully: {response['order']}")
        else:
            print(f"Error placing Stop order: {response['message']}")
    except Exception as e:
        print(f"Error placing Stop order: {e}")


def place_stop_limit_order(fyers, order_details):
    default_order = {
        "symbol": "NSE:HATHWAY-EQ",
        "qty": 1,
        "type": 4,
        "side": -1,
        "productType": "INTRADAY",
        "limitPrice": 21,
        "stopPrice": 22,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        "orderTag": "tag1",
    }

    # Update default values with user-provided values
    order = {**default_order, **order_details}

    try:
        response = fyers.place_order(data=order)
        if response["code"] == 200:
            print(f"Stop Limit Order placed successfully: {response['order']}")
        else:
            print(f"Error placing Stop Limit order: {response['message']}")
    except Exception as e:
        print(f"Error placing Stop Limit order: {e}")


def place_cover_order(fyers, order_details):
    default_order = {
        "symbol": "NSE:ONGC-EQ",
        "qty": 1,
        "type": 2,
        "side": 1,
        "productType": "CO",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        "stopLoss": 3,
        "takeProfit": 0,
    }

    # Update default values with user-provided values
    order = {**default_order, **order_details}

    try:
        response = fyers.place_order(data=order)
        if response["code"] == 200:
            print(f"Cover Order placed successfully: {response['order']}")
        else:
            print(f"Error placing Cover order: {response['message']}")
    except Exception as e:
        print(f"Error placing Cover order: {e}")


def place_bracket_order(fyers, data):
    data = {
        "symbol": "NSE:NTPC-EQ",
        "qty": 1,
        "type": 2,
        "side": 1,
        "productType": "BO",
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        "stopLoss": 5,
        "takeProfit": 5,
    }
    try:
        response = fyers.place_order(data=data)
        if response["code"] == 200:
            print(f"Bracket Order placed successfully: {response['order']}")
        else:
            print(f"Error placing Bracket order: {response['message']}")
    except Exception as e:
        print(f"Error placing Bracket order: {e}")


def place_bracket_order_with_limit(fyers, order_details):
    default_order = {
        "symbol": "NSE:NTPC-EQ",
        "qty": 1,
        "type": 1,
        "side": 1,
        "productType": "BO",
        "limitPrice": 335,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": False,
        "stopLoss": 5,
        "takeProfit": 5,
    }

    # Update default values with user-provided values
    order = {**default_order, **order_details}

    try:
        response = fyers.place_order(data=order)
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


def modify_order(fyers, order_details):
    default_order = {"id": "24022300385686", "type": 1, "limitPrice": 332, "qty": 1}

    # Update default values with user-provided values
    order = {**default_order, **order_details}

    try:
        response = fyers.modify_order(data=order)
        if response["code"] == 200:
            print(f"Order modified successfully: {response['order']}")
        else:
            print(f"Error modifying order: {response['message']}")
    except Exception as e:
        print(f"Error modifying order: {e}")


def cancel_order(fyers, order_id):
    data = {"id": order_id}
    try:
        response = fyers.cancel_order(data=data)
        if response["code"] == 200:
            print(f"Order cancelled successfully: {response['order']}")
        else:
            print(f"Error cancelling order: {response['message']}")
    except Exception as e:
        print(f"Error cancelling order: {e}")
