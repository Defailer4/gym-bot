from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
import asyncio
import os
import logging

from handlers.start import router as start_router
from database.db import init_db

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot=bot)

    dp.include_router(start_router)

    logging.info("Инициализация базы данных...")
    await init_db()
    logging.info("База данных успешно инициализирована")

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())