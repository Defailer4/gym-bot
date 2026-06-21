import aiosqlite
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from database.weight import add_weight, get_last_weight, delete_last_weight
from keyboards.weight_kb import get_weight_rollback_kb, get_cancel_weight_kb
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

    await message.answer(text, reply_markup=get_cancel_weight_kb(), parse_mode="HTML")

    await state.set_state(WeightStates.waiting_for_weight)


@router.callback_query(F.data == "cancel_weight_input", WeightStates.waiting_for_weight)
async def cancel_weight_callback(callback: CallbackQuery, state: FSMContext):
    await state.clear()
    await callback.answer("Ввод отменен")
    await callback.message.edit_text("❌ Ввод веса отменен. Можешь вернуться к этому позже.")


@router.message(WeightStates.waiting_for_weight)
async def process_weight_input(message: Message, db: aiosqlite.Connection, state: FSMContext):
    raw_text = message.text.replace(",", ".")

    try:
        weight_value = float(raw_text)

        if not(10 <= weight_value <= 635):
            await message.answer("Пожалуйста, введи реальный вес в килограммах (от 10 до 635)")
            return

    except ValueError:
        await message.answer("Непонятный формат! Пожалуйста, введи только цифры (например 85,5):")
        return

    user_id = message.from_user.id
    await add_weight(db, user_id, weight_value)
    await state.clear()

    await message.answer(
        f"✅ Твой вес <b>{weight_value} кг</b> успешно сохранен!",
        reply_markup=get_weight_rollback_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "rollback_last_weight")
async def weight_rollback_last_weight(callback: CallbackQuery, db: aiosqlite.Connection):
    user_id = callback.from_user.id
    was_deleted = await delete_last_weight(db, user_id)

    if was_deleted:
        await callback.answer("Запись веса удалена")
        await callback.message.edit_text("↩️ Последняя запись веса успешно удалена.")
    else:
        await callback.answer("Нечего удалять!", show_alert=True)
        await callback.message.edit_text("❌ Ошибка: не удалось найти запись для удаления.")