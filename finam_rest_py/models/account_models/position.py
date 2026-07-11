from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Position:
    symbol: str
    quantity: int
    average_price: float
    current_price: float
    daily_pnl: float
    unrealized_pnl: float

    @classmethod
    def from_dict(cls, response_dict: dict) -> Position:
        return Position(
            symbol=str(response_dict['symbol']),
            quantity=int(float(response_dict['quantity']['value'])),
            average_price=float(response_dict['average_price']['value']) if 'average_price' in response_dict.keys()
            else float(response_dict['averagePrice']['value']),
            current_price=float(response_dict['current_price']['value']) if 'current_price' in response_dict.keys()
            else float(response_dict['currentPrice']['value']),
            daily_pnl=float(response_dict['daily_pnl']['value']) if 'daily_pnl' in response_dict.keys()
            else float(response_dict['dailyPnl']['value']),
            unrealized_pnl=float(response_dict['unrealized_pnl']['value']) if 'unrealized_pnl' in response_dict.keys()
            else float(response_dict['unrealizedPnl']['value'])
        )
