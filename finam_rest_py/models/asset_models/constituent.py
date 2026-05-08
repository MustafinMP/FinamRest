from __future__ import annotations

from dataclasses import dataclass


@dataclass
class Constituent:
    symbol: str
    name: str
    sector: str
    subsector: str
    cik: str

    @classmethod
    def from_dict(cls, constituent_dict: dict) -> Constituent:
        return Constituent(
            symbol=constituent_dict['symbol'],
            name=constituent_dict['name'],
            sector=constituent_dict['sector'],
            subsector=constituent_dict['subsector'],
            cik=constituent_dict['cik']
        )
