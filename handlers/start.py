from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message

from keyboards.main_menu import reply_markup


router = Router()

@router.message(CommandStart())
async def start_handeler(message: Message):
    await message.answer(
        "Привет друн я крутой бот для отслеживания тренировок",
        reply_markup=reply_markup
    )
