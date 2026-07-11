from __future__ import annotations

from datetime import timedelta
from enum import Enum



class TimeFrame(Enum):
    TIME_FRAME_UNSPECIFIED = 0  # Таймфрейм не указан
    TIME_FRAME_M1 = 1  # 1 минута. Глубина данных 7 дней.
    TIME_FRAME_M5 = 5  # 5 минут. Глубина данных 30 дней.
    TIME_FRAME_M15 = 9  # 15 минут. Глубина данных 30 дней.
    TIME_FRAME_M30 = 11  # 30 минут. Глубина данных 30 дней.
    TIME_FRAME_H1 = 12 # 1 час. Глубина данных 30 дней.
    TIME_FRAME_H2 = 13  # 2 часа. Глубина данных 30 дней.
    TIME_FRAME_H4 = 15  # 4 часа. Глубина данных 30 дней.
    TIME_FRAME_H8 = 17  # 8 часов. Глубина данных 30 дней.
    TIME_FRAME_D = 19  # День. Глубина данных 365 дней.
    TIME_FRAME_W = 20  # Неделя. Глубина данных 365 * 5 дней.
    TIME_FRAME_MN = 21  # Месяц. Глубина данных 365 * 5 дней.
    TIME_FRAME_QR = 22  # Квартал. Глубина данных 365 * 5 дней.
    UNSPECIFIED = 0  # Таймфрейм не указан
    M1 = 1  # 1 минута. Глубина данных 7 дней.
    M5 = 5  # 5 минут. Глубина данных 30 дней.
    M15 = 9  # 15 минут. Глубина данных 30 дней.
    M30 = 11  # 30 минут. Глубина данных 30 дней.
    H1 = 12 # 1 час. Глубина данных 30 дней.
    H2 = 13  # 2 часа. Глубина данных 30 дней.
    H4 = 15  # 4 часа. Глубина данных 30 дней.
    H8 = 17  # 8 часов. Глубина данных 30 дней.
    D = 19  # День. Глубина данных 365 дней.
    W = 20  # Неделя. Глубина данных 365 * 5 дней.
    MN = 21  # Месяц. Глубина данных 365 * 5 дней.
    QR = 22  # Квартал. Глубина данных 365 * 5 дней.

    def max_deep(self) -> timedelta:
        if self.value == 0:
            return None
        return {
            1: timedelta(days=7),
            5: timedelta(days=30),
            9: timedelta(days=30),
            11: timedelta(days=30),
            12: timedelta(days=30),
            13: timedelta(days=30),
            15: timedelta(days=30),
            17: timedelta(days=30),
            19: timedelta(days=365),
            20: timedelta(days=365 * 5),
            21: timedelta(days=365 * 5),
            22: timedelta(days=365 * 5),
        }[self.value]

    @classmethod
    def from_str(cls, string: str) -> TimeFrame:
        match string:
            case 'TIME_FRAME_UNSPECIFIED', None: return cls.TIME_FRAME_UNSPECIFIED
            case 'TIME_FRAME_M1', 'M1', 'm1': return cls.TIME_FRAME_M1
            case 'TIME_FRAME_M5', 'M5', 'm5': return cls.TIME_FRAME_M5
            case 'TIME_FRAME_M15', 'M15', 'm15': return cls.TIME_FRAME_M15
            case 'TIME_FRAME_M30', 'M30', 'm30': return cls.TIME_FRAME_M30
            case 'TIME_FRAME_H1', 'H1', 'h1': return cls.TIME_FRAME_H1
            case 'TIME_FRAME_H2', 'H2', 'h2': return cls.TIME_FRAME_H2
            case 'TIME_FRAME_H4', 'H4', 'h4': return cls.TIME_FRAME_H4
            case 'TIME_FRAME_H8', 'H8', 'h8': return cls.TIME_FRAME_H8
            case 'TIME_FRAME_D', 'D', 'd': return cls.TIME_FRAME_D
            case 'TIME_FRAME_W', 'W', 'w': return cls.TIME_FRAME_W
            case 'TIME_FRAME_MN', 'MN', 'mn': return cls.TIME_FRAME_MN
            case 'TIME_FRAME_QR', 'QR', 'qr': return cls.TIME_FRAME_QR
            case _: raise ValueError(f'Invalid timeframe string {string}')

    def to_str(self) -> str:
        return {
            1: 'TIME_FRAME_M1',
            5: 'TIME_FRAME_M5',
            9: 'TIME_FRAME_M15',
            11: 'TIME_FRAME_M30',
            12: 'TIME_FRAME_H1',
            13: 'TIME_FRAME_H2',
            15: 'TIME_FRAME_H4',
            17: 'TIME_FRAME_H8',
            19: 'TIME_FRAME_D',
            20: 'TIME_FRAME_W',
            21: 'TIME_FRAME_MN',
            22: 'TIME_FRAME_QR',
        }[self.value]
