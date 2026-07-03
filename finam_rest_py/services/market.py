from datetime import datetime

from finam_rest_py.exceptions import FinamResponseFailureException
from finam_rest_py.models import Bar, Trade, TimeFrame, Quote, OrderBook
from finam_rest_py.services.base_service import AsyncBaseService


class MarketService(AsyncBaseService):
    async def get_bars(self,
                       symbol: str,
                       timeframe: TimeFrame | str,
                       start_time: datetime,
                       end_time: datetime) -> list[Bar]:
        """Получает свечи по инструменту в нужном таймфрейме.

        Args:
            symbol (str): символ инструмента в формате ticker@mic.
            timeframe (TimeFrame | str):
            start_time (datetime): начало запрашиваемого периода.
            end_time (datetime): конец запрашиваемого периода.

        Returns:
            list[Bar]: список свечей.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        if isinstance(timeframe, str):
            timeframe = TimeFrame.from_str(timeframe)
        if end_time - timeframe.max_deep() > start_time:
            start_time = end_time - timeframe.max_deep()
        params = {
            'symbol': symbol,
            'timeframe': timeframe.value,
            'interval.start_time': start_time.isoformat() + 'Z',
            'interval.end_time': end_time.isoformat() + 'Z'
        }
        response = await self._session.get(f'instruments/{symbol}/bars', params=params)
        if response.status_code == 401 or response.status_code == 500:
            await self._base_module.refresh_session()
            response = await self._session.get(f'instruments/{symbol}/bars', params=params)

        if response.status_code == 200:
            return [Bar.from_dict(bar) for bar in response.json()['bars']]

        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_last_quote(self, symbol: str) -> Quote:
        """Получает последнюю котировку по инструменту.

        Args:
            symbol (str): символ инструмента в формате ticker@mic.

        Returns:
            Quote: последняя котировка по инструменту.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get(f'instruments/{symbol}/quotes/latest', params={'symbol': symbol})
        if response.status_code == 401 or response.status_code == 500:
            await self._base_module.refresh_session()
            response = await self._session.get(f'instruments/{symbol}/quotes/latest', params={'symbol': symbol})

        if response.status_code == 200:
            return Quote.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_latest_trades(self, symbol: str) -> list[Trade]:
        """Получает данные о последних сделках по инструменту.

        Args:
            symbol (str): символ инструмента в формате ticker@mic.

        Returns:
            list[Trade]: список последних сделок.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get(f'instruments/{symbol}/trades/latest', params={'symbol': symbol})
        if response.status_code == 401 or response.status_code == 500:
            await self._base_module.refresh_session()
            response = await self._session.get(f'instruments/{symbol}/trades/latest', params={'symbol': symbol})

        if response.status_code == 200:
            return [Trade.from_dict(t) for t in response.json()['trades']]
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_order_book(self, symbol: str) -> OrderBook:
        """Получает книгу заявок по инструменту.

        Args:
            symbol (str): символ инструмента в формате ticker@mic.

        Returns:
            OrderBook: книга заявок.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get(f'instruments/{symbol}/orderbook', params={'symbol': symbol})
        if response.status_code == 401 or response.status_code == 500:
            await self._base_module.refresh_session()
            response = await self._session.get(f'instruments/{symbol}/orderbook', params={'symbol': symbol})

        if response.status_code == 200:
            return OrderBook.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)
