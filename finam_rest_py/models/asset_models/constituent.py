from __future__ import annotations

from dataclasses import dataclass
from typing import Optional


@dataclass
class Constituent:
    symbol: str
    name: str
    sector: str
    subsector: Optional[str]
    cik: str

    @classmethod
    def from_dict(cls, constituent_dict: dict) -> Constituent:
        return Constituent(
            symbol=constituent_dict['symbol'],
            name=constituent_dict['name'],
            sector=constituent_dict['sector'],
            subsector=constituent_dict['subsector'] if 'subsector' in constituent_dict.keys() else None,
            cik=constituent_dict['cik']
        )
