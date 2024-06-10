import os
import asyncio
import logging

from aiogram import Dispatcher, Bot
from handler import form_router


async def main() -> None:
    logging.basicConfig(level=logging.DEBUG)

    dp = Dispatcher()
    bot = Bot(token='7329106712:AAEsE-rV_xhAqwHF09OQVeKKD_EA64Ov2t8')
    dp.include_router(form_router)

    await dp.start_polling(bot)


if __name__ == '__main__':
    try:
        asyncio.run(main())
    except (KeyboardInterrupt, SystemExit):
        print('Bot stopped')
