from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from finam_rest_py.models.converters import date_from_dict


@dataclass
class Asset:
    id: str
    ticker: str
    mic: str
    isin: str
    type: str
    name: str

    @property
    def symbol(self) -> str:
        return f'{self.ticker}@{self.mic}'

    @classmethod
    def from_dict(cls, asset_dict: dict) -> Asset:
        return Asset(
            id=asset_dict['id'],
            ticker=asset_dict['ticker'],
            mic=asset_dict['mic'],
            isin=asset_dict['isin'],
            type=asset_dict['type'],
            name=asset_dict['name']
        )


@dataclass
class FullAsset(Asset):
    min_price_step: float
    lot_size: float
    expiration_date: Optional[datetime, None]
    quote_currency: Optional[str | None]

    @classmethod
    def _calculate_min_step_price(cls, min_step: int, decimals: int):
        return min_step * 10 ** -decimals

    @property
    def min_lot_price_step(self):
        return self.min_price_step * self.lot_size

    @classmethod
    def from_dict(cls, asset_dict: dict) -> FullAsset:
        return FullAsset(
            id=asset_dict['id'],
            ticker=asset_dict['ticker'],
            mic=asset_dict['mic'],
            isin=asset_dict['isin'],
            type=asset_dict['type'],
            name=asset_dict['name'],
            min_price_step=cls._calculate_min_step_price(int(asset_dict['min_step']), int(asset_dict['decimals'])),
            lot_size=int(float(asset_dict['lot_size']['value'])),
            expiration_date=date_from_dict(
                asset_dict['expiration_date']) if 'expiration_date' in asset_dict else None,
            quote_currency=asset_dict.get('quote_currency', None)
        )
