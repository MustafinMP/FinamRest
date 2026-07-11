from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from finam_rest_py.models.converters import formatted_datetime


@dataclass
class QuoteOption:
    open_interest: float  # Открытый интерес
    implied_volatility: float  # Подразумеваемая волатильность
    theoretical_price: float  # Теоретическая цена
    delta: float
    gamma: float
    theta: float
    vega: float
    rho: float

    @classmethod
    def from_dict(cls, option_dict: dict) -> QuoteOption:
        return QuoteOption(
            open_interest=float(option_dict['open_interest']['value']),
            implied_volatility=float(option_dict['implied_volatility']['value']),
            theoretical_price=float(option_dict['theoretical_price']['value']),
            delta=float(option_dict['delta']['value']),
            gamma=float(option_dict['gamma']['value']),
            theta=float(option_dict['theta']['value']),
            vega=float(option_dict['vega']['value']),
            rho=float(option_dict['rho']['value']),
        )


@dataclass
class Quote:
    symbol: str
    datetime: datetime
    ask: float  # Аск. 0 при отсутствии активного аска
    ask_size: float  # Размер аска
    bid: float  # Бид. 0 при отсутствии активного бида
    bid_size: float  # Размер бида
    last: float  # Цена последней сделки
    last_size: float  # Размер последней сделки
    volume: float  # Дневной объем сделок
    turnover: float  # Дневной оборот сделок
    open: float  # Цена открытия. Дневная
    high: float  # Максимальная цена. Дневная
    low: float  # Минимальная цена. Дневная
    close: float  # Цена закрытия. Дневная
    change: float  # Изменение цены (last минус close)
    option: Optional[QuoteOption | None]  # Информация об опционе

    @classmethod
    def from_dict(cls, quote: dict) -> Quote:
        return Quote(
            symbol=quote['symbol'] if 'symbol' in quote.keys() else '',
            datetime=formatted_datetime(quote['timestamp']),
            ask=float(quote['ask']['value']) if 'ask' in quote.keys() else 0,
            ask_size=float(quote['ask_size']['value']) if 'ask_size' in quote.keys()
            else float(quote['askSize']['value']) if 'askSize' in quote.keys() else 0,
            bid=float(quote['bid']['value']) if 'bid' in quote.keys() else 0,
            bid_size=float(quote['bid_size']['value']) if 'bid_size' in quote.keys()
            else float(quote['bidSize']['value']) if 'bidSize' in quote.keys() else 0,
            last=float(quote['last']['value']) if 'last' in quote.keys() else 0,
            last_size=float(quote['last_size']['value']) if 'last_size' in quote.keys()
            else float(quote['lastSize']['value']) if 'lastSize' in quote.keys() else 0,
            volume=float(quote['volume']['value']) if 'volume' in quote.keys() else 0,
            turnover=float(quote['turnover']['value']) if 'turnover' in quote.keys() else 0,
            open=float(quote['open']['value']) if 'open' in quote.keys() else 0,
            high=float(quote['high']['value']) if 'high' in quote.keys() else 0,
            low=float(quote['low']['value']) if 'low' in quote.keys() else 0,
            close=float(quote['close']['value']) if 'close' in quote.keys() else 0,
            change=float(quote['change']['value']) if 'change' in quote.keys() else 0,
            option=QuoteOption.from_dict(quote['option']) if 'option' in quote.keys() else None
        )
