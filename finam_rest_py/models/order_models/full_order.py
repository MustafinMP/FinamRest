from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from finam_rest_py.models.converters import formatted_datetime
from finam_rest_py.models.order_models.order import Order
from finam_rest_py.models.order_models.sltp_order import SLTPOrder


@dataclass
class OrderInfo:
    order_id: str
    exec_id: str
    status: None
    order: Optional[Order]
    sltp_order: Optional[SLTPOrder]
    transact_at: datetime
    accept_at: Optional[datetime | None]
    withdraw_at: Optional[datetime | None]
    initial_quantity: Optional[float | None]
    executed_quantity: Optional[float | None]
    remaining_quantity: Optional[float | None]

    @classmethod
    def from_dict(cls, order_dict: dict) -> OrderInfo:
        return OrderInfo(
            order_id=order_dict['order_id'],
            exec_id=order_dict['exec_id'],
            status=order_dict['status'],
            order=Order.from_dict(order_dict['order']) if 'order' in order_dict else None,
            sltp_order=SLTPOrder.from_dict(order_dict['sltp_order']) if 'sltp_order' in order_dict else None,
            transact_at=formatted_datetime(order_dict['transact_at']),
            accept_at=formatted_datetime(order_dict['accept_at']) if 'accept_at' in order_dict else None,
            withdraw_at=formatted_datetime(order_dict['withdraw_at']) if 'withdraw_at' in order_dict else None,
            initial_quantity=float(
                order_dict['initial_quantity']['value']) if 'initial_quantity' in order_dict else None,
            executed_quantity=float(
                order_dict['executed_quantity']['value']) if 'executed_quantity' in order_dict else None,
            remaining_quantity=float(
                order_dict['remaining_quantity']['value']) if 'remaining_quantity' in order_dict else None,
        )
