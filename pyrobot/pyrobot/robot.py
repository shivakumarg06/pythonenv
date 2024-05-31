import pandas as pd

from td.client import TDClient
from td.utils import milliseconds_since_epoch

from datetime import datetime
from datetime import time
from datetime import timezone


from typing import list
from typing import dict
from typing import unio


class PyRobot:

    def __init__(
        self,
        client_id,
        str,
        redirect_uri,
        stry,
        credentails_path=None,
        trading_account: str = None,
    ) -> None:

        self.trading_account: str = trading_account
        self.client_id: str = client_id
        self.redirect_uri: str = redirect_uri
        self.credentials_path: str = credentials_path
        self.session: TDClient = self._create_session()
        self.trades: dict = {}
        self.historical_prices: dict = {}
        self.stock_frame = None

    def _create_session(self) -> TDClient:
        td_client = TDClient(
            client_id=self.client_id,
            redirect_uri=self.redirect_uri,
            credentials_path=self.credentials_path,
        )

        # Login to the session
        td_client.login()

        return td_client

    ########################################################################################################################################################################

    @property
    def pre_market_open(self) -> bool:
        pre_market_start_time = (
            datetime.now()
            .replace(hour=12, minute=00, second=00, tzinfo=timezone.utc)
            .timestamp()
        )
        market_start_time = (
            datetime.now()
            .replace(hour=13, minute=30, second=00, tzinfo=timezone.utc)
            .timestamp()
        )
        right_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        if market_start_time >= right_now >= pre_market_start_time:
            return True
        else:
            return False

    @property
    def post_market_open(self) -> bool:

        post_market_end_time = (
            datetime.now()
            .replace(hour=22, minute=30, second=00, tzinfo=timezone.utc)
            .timestamp()
        )
        market_end_time = (
            datetime.now()
            .replace(hour=20, minute=30, second=00, tzinfo=timezone.utc)
            .timestamp()
        )
        right_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        if post_market_end_time >= right_now >= market_end_time:
            return True
        else:
            return False

    @property
    def regular_market_open(self) -> bool:

        market_start_time = (
            datetime.now()
            .replace(hour=13, minute=30, second=00, tzinfo=timezone.utc)
            .timestamp()
        )
        market_end_time = (
            datetime.now()
            .replace(hour=20, minute=30, second=00, tzinfo=timezone.utc)
            .timestamp()
        )
        right_now = datetime.now().replace(tzinfo=timezone.utc).timestamp()

        if market_end_time >= right_now >= market_start_time:
            return True
        else:
            return False

    ########################################################################################################################################################################

    def create_portfolio(self, balance: float) -> dict:
        return {"balance": balance, "assets": []}

    ########################################################################################################################################################################

    def create_trade(
        self,
        trade_id: str,
        symbol: str,
        qty: int,
        side: str,
        order_type: str = "limit",
        limit_price: float = None,
        stop_price: float = None,
        status: str = "open",
    ) -> dict:
        trade = {
            "trade_id": trade_id,
            "symbol": symbol,
            "qty": qty,
            "side": side,
            "order_type": order_type,
            "limit_price": limit_price,
            "stop_price": stop_price,
            "status": status,
        }

        return trade

    ########################################################################################################################################################################

    def grab_current_quotes(self) -> dict:
        if self.trading_account:
            # Grab the current quotes
            raw_quotes = self.session.get_quotes(instruments=[self.trading_account])
        else:
            raw_quotes = self.session.get_quotes()

        quotes = {}

        for quote in raw_quotes:
            quotes[quote] = {
                "ask_price": raw_quotes[quote]["askPrice"],
                "bid_price": raw_quotes[quote]["bidPrice"],
                "last_price": raw_quotes[quote]["lastPrice"],
            }

        return quotes

    ########################################################################################################################################################################

    def grab_historical_prices(
        self,
        start: datetime,
        end: datetime,
        bar_size: int = 1,
        bar_type: str = "minute",
    ) -> dict:

        start = milliseconds_since_epoch(start)
        end = milliseconds_since_epoch(end)

        historical_prices = self.session.get_price_history(
            symbol=self.trading_account,
            period_type="day",
            start_date=start,
            end_date=end,
            frequency_type=bar_type,
            frequency=bar_size,
        )

        self.historical_prices = historical_prices

        return historical_prices

    ########################################################################################################################################################################

    def create_stock_frame(self, data: dict) -> pd.DataFrame:

        for key in data:
            self.stock_frame = pd.DataFrame(data[key])

        return self.stock_frame
