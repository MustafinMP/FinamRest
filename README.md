# FinamRestPy

FinamRestPy - асинхронная библиотека-обертка над Finam Trade API (REST, WebSocket) (https://tradeapi.finam.ru/).
Основная цель библиотеки - обеспечить подключение Finam Trade API к коду на Python,
сохранив структуру Finam Trade API и сделав интерфейс библиотеки максимально простым
для разработчиков.

### Возможности библиотеки

- Подключение к API, автоматическое обновление токена,
  поддержание одновременно нескольких клиентов на одном токене
- Выполнение запросов к REST API
- Стрим данных через WebSocket
- Асинхронность
- Работа через типы Python, наличие type hints

## Установка

```shell
pip install git+https://github.com/MustafinMP/FinamRestPy.git
```

## Использование

Для начала работы необходимо инициализировать модуль:

```python
import asyncio
from finam_rest_py import Finam

finam = asyncio.run(Finam.create('your_finam_token', 'your_account_id'))
```

Инструкция, как получить токен и узнать ID аккаунта(-ов),
есть на сайте Finam Trade API (https://tradeapi.finam.ru/docs/about/)

Для смены аккаунта используйте следующий код, подставив в него ID нужного аккаунта:

```python
import asyncio
from finam_rest_py import Finam

finam = asyncio.run(Finam.create('your_finam_token', 'your_account_id'))
finam.set_account('your_other_account_id')
```

Ниже представлен пример запроса для получения информации об аккаунте:

```python
import asyncio
from finam_rest_py import Finam


async def main():
    finam = await Finam.create('your_finam_token', 'your_account_id')
    account = await finam.account.get_account()
    print(account)


asyncio.run(main())
```

Больше примеров использования можно увидеть в папке examples
