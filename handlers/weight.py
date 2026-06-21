import aiosqlite
from aiogram import F, Router
from aiogram.types import Message
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from database.weight import add_weight, get_last_weight

router = Router()

class WeightStates(StatesGroup):
    waiting_for_weight = State()

@router.message(F.text == "⚖️ Вес тела")
async def weight_main(message: Message, db: aiosqlite.Connection, state: FSMContext):
    user_id = message.from_user.id
    last_weight = await get_last_weight(db, user_id)

    if last_weight:
        text = f"⚖️ <b>Твой трекер веса</b>\n\nПоследний записанный вес: <code>{last_weight} кг</code>\n\nВведи свой текущий вес в килограммах (например, 85.5):"
    else:
        text = "⚖️ <b>Твой трекер веса</b>\n\nТы еще не записывал свой вес.\n\nВведи свой текущий вес в килограммах (например, 85.5):"

    await message.answer(text, parse_mode="HTML")

    await state.set_state(WeightStates.waiting_for_weight)

