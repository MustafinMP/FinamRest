from datetime import datetime

from finam_rest_py.exceptions import FinamResponseFailureException
from finam_rest_py.models import Account, Trade, Transaction
from finam_rest_py.services.base_service import AsyncBaseService


class AccountService(AsyncBaseService):
    async def get_account(self) -> Account:
        """Получает аккаунт в Finam.

        Returns:
            Account: аккаунт в Finam.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get(f'accounts/{self._account_id}')
        if response.status_code == 200:
            return Account.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_trades(self,
                         end_time: datetime,
                         start_time: datetime = None,
                         limit: int = None) -> list[Trade]:
        """Получает истории по сделкам аккаунта.

        Args:
            end_time (datetime): конец запрашиваемого периода.
            start_time (Optional[datetime]): начало запрашиваемого периода.
            limit (Optional[int]): лимит количества сделок.

        Returns:
            list[Trade]: список сделок по аккаунту.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        params = {'interval.end_time': end_time.isoformat() + 'Z'}
        if start_time:
            params['interval.start_time'] = start_time.isoformat() + 'Z'
        if limit:
            params['limit'] = limit

        response = await self._session.get(f'accounts/{self._account_id}/trades', params=params)
        if response.status_code == 200:
            return [Trade.from_dict(t) for t in response.json()['trades']]
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def transactions(self,
                           end_time: datetime,
                           start_time: datetime = None,
                           limit: int = None) -> list[Transaction]:
        """Получает список транзакций аккаунта.

        Args:
            end_time (datetime): конец запрашиваемого периода.
            start_time (Optional[datetime]): начало запрашиваемого периода.
            limit (Optional[int]): лимит количества транзакций.

        Returns:
            list[Transaction]: список транзакций аккаунта.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        params = {'interval.end_time': end_time.isoformat() + 'Z'}
        if start_time:
            params['interval.start_time'] = start_time.isoformat() + 'Z'
        if limit:
            params['limit'] = limit

        response = await self._session.get(f'accounts/{self._account_id}/transactions', params=params)
        if response.status_code == 200:
            return [Transaction.from_dict(t) for t in response.json()['transactions']]
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)
