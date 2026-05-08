from datetime import datetime

from finam_rest_py.exceptions import FinamResponseFailureException
from finam_rest_py.models import Report
from finam_rest_py.services.base_service import AsyncBaseService


class ReportService(AsyncBaseService):
    async def init_report(self, date_begin: datetime, date_end: datetime, report_form) -> str:
        """Инициирует формирование отчета на сервере

        Args:
            date_begin (datetime): левая граница периода отчета.
            date_end (datetime): правая граница периода отчета.
            report_form (str): периода. Допустимые значения: 'short' или 'long'

        Returns:
            report_id (int): ID отчета на сервере.

        Raises:
            FinamResponseFailureException: если произошла ошибка запроса к серверу.
        """

        if report_form == 'short':
            form = 'REPORT_FORM_SHORT'
        elif report_form == 'long':
            form = 'REPORT_FORM_LONG'
        else:
            raise ValueError(
                f"Аргумент report_form имеет недопустимое значение {report_form} (требуется 'short' или 'long')")
        params = {
            'date_range.date_begin': date_begin.isoformat() + 'Z',
            'date_range.date_end': date_end.isoformat() + 'Z',
            'report_form': form,
            'account_id': self._account_id
        }
        response = await self._session.post('report', params=params)
        if response.status_code == 200:
            return response.json()['report_id']
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)

    async def get_report(self, report_id: str):
        response = await self._session.get(f'report/{report_id}/info')
        if response.status_code == 200:
            return Report.from_dict(response.json())
        raise FinamResponseFailureException(status_code=response.status_code, reason=response.reason_phrase,
                                            text=response.text)
