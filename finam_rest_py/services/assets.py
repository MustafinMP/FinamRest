from datetime import datetime

from finam_rest_py.exceptions import FinamResponseFailureException
from finam_rest_py.models import Exchange, ScheduleSession, Asset, FullAsset, Option, AssetParams
from finam_rest_py.models.converters import formatted_datetime
from finam_rest_py.services.base_service import AsyncBaseService


class AssetService(AsyncBaseService):
    async def get_assets(self) -> list[Asset]:
        """Получает список доступных инструментов, их описание.

        Returns:
            list[Asset]: список доступных инструментов.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get('assets')
        if response.status_code == 200:
            return [Asset.from_dict(a) for a in response.json()['assets']]
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_all_assets(self) -> list[Asset]:
        """Получает список инструментов (в том числе архивных), их описание.

                Returns:
                    list[Asset]: список всех инструментов.

                Raises:
                    FinamResponseFailureException: если произошла ошибка запроса к серверу.
                """
        response = await self._session.get('assets/all')
        if response.status_code == 200:
            return [Asset.from_dict(a) for a in response.json()['assets']]
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_clock(self) -> datetime:
        """Получает текущее время на сервере (локализованное).

        Returns:
            datetime: время на сервере.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get('assets/clock')
        if response.status_code == 200:
            return formatted_datetime(response.json()['timestamp'])
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_exchanges(self) -> list[Exchange]:
        """Получает список доступных бирж, названия и mic коды.

        Returns:
            list[Exchange]: список доступных бирж.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get('exchanges')
        if response.status_code == 200:
            return [Exchange.from_dict(e) for e in response.json()['exchanges']]
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_asset(self, symbol: str) -> FullAsset:
        """Получает подробную информацию по конкретному инструменту.

        Args:
            symbol (str): символ инструмента в формате ticker@mic.

        Returns:
            FullAsset: подробная информация по инструменту.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get(f'assets/{symbol}',
                                           params={'symbol': symbol, 'account_id': self._account_id})
        if response.status_code == 200:
            return FullAsset.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_asset_params(self, symbol: str, account_id: str = None):
        """Получает торговые параметры по инструменту.

        Args:
            symbol (str): символ инструмента в формате ticker@mic.
            account_id (Optional[str]): ID аккаунта, по умолчанию будут использован ID текущего аккаунта.

        Returns:
            AssetParams: торговые параметры по инструменту.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        params = {'symbol': symbol, 'account_id': account_id if account_id else self._account_id}
        response = await self._session.get(f'assets/{symbol}/params', params=params)
        if response.status_code == 200:
            return AssetParams.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_options_chain(self,
                                underlying_symbol: str,
                                root: str = None,
                                expiration_date: datetime = None) -> list[Option]:
        """Получает цепочку опционов для базового актива.

        Args:
            underlying_symbol (str): символ базового инструмента в формате ticker@mic.
            root (str):
            expiration_date (datetime): дата экспирации.

        Returns:
            list[Option]: цепочка опционов.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        params = {'underlying_symbol': underlying_symbol}
        if root:
            params['root'] = root
        if expiration_date:
            params['expiration_date.year'] = expiration_date.year
            params['expiration_date.month'] = expiration_date.month
            params['expiration_date.day'] = expiration_date.day
        response = await self._session.get(f'assets/{underlying_symbol}/options', params=params)
        if response.status_code == 200:
            return [Option.from_dict(op) for op in response.json()['options']]
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_schedule(self, symbol: str, only_today=False) -> list[ScheduleSession]:
        """Получает расписание торгов для инструмента.

        Args:
            symbol (str): символ инструмента в формате ticker@mic.
            only_today (Optional[bool]): отбор только сегодняшних сессий.

        Returns:
            list[ScheduleSession]: список торговых сессий.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get(f'assets/{symbol}/schedule', params={'symbol': symbol})
        if response.status_code == 200:
            sessions = [ScheduleSession.from_dict(s) for s in response.json()['sessions']]
            if only_today:
                today = datetime.now().date()
                sessions = filter(lambda s: s.open_time.date() == today, sessions)
            return sorted(
                sessions,
                key=lambda s: s.open_time
            )
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)
