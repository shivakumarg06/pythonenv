class Position:
    def __init__(self, symbol, entry_price, entry_time, position_type):
        self.symbol = symbol
        self.entry_price = entry_price
        self.entry_time = entry_time
        self.position_type = position_type
        self.stop_loss = None
        self.take_profit = None
        self.exit_price = None
        self.exit_time = None

    def set_stop_loss(self, stop_loss):
        self.stop_loss = stop_loss

    def set_take_profit(self, take_profit):
        self.take_profit = take_profit

    def update_exit_price(self, exit_price):
        self.exit_price = exit_price

    def update_exit_time(self, exit_time):
        self.exit_time = exit_time


class PositionManager:
    def __init__(self):
        self.open_positions = []

    def open_position(self, symbol, entry_price, entry_time, position_type):
        position = Position(symbol, entry_price, entry_time, position_type)
        self.open_positions.append(position)
        return position

    def close_position(self, position_index, exit_price, exit_time):
        position = self.open_positions[position_index]
        position.update_exit_price(exit_price)
        position.update_exit_time(exit_time)
        del self.open_positions[position_index]

    def update_stop_loss(self, position_index, stop_loss):
        position = self.open_positions[position_index]
        position.set_stop_loss(stop_loss)

    def update_take_profit(self, position_index, take_profit):
        position = self.open_positions[position_index]
        position.set_take_profit(take_profit)

    def get_open_positions(self):
        return self.open_positions


# Example usage:
if __name__ == "__main__":
    position_manager = PositionManager()

    # Opening a position
    position1 = position_manager.open_position(
        "AAPL", 150.0, "2024-05-06 09:30:00", "Long"
    )

    # Setting stop-loss and take-profit levels
    position1.set_stop_loss(145.0)
    position1.set_take_profit(160.0)

    # Closing a position
    position_manager.close_position(0, 155.0, "2024-05-06 15:30:00")

    # Getting open positions
    open_positions = position_manager.get_open_positions()
    for position in open_positions:
        print(
            f"Symbol: {position.symbol}, Entry Price: {position.entry_price}, Entry Time: {position.entry_time}, Exit Price: {position.exit_price}, Exit Time: {position.exit_time}"
        )
