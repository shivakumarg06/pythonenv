from typing import list
from typing import dict
from typing import unio
from typing import Optional


class Portfolio:

    def __init__(self, account_nunber: Optional[str]):

        self._positions = {}
        self._positions_count = 0
        self.market_value = 0.0
        self.profit_loss = 0.0
        self.risk_tolerance = 0.0
        self.account_nunber = account_nunber

    def add_postion(
        self,
        symbol: str,
        assest_type: str,
        purchase_date: Optional[str],
        quantity: int = 0,
        purchase_price: float = 0.0,
    ) -> dict:

        self.positions[symbol] = {}
        self.positions[symbol]["symbol"] = symbol
        self.postition[symbol]["quantity"] = quantity
        self.positions[symbol]["purchase_price"] = purchase_price
        self.positions[symbol]["purchase_date"] = purchase_date
        self.positions[symbol]["assest_type"] = assest_type

        return self.positions

    ########################################################################################################################################################################

    def add_positions(self, positions: list) -> dict:

        if isinstance(positions, list):

            for position in positions:

                self.add_positions(
                    symbol=position["symbol"],
                    assest_type=position["assest_type"],
                    purchase_date=position.get("purchase_date", None),
                    purchase_price=position.get("purchase_price"),
                    quantity=position.get("quantity", 0),
                )

                return self.positions

            else:

                raise TypeError("Positions must be a list of dictionaries")

    ########################################################################################################################################################################

    def remove_position(self, symbol: str) -> tuple[bool, str]:

        if symbol in self.positions:
            del self.positions[symbol]
            return (True, "{Sybmol} was successfully removed.".format(symbol=symbol))
        else:
            return (
                False,
                "{Symbol} did not exist in the portfolio.".format(symbol=symbol),
            )

    ########################################################################################################################################################################

    def total_allocation(self):
        pass

    ########################################################################################################################################################################

    def risk_exposure(self):
        pass

    ########################################################################################################################################################################

    def total_market_value(self):
        pass

    ########################################################################################################################################################################
    def in_portfolio(self, symbol: str) -> bool:

        if symbol in self.positions:
            return True
        else:
            return False

    ########################################################################################################################################################################

    def is_profitable(self, symbol: str, current_price: float) -> bool:

        # Grab the purchase price
        purchase_price = self.positions[symbol]["purchase_price"]

        if purchase_price <= current_price:
            return True
        elif purchase_price > current_price:
            return False
