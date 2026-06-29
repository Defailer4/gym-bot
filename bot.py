from aiogram import Bot, Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from dotenv import load_dotenv
import asyncio
import os
import logging

from handlers.start import router as start_router
from handlers.water import router as water_router
from handlers.weight import router as weight_router
from handlers.profile import router as profile_router
from handlers.workout import router as workout_router
from handlers.history import router as history_router

from middlewares.db import DbMiddleware
from database.db import init_db

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")
redis_host = os.getenv("REDIS_HOST", "localhost")
storage = RedisStorage.from_url(f"redis://{redis_host}:6379/0")

async def main():
    logging.basicConfig(level=logging.INFO)

    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot=bot, storage=storage)

    dp.include_router(start_router)
    dp.include_router(water_router)
    dp.include_router(weight_router)
    dp.include_router(profile_router)
    dp.include_router(workout_router)
    dp.include_router(history_router)

    dp.message.middleware(DbMiddleware())
    dp.callback_query.middleware(DbMiddleware())

    logging.info("Инициализация базы данных...")
    await init_db()
    logging.info("База данных успешно инициализирована")
    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())