from __future__ import annotations

from dataclasses import dataclass


@dataclass
class MoneyModel:
    currency_code: str
    units: int
    nanos: int

    @classmethod
    def from_dict(cls, response_dict: dict) -> MoneyModel:
        return MoneyModel(
            currency_code=str(response_dict['currency_code']) if 'currency_code' in response_dict.keys()
            else str(response_dict['currencyCode']),
            units=int(response_dict['units']),
            nanos=int(response_dict['nanos']) // (10 ** 7)
        )
