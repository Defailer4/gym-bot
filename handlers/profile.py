import aiosqlite
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.profile_kb import get_profile_main_kb, get_profile_settings_kb
from database.users import update_water_goal, update_weight_goal
from services.profile import get_profile_text_and_kb
router = Router()


class ProfileStates(StatesGroup):
    waiting_for_water_goal = State()
    waiting_for_weight_goal = State()



@router.message(F.text == "👤 Мой профиль")
async def profile_main_message(message: Message, db: aiosqlite.Connection):
    text = await get_profile_text_and_kb(db, message.from_user.id)
    await message.answer(text, reply_markup=get_profile_main_kb(), parse_mode="HTML")


@router.callback_query(F.data == "back_to_profile")
async def back_to_profile(callback: CallbackQuery, db: aiosqlite.Connection):
    await callback.answer()
    text = await get_profile_text_and_kb(db, callback.from_user.id)
    # Поменяли reply_markup на главную клавиатуру профиля
    await callback.message.edit_text(text, reply_markup=get_profile_main_kb(), parse_mode="HTML")



@router.callback_query(F.data == "profile_settings")
async def show_profile_settings(callback: CallbackQuery):
    await callback.answer()
    await callback.message.edit_text(
        "⚙️ <b>Настройка личных целей</b>\n\n"
        "Выбери, какой показатель ты хочешь изменить или установить:",
        reply_markup=get_profile_settings_kb(),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "edit_goal_water")
async def edit_water_goal_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        "💧 <b>Изменение цели воды</b>\n\n"
        "Введи новую дневную норму воды в <b>миллилитрах</b> (например, 2500):",
        parse_mode="HTML"
    )
    await state.set_state(ProfileStates.waiting_for_water_goal)


@router.callback_query(F.data == "edit_goal_weight")
async def edit_weight_goal_start(callback: CallbackQuery, state: FSMContext):
    await callback.answer()
    await callback.message.edit_text(
        "🎯 <b>Изменение целевого веса</b>\n\n"
        "Введи желаемый вес в <b>килограммах</b> (например, 82.5):",
        parse_mode="HTML"
    )
    await state.set_state(ProfileStates.waiting_for_weight_goal)



@router.message(ProfileStates.waiting_for_water_goal)
async def process_water_goal_input(message: Message, db: aiosqlite.Connection, state: FSMContext):
    try:
        new_goal = int(message.text)
        if not (500 <= new_goal <= 10000):
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введи адекватную цель — целое число от 500 до 10000 мл:")
        return

    await update_water_goal(db, message.from_user.id, new_goal)
    await state.clear()

    text = await get_profile_text_and_kb(db, message.from_user.id)
    await message.answer(text, reply_markup=get_profile_main_kb(), parse_mode="HTML")


@router.message(ProfileStates.waiting_for_weight_goal)
async def process_weight_goal_input(message: Message, db: aiosqlite.Connection, state: FSMContext):
    raw_text = message.text.replace(",", ".")
    try:
        new_goal = float(raw_text)
        if not (10 <= new_goal <= 635):
            raise ValueError
    except ValueError:
        await message.answer("Пожалуйста, введи реальный целевой вес цифрами (от 10 до 635 кг):")
        return

    await update_weight_goal(db, message.from_user.id, new_goal)
    await state.clear()

    text = await get_profile_text_and_kb(db, message.from_user.id)
    await message.answer(text, reply_markup=get_profile_main_kb(), parse_mode="HTML")