from __future__ import annotations

import asyncio
from typing import Optional

import httpx

from finam_rest_py.services.account import AccountService
from finam_rest_py.services.assets import AssetService
from finam_rest_py.services.market import MarketService
from finam_rest_py.services.metrics import MetricsService
from finam_rest_py.services.order import OrderService
from finam_rest_py.services.report import ReportService


class Finam:
    _base_url = 'https://api.finam.ru/v1/'
    _jwt_token_dict = dict()
    _jwt_expires_at = dict()
    _lock = None

    def __init__(self, user_token: str, account_id: str):
        self.account = AccountService(self)
        self.instruments = AssetService(self)
        self.orders = OrderService(self)
        self.market = MarketService(self)
        self.metrics = MetricsService(self)
        self.report = ReportService(self)

        self._account_id = account_id
        self._user_token = user_token

        self._session: Optional[httpx.AsyncClient] = None
        self._refresh_token_task = None

    @classmethod
    def _get_lock(cls) -> asyncio.Lock:
        """Ленивая инициализация Lock, чтобы он привязался к правильному event loop"""
        if cls._lock is None:
            cls._lock = asyncio.Lock()
        return cls._lock

    @classmethod
    async def create(cls, user_token: str, account_id: str) -> Finam:
        """Инициализация модуля.

        Args:
            user_token (str): API токен пользователя.
            account_id (str): ID счета пользователя.

        Returns:
            Finam: объект для работы с API.
        """
        finam = Finam(user_token, account_id)
        await finam._refresh_jwt_token()
        return finam

    async def refresh_session(self):
        async with self._get_lock():
            await self._refresh_jwt_token()
            if self._session is not None:
                await self._session.aclose()
            self._session = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=30,
                headers=self._headers(),
                http2=True,
            )

    async def _refresh_jwt_token(self) -> None:
        async with httpx.AsyncClient(
                base_url=self._base_url,
                headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                timeout=10
        ) as session:
            response = await session.post('sessions', json={'secret': self._user_token})
            token = response.json()['token']
            self._jwt_token_dict[self._user_token] = token
        await session.aclose()

    def _get_session(self) -> httpx.AsyncClient:
        if self._session is None or self._session.is_closed:
            self._session = httpx.AsyncClient(
                base_url=self._base_url,
                timeout=30,
                headers=self._headers(),
                http2=True,

            )

        return self._session

    def _headers(self):
        return {"Authorization": f"Bearer {self._jwt_token_dict[self._user_token]}",
                'Content-Type': 'application/json',
                'Accept': 'application/json'}

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
