from __future__ import annotations

from dataclasses import dataclass
from typing import Optional

from finam_rest_py.models.trade_side import TradeSide
from finam_rest_py.models.order_models.order_valid_before import OrderValidBefore


@dataclass
class SLTPOrder:
    symbol: str
    client_order_id: str
    sl_quantity: float
    tp_quantity: float
    sl_price: float
    tp_price: float
    side: TradeSide
    account_id: Optional[str] = None
    valid_before: Optional[OrderValidBefore | None] = None
    comment: Optional[str] = None

    @classmethod
    def from_dict(cls, dct: dict) -> SLTPOrder:
        return cls(
            symbol=dct.get('symbol'),
            client_order_id=dct['client_order_id'] if 'client_order_id' in dct.keys() else dct['clientOrderId'],
            sl_quantity=dct['quantity_sl']['value'] if 'quantity_sl' in dct.keys() else dct['quantitySl']['value'],
            tp_quantity=dct['quantity_tp']['value'] if 'quantity_tp' in dct.keys() else dct['quantityTp']['value'],
            sl_price=dct['sl_price']['value'] if 'sl_price' in dct.keys() else dct['slPrice']['value'],
            tp_price=dct['tp_price']['value'] if 'tp_price' in dct.keys() else dct['tpPrice']['value'],
            side=TradeSide.from_str(dct['side']),
            comment=dct.get('comment'),
            account_id=dct.get('account_id') if 'account_id' in dct.keys() else dct['accountId'],
        )