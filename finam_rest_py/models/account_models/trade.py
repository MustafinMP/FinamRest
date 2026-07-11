from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from finam_rest_py.models.converters import formatted_datetime
from finam_rest_py.models.trade_side import TradeSide


@dataclass
class Trade:
    trade_id: str
    symbol: str
    price: float
    size: float
    side: TradeSide
    timestamp: datetime
    order_id: str
    account_id: str

    @classmethod
    def from_dict(cls, response_dict: dict) -> Trade:
        return Trade(
            trade_id=response_dict['trade_id'] if 'trade_id' in response_dict else response_dict['tradeId'],
            symbol=response_dict['symbol'],
            price=float(response_dict['price']['value']),
            size=float(response_dict['size']['value']),
            side=TradeSide.from_str(response_dict['side']),
            timestamp=formatted_datetime(response_dict['timestamp']),
            order_id=response_dict['order_id'] if 'order_id' in response_dict else response_dict['orderId'],
            account_id=response_dict['account_id'] if 'account_id' in response_dict else response_dict['accountId']
        )

