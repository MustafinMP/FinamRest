from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime

from finam_rest_py.models.converters import formatted_datetime
from finam_rest_py.models.trade_side import TradeSide


@dataclass
class AssetTrade:
    trade_id: str
    timestamp: datetime
    price: float
    size: float
    side: TradeSide

    @classmethod
    def from_dict(cls, trade_dict: dict) -> AssetTrade:
        return AssetTrade(
            trade_id=trade_dict['trade_id'] if 'trade_id' in trade_dict.keys() else trade_dict['tradeId'],
            timestamp=formatted_datetime(trade_dict['timestamp']),
            price=float(trade_dict['price']['value']),
            size=float(trade_dict['size']['value']),
            side=TradeSide.from_str(trade_dict['side'])
        )