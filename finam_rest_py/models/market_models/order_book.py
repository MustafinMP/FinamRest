from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Optional

from finam_rest_py.models.converters import formatted_datetime


class Action(Enum):
    ACTION_UNSPECIFIED = 0  # Действие не указано
    ACTION_REMOVE = 1  # Удалить
    ACTION_ADD = 2  # Добавить
    ACTION_UPDATE = 3  # Обновить

    @classmethod
    def from_str(cls, string: str) -> Action:
        match string:
            case 'ACTION_UNSPECIFIED': return cls.ACTION_UNSPECIFIED
            case 'ACTION_REMOVE': return cls.ACTION_REMOVE
            case 'ACTION_ADD': return cls.ACTION_ADD
            case 'ACTION_UPDATE': return cls.ACTION_UPDATE
            case _: return cls.ACTION_UNSPECIFIED


@dataclass
class OrderBookRow:
    price: float
    sell_size: float
    buy_size: float
    action: Action
    mpid: Optional[str]
    datetime: datetime

    @classmethod
    def from_rest_dict(cls, row_dict: dict) -> OrderBookRow:
        return OrderBookRow(
            price=float(row_dict['price']['value']),
            sell_size=float(row_dict['sell_size']['value']) if 'sell_size' in row_dict else 0,
            buy_size=float(row_dict['buy_size']['value']) if 'buy_size' in row_dict else 0,
            action=Action.from_str(row_dict['action']),
            mpid=row_dict['mpid'],
            datetime=formatted_datetime(row_dict['timestamp'])
        )

    @classmethod
    def from_ws_dict(cls, row_dict: dict) -> OrderBookRow:
        return OrderBookRow(
            price=float(row_dict['price']['value']),
            sell_size=float(row_dict['sellSize']['value']) if 'sellSize' in row_dict else 0,
            buy_size=float(row_dict['buySize']['value']) if 'buySize' in row_dict else 0,
            action=Action.from_str(row_dict['action']),
            mpid=row_dict['mpid'] if 'mpid' in row_dict.keys() else None,
            datetime=formatted_datetime(row_dict['timestamp'])
        )


@dataclass
class OrderBook:
    symbol: str
    orderbook: list[OrderBookRow]

    @classmethod
    def from_rest_dict(cls, order_book_dict: dict) -> OrderBook:
        return OrderBook(
            symbol=order_book_dict['symbol'],
            orderbook=[OrderBookRow.from_rest_dict(r) for r in order_book_dict['orderbook']['rows']]
        )

    @classmethod
    def from_ws_dict(cls, order_book_dict: dict) -> OrderBook:
        return OrderBook(
            symbol=order_book_dict['symbol'],
            orderbook=[OrderBookRow.from_ws_dict(r) for r in order_book_dict['rows']]
        )