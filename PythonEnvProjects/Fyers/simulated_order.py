# simulated_order.py


def simulate_order(symbol, qty, side, order_type, product_type):
    # Define the order details
    order = {
        "symbol": symbol,
        "qty": qty,
        "side": side,
        "orderType": order_type,
        "productType": product_type,
        "limitPrice": 0,
        "stopPrice": 0,
        "validity": "DAY",
        "disclosedQty": 0,
        "offlineOrder": "False",
        "stopLoss": 0,
        "takeProfit": 0,
    }

    # Print the order instead of executing it
    print(f"Simulated order: {order}")
