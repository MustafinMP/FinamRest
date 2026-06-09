from __future__ import annotations

from dataclasses import dataclass
from datetime import datetime
from typing import Optional

from finam_rest_py.models.converters import formatted_datetime


@dataclass
class QuotaUsageMetric:
    name: str
    limit: int
    remaining: int
    reset_time: Optional[datetime | None]

    @classmethod
    def from_dict(cls, quota_usage_dict: dict) -> QuotaUsageMetric:
        return QuotaUsageMetric(
            name=quota_usage_dict['name'],
            limit=int(quota_usage_dict['limit']),
            remaining=int(quota_usage_dict['remaining']),
            reset_time=formatted_datetime(quota_usage_dict['reset_time']) if 'reset_time' in quota_usage_dict else None
        )


@dataclass
class QuotaUsageMetrics:
    quotas: list[QuotaUsageMetric]

    @classmethod
    def from_dict(cls, quota_usage_metrics_dict: dict) -> QuotaUsageMetrics:
        return QuotaUsageMetrics(
            quotas=[QuotaUsageMetric.from_dict(q) for q in quota_usage_metrics_dict['quotas']]
        )

    def __iter__(self):
        for quota in self.quotas:
            yield quota

    def as_dict(self):
        return {
            metric.name: metric
            for metric in self.quotas
        }