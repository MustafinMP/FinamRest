from __future__ import annotations

import asyncio
from typing import Optional

import httpx


class SessionManager:
    _lock = None
    _jwt_token_dict = dict()

    def __init__(self, base_url: str, user_token: str):
        self._base_url = base_url
        self._user_token = user_token

        self._session: Optional[httpx.AsyncClient] = None

    @classmethod
    async def create(cls, base_url: str, user_token: str) -> SessionManager:
        manager = cls(base_url, user_token)
        await manager.refresh_session()
        return manager

    @classmethod
    def _get_lock(cls) -> asyncio.Lock:
        """Ленивая инициализация Lock, чтобы он привязался к правильному event loop"""
        if cls._lock is None:
            cls._lock = asyncio.Lock()
        return cls._lock

    def get_auth_token(self) -> str:
        return self._jwt_token_dict[self._user_token]

    def get_session(self) -> httpx.AsyncClient:
        if self._session is None or self._session.is_closed:
            self._session = self._get_new_session()
        return self._session

    async def refresh_session(self):
        async with self._get_lock():
            await self._refresh_jwt_token()
            if self._session is not None:
                await self._session.aclose()
            self._session = self._get_new_session()

    async def _refresh_jwt_token(self) -> None:
        while True:
            try:
                async with httpx.AsyncClient(
                        base_url=self._base_url,
                        headers={'Content-Type': 'application/json', 'Accept': 'application/json'},
                        timeout=10
                ) as session:
                    response = await session.post('sessions', json={'secret': self._user_token})
                    token = response.json()['token']
                    self._jwt_token_dict[self._user_token] = token
                await session.aclose()
                break
            except httpx.ReadTimeout:
                print('Таймаут при обновлении токена, повторная попытка обновления')

    def _get_new_session(self):
        return httpx.AsyncClient(
            base_url=self._base_url,
            timeout=30,
            headers=self._headers(),
            http2=True,
        )

    def _headers(self):
        return {"Authorization": f"Bearer {self._jwt_token_dict[self._user_token]}",
                'Content-Type': 'application/json',
                'Accept': 'application/json'}
