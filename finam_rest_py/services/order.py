from finam_rest_py.exceptions import FinamResponseFailureException
from finam_rest_py.models import Order, OrderInfo, TradeSide, OrderValidBefore
from finam_rest_py.services.base_service import AsyncBaseService


class OrderService(AsyncBaseService):
    async def get_order(self, order_id: str) -> OrderInfo:
        """Получает информацию о заявке.

        Args:
            order_id (str): ID заявки.

        Returns:
            OrderInfo: данные о заявке.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get(f'accounts/{self._account_id}/orders/{order_id}')
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.get(f'accounts/{self._account_id}/orders/{order_id}')

        if response.status_code == 200:
            return OrderInfo.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_orders(self) -> list[OrderInfo]:
        """Получает данные обо всех заявках.

        Returns:
            list[OrderInfo]: данные обо всех заявках.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get(f'accounts/{self._account_id}/orders')
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.get(f'accounts/{self._account_id}/orders')
        if response.status_code == 200:
            return [OrderInfo.from_dict(o) for o in response.json()['orders']]
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def place_order(self, order: Order) -> OrderInfo:
        """Размещает заявку на бирже.

        Args:
            order (Order): размещаемая заявка.

        Returns:
            OrderInfo: информация о размещенной заявке.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        if order.account_id is None:
            order.account_id = self._base_module.get_account()
        response = await self._session.post(f'accounts/{self._account_id}/orders', json=order.to_dict())
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.post(f'accounts/{self._account_id}/orders', json=order.to_dict())
        if response.status_code == 200:
            return OrderInfo.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def place_sl_tp_order(
            self,
            symbol: str,
            side: TradeSide | str,
            sl_quantity: float,
            sl_price: float,
            tp_quantity: float,
            tp_price: float,
            valid_before: OrderValidBefore = OrderValidBefore.VALID_BEFORE_GOOD_TILL_CANCEL
    ) -> OrderInfo:
        """Размещает заявку на бирже.

        Args:


        Returns:
            OrderInfo: информация о размещенной заявке.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        if isinstance(side, str):
            if side == 'long' or side == 'LONG':
                side = TradeSide.LONG
            elif side == 'short' or side == 'SHORT':
                side = TradeSide.SHORT
            else:
                raise ValueError
        params = {
            'symbol': symbol,
            'side': side.value,
            'quantity_sl': {'value': str(sl_quantity)},
            'sl_price': {'value': str(sl_price)},
            'quantity_tp': {'value': str(tp_quantity)},
            'tp_price': {'value': str(tp_price)},
            'valid_before': valid_before.value,
            # "tp_guard_spread": {
            #     "value": "0"
            # },
            # "tp_spread_measure": "TP_SPREAD_MEASURE_UNDEFINED",
            # "client_order_id": "string",
        }
        response = await self._session.post(f'accounts/{self._account_id}/sltp-orders', json=params)
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.post(f'accounts/{self._account_id}/sltp-orders', json=params)
        if response.status_code == 200:
            return OrderInfo.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def cancel_order(self, order_id: str) -> OrderInfo:
        """Отменяет размещенную заявку.

        Args:
            order_id (str): ID размещенной заявки.

        Returns:
            OrderInfo: информация об отменяемой заявке.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.delete(f'accounts/{self._account_id}/orders/{order_id}')
        if response.status_code == 401 or response.status_code == 500:
            await self._session_manager.refresh_session()
            response = await self._session.delete(f'accounts/{self._account_id}/orders/{order_id}')
        if response.status_code == 200:
            return OrderInfo.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)
