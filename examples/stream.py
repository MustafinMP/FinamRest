import asyncio

from finam_rest_py import Finam
from finam_rest_py.models import TimeFrame

FINAM_TOKEN = 'your_finam_token'
ACCOUNT_ID = 'your_account_id'


async def main():
    finam = await Finam.create(FINAM_TOKEN, ACCOUNT_ID)
    print('Bars stream')
    i = 0
    async for bars in finam.streams.bars_stream('SBER@MISX', TimeFrame.TIME_FRAME_M1):
        print(len(bars), bars)
        i += 1
        if i == 5: break

    print('Order book stream')
    i = 0
    async for order_book in finam.streams.order_book_stream('SBER@MISX'):
        print(order_book)
        i += 1
        if i == 5: break

    print('Quotes stream')
    i = 0
    async for quotes in finam.streams.quotes_stream('SBER@MISX', 'YDEX@MISX'):
        print(quotes)
        i += 1
        if i == 5: break

    print('Latest trades stream')
    i = 0
    async for trade in finam.streams.latest_trades_stream('SBER@MISX'):
        print(trade)
        i += 1
        if i == 5: break

    print('Account orders stream')
    i = 0
    async for order in finam.streams.account_orders_stream():
        print(order)
        i += 1
        if i == 5: break

    print('Account trades stream')
    i = 0
    async for trade in finam.streams.account_trades_stream():
        print(trade)
        i += 1
        if i == 5: break

    print('Account changes stream')
    i = 0
    async for item in finam.streams.account_changes_stream():
        print(item)
        i += 1
        if i == 5: break


if __name__ == "__main__":
    asyncio.run(main())
