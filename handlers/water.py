import aiosqlite
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from database.water import get_today_water, add_water, delete_last_water
from keyboards.water_kb import get_water_kb

router = Router()

def get_water_response(today_amount: int):
    text = f"💧 <b>Твой трекер воды</b>\n\nВыпито за сегодня: <code>{today_amount} мл</code>"
    reply_markup = get_water_kb()
    return text, reply_markup

@router.message(F.text == "💧 Вода")
async def water_main(message: Message, db: aiosqlite.Connection):
    user_id = message.from_user.id

    today_amount = await get_today_water(db, user_id)

    text, reply_markup = get_water_response(today_amount)
    await message.answer(text, reply_markup=reply_markup, parse_mode="HTML")

@router.callback_query(F.data.startswith("water_add_"))
async def water_add_callback(callback: CallbackQuery, db: aiosqlite.Connection):
    user_id = callback.from_user.id

    amount = int(callback.data.split("_")[-1])

    await add_water(db, user_id, amount)

    today_amount = await get_today_water(db, user_id)

    await callback.answer(f"Добавлено {amount} мл!")

    text, reply_markup = get_water_response(today_amount)
    await callback.message.edit_text(text, reply_markup=reply_markup, parse_mode="HTML")

@router.callback_query(F.data == "water_rollback")
async def water_rollback_callback(callback: CallbackQuery, db: aiosqlite.Connection):
    user_id = callback.from_user.id
    was_deleted = await delete_last_water(db, user_id)

    if was_deleted:
        today_amount = await get_today_water(db, user_id)
        await callback.answer("Последнее действие отменено!")

        text, reply_markup = get_water_response(today_amount)
        await callback.message.edit_text(text, reply_markup=reply_markup,parse_mode="HTML")
    else:
        await callback.answer("Удалять нечего, лог за сегодня пуст! 🤷‍♂️", show_alert=True)