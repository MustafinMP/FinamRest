from __future__ import annotations

import json
from typing import Iterable, TYPE_CHECKING

import websockets

if TYPE_CHECKING:
    from finam_rest_py import Finam
from finam_rest_py._session_manager import SessionManager
from finam_rest_py.models import Bar, TimeFrame, OrderBook, Quote, AssetTrade, OrderInfo, Trade, Account


class Stream:
    def __init__(self, ws_url: str, base_module: Finam, session_manager: SessionManager):
        self._ws_url = ws_url
        self._base_module = base_module
        self._session_manager = session_manager

    async def bars_stream(self, symbol: str, timeframe: TimeFrame) -> Iterable[list[Bar]]:
        async with websockets.connect(self._ws_url) as ws:
            await ws.send(json.dumps({
                "action": "SUBSCRIBE",
                "type": "BARS",
                "data": {"symbol": symbol, "timeframe": timeframe.to_str()},
                "token": self._session_manager.get_auth_token()
            }))
            async for raw_message in ws:
                message = json.loads(raw_message)
                if message['type'] == 'DATA':
                    payload = json.loads(message['payload'])
                    yield [Bar.from_dict(bar) for bar in payload['bars']]
                elif message['type'] == 'ERROR':
                    raise ValueError(message['error_info']['message'])

    async def order_book_stream(self, symbol: str) -> Iterable[OrderBook]:
        async with websockets.connect(self._ws_url) as ws:
            await ws.send(json.dumps({
                "action": "SUBSCRIBE",
                "type": "ORDER_BOOK",
                "data": {"symbol": symbol},
                "token": self._session_manager.get_auth_token()}))
            async for raw_message in ws:
                message = json.loads(raw_message)
                if message['type'] == 'DATA':
                    payload = json.loads(message['payload'])
                    yield OrderBook.from_ws_dict(payload['orderBook'][0])
                elif message['type'] == 'ERROR':
                    raise ValueError(message['error_info']['message'])

    async def quotes_stream(self, *symbols: str) -> Iterable[list[Quote]]:
        async with websockets.connect(self._ws_url) as ws:
            await ws.send(json.dumps({
                "action": "SUBSCRIBE",
                "type": "QUOTES",
                "data": {"symbols": symbols},
                "token": self._session_manager.get_auth_token()}))
            async for raw_message in ws:
                message = json.loads(raw_message)
                if message['type'] == 'DATA':
                    payload = json.loads(message['payload'])
                    yield [Quote.from_dict(quote) for quote in payload['quote']]
                elif message['type'] == 'ERROR':
                    raise ValueError(message['error_info']['message'])

    async def latest_trades_stream(self, symbol: str) -> Iterable[AssetTrade]:
        async with websockets.connect(self._ws_url) as ws:
            await ws.send(json.dumps({
                "action": "SUBSCRIBE",
                "type": "INSTRUMENT_TRADES",
                "data": {"symbol": symbol},
                "token": self._session_manager.get_auth_token()}))
            async for raw_message in ws:
                message = json.loads(raw_message)
                if message['type'] == 'DATA':
                    payload = json.loads(message['payload'])
                    yield [AssetTrade.from_dict(trade) for trade in payload['trades']]
                elif message['type'] == 'ERROR':
                    raise ValueError(message['error_info']['message'])

    async def account_orders_stream(self, account_id: int = None) -> Iterable[list[OrderInfo]]:
        async with websockets.connect(self._ws_url) as ws:
            await ws.send(json.dumps({
                "action": "SUBSCRIBE",
                "type": "ORDERS",
                "data": {"account_id": account_id if account_id is not None else self._base_module.get_account()},
                "token": self._session_manager.get_auth_token()}))
            async for raw_message in ws:
                message = json.loads(raw_message)
                if message['type'] == 'DATA':
                    payload = json.loads(message['payload'])
                    if 'orders' in payload.keys():
                        yield [OrderInfo.from_dict(order) for order in payload['orders']]
                    else:
                        yield []
                elif message['type'] == 'ERROR':
                    raise ValueError(message['error_info']['message'])

    async def account_trades_stream(self, account_id: int = None) -> Iterable[list[Trade]]:
        async with websockets.connect(self._ws_url) as ws:
            await ws.send(json.dumps({
                "action": "SUBSCRIBE",
                "type": "TRADES",
                "data": {"account_id": account_id if account_id is not None else self._base_module.get_account()},
                "token": self._session_manager.get_auth_token()}))
            async for raw_message in ws:
                message = json.loads(raw_message)
                if message['type'] == 'DATA':
                    payload = json.loads(message['payload'])
                    if 'trades' in payload.keys():
                        yield [Trade.from_dict(trade) for trade in payload['trades']]
                    else:
                        yield []
                elif message['type'] == 'ERROR':
                    raise ValueError(message['error_info']['message'])

    async def account_changes_stream(self, account_id: int = None) -> Iterable[None]:
        async with websockets.connect(self._ws_url) as ws:
            await ws.send(json.dumps({
                "action": "SUBSCRIBE",
                "type": "ACCOUNT",
                "data": {"account_id": account_id if account_id is not None else self._base_module.get_account()},
                "token": self._session_manager.get_auth_token()}))
            async for raw_message in ws:
                message = json.loads(raw_message)
                if message['type'] == 'DATA':
                    payload = json.loads(message['payload'])
                    yield Account.from_dict(payload)
                elif message['type'] == 'ERROR':
                    raise ValueError(message['error_info']['message'])
