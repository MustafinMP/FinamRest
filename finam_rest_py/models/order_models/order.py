from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from finam_rest_py.models.order_models.order_stop_condition import OrderStopCondition
from finam_rest_py.models.order_models.order_type import OrderType
from finam_rest_py.models.order_models.order_type_in_force import OrderTypeInForce
from finam_rest_py.models.order_models.order_valid_before import OrderValidBefore
from finam_rest_py.models.trade_side import TradeSide


@dataclass
class Order:
    symbol: str
    quantity: float
    side: TradeSide
    type: OrderType
    time_in_force: OrderTypeInForce
    account_id: Optional[str] = None
    limit_price: Optional[float | None] = None
    stop_price: Optional[float | None] = None
    stop_condition: Optional[OrderStopCondition | None] = None
    client_order_id: Optional[str | None] = None
    valid_before: Optional[OrderValidBefore | None] = None
    comment: Optional[str | None] = None

    def to_dict(self) -> dict:
        order = {
            'symbol': self.symbol,
            'quantity': {'value': str(self.quantity)},
            'side': 'SIDE_BUY' if self.side == TradeSide.LONG else 'SIDE_SELL',
            'type': self.type.to_str(),
            'time_in_force': self.time_in_force.to_str()
        }
        if self.limit_price:
            order['limit_price'] = {'value': str(self.limit_price)}
        if self.stop_price:
            order['stop_price'] = {'value': str(self.stop_price)}
        if self.stop_condition:
            order['stop_condition'] = self.stop_condition.value
        if self.client_order_id:
            order['client_order_id'] = self.client_order_id
        if self.valid_before:
            order['valid_before'] = self.valid_before.value
        if self.comment:
            order['comment'] = self.comment
        return order

    @classmethod
    def from_dict(cls, order_dict: dict) -> Order:
        return Order(
            account_id=order_dict['account_id'] if 'account_id' in order_dict else order_dict['accountId'],
            symbol=order_dict['symbol'],
            quantity=float(order_dict['quantity']['value']),
            side=TradeSide.from_str(order_dict['side']),
            type=OrderType.from_str(order_dict['type']),
            time_in_force=OrderTypeInForce.from_str(order_dict['time_in_force']) if 'time_in_force' in order_dict
            else OrderTypeInForce.from_str(order_dict['timeInForce']) if 'timeInForce' in order_dict else None,
            limit_price=float(order_dict['limit_price']['value']) if 'limit_price' in order_dict.keys()
            else float(order_dict['limitPrice']['value']) if 'limitPrice' in order_dict.keys() else None,
            stop_price=float(order_dict['stop_price']['value']) if 'stop_price' in order_dict.keys()
            else float(order_dict['stopPrice']['value']) if 'stopPrice' in order_dict.keys() else None,
            stop_condition=OrderStopCondition.from_str(
                order_dict.get('stop_condition', order_dict.get('stopCondition', None))),
            client_order_id=order_dict.get('client_order_id', order_dict.get('clientOrderId', None)),
            valid_before=OrderValidBefore.from_str(order_dict.get('valid_before', order_dict.get('validBefore', None))),
            comment=order_dict.get('comment', None),
        )
