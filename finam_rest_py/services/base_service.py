from __future__ import annotations
from typing import TYPE_CHECKING

from finam_rest_py._session_manager import SessionManager

if TYPE_CHECKING:
    from finam_rest_py import Finam


class AsyncBaseService:
    def __init__(self, base_module: Finam, session_manager: SessionManager):
        self._base_module = base_module
        self._session_manager = session_manager

    @property
    def _session(self):
        return self._session_manager.get_session()

    @property
    def _account_id(self):
        return self._base_module.get_account()
