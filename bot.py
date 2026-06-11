from aiogram import Bot, Dispatcher
from dotenv import load_dotenv
from handlers.start import router as start_router
import asyncio
import os

load_dotenv()

BOT_TOKEN = os.getenv("BOT_TOKEN")

async def main():
    bot = Bot(token=BOT_TOKEN)
    dp = Dispatcher(bot=bot)

    dp.include_router(start_router)

    await dp.start_polling(bot)

if __name__ == '__main__':
    asyncio.run(main())