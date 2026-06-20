import aiosqlite
from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.types import Message
from keyboards.main_menu import reply_markup
from database.users import get_user, add_user


router = Router()

@router.message(CommandStart())
async def start_handler(message: Message, db: aiosqlite.Connection):
    user_id = message.from_user.id

    user = await get_user(db, user_id)

    if user is None:
        await add_user(db, user_id)

        await message.answer(
            "Привет друн твой профиль успешно зарегестрирован!",
            reply_markup=reply_markup
        )
    else:
        await message.answer(
            "Привет друн",
            reply_markup=reply_markup
        )