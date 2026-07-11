from __future__ import annotations

from finam_rest_py._session_manager import SessionManager
from finam_rest_py.services.account import AccountService
from finam_rest_py.services.assets import AssetService
from finam_rest_py.services.market import MarketService
from finam_rest_py.services.metrics import MetricsService
from finam_rest_py.services.order import OrderService
from finam_rest_py.services.report import ReportService
from finam_rest_py.services.stream import Stream


class Finam:
    _base_url = 'https://api.finam.ru/v1/'
    _ws_url = 'wss://api.finam.ru:443/ws'

    def __init__(self, session_manager: SessionManager, account_id: str):
        self.account = AccountService(self, session_manager)
        self.instruments = AssetService(self, session_manager)
        self.orders = OrderService(self, session_manager)
        self.market = MarketService(self, session_manager)
        self.metrics = MetricsService(self, session_manager)
        self.report = ReportService(self, session_manager)
        self.streams = Stream(self._ws_url, self, session_manager)

        self._account_id = account_id

    @classmethod
    async def create(cls, user_token: str, account_id: str) -> Finam:
        """Инициализация модуля.

        Args:
            user_token (str): API токен пользователя.
            account_id (str): ID счета пользователя.

        Returns:
            Finam: объект для работы с API.
        """
        finam = Finam(await SessionManager.create(cls._base_url, user_token), account_id)
        return finam

    def set_account(self, account_id: str) -> None:
        """Переключает аккаунт пользователя.

        Args:
            account_id (str): другой аккаунт пользователя.

        Returns:
            None
        """
        self._account_id = account_id

    def get_account(self) -> str:
        """Возвращает ID текущего аккаунта.

        Returns:
            str: ID текущего аккаунта.
        """
        return self._account_id
