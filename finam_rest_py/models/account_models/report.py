from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Report:
    report_id: str
    status: int
    date_begin: datetime
    date_end: datetime
    report_form: str
    account_id: str
    url: Optional[str]

    @classmethod
    def from_dict(cls, report_dict: dict) -> Report:
        report_dict = report_dict['info']
        return Report(
            report_id=report_dict['report_id'],
            status=report_dict['status'],
            date_begin=report_dict['date_range']['date_begin'],
            date_end=report_dict['date_range']['date_end'],
            report_form=report_dict['report_form'],
            account_id=report_dict['account_id'],
            url=report_dict['url'] if 'url' in report_dict.keys() else None,
        )
