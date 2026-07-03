from finam_rest_py.exceptions import FinamResponseFailureException
from finam_rest_py.models import QuotaUsageMetrics
from finam_rest_py.services.base_service import AsyncBaseService


class MetricsService(AsyncBaseService):
    async def get_usage_metrics(self, as_dict: bool = False) -> QuotaUsageMetrics:
        """получает метрики об использовании API.

        Returns:
            QuotaUsageMetrics: данные о различных метриках.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """
        response = await self._session.get('usage')
        if response.status_code == 401 or response.status_code == 500:
            await self._base_module.refresh_session()
            response = await self._session.get('usage')
        if response.status_code == 200:
            return QuotaUsageMetrics.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)
