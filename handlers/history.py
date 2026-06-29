import aiosqlite
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery
from datetime import datetime

from database.history import get_active_months, get_workout_by_month, get_workout_details
from keyboards.history_kb import get_history_kb, get_months_archive_kb, MONTHS_RU

router = Router()

@router.message(F.text == "📜 История")
async def show_current_month_history(message: Message, db: aiosqlite.Connection):
    user_id = message.from_user.id
    current_ym = datetime.now().strftime("%Y-%m")

    workouts = await get_workout_by_month(db, user_id, current_ym)

    if not workouts:
        await message.answer(
            "📭 В этом месяце тренировок еще не было. Заглянем в старые записи?",
            reply_markup=get_history_kb([], show_archive_btn=True)
        )
        return

    await message.answer(
        "📜 <b>Твои тренировки в этом месяце:</b>\n\nВыбери дату:",
        reply_markup=get_history_kb(workouts, show_archive_btn=True),
        parse_mode="HTML"
    )


@router.callback_query(F.data == "hist_archive")
async def show_archive_months(callback: CallbackQuery, db: aiosqlite.Connection):
    user_id = callback.from_user.id
    months = await get_active_months(db, user_id)

    if not months:
        await callback.answer("Архив пока пуст!", show_alert=True)
        return

    await callback.message.edit_text(
        "🗄 <b>Архив тренировок</b>\n\nВыбери месяц:",
        reply_markup=get_months_archive_kb(months),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("hist_month_"))
async def show_month_workouts(callback: CallbackQuery, db: aiosqlite.Connection):
    user_id = callback.from_user.id
    year_month = callback.data.split("_")[2]  # Достаем "2026-06"

    workouts = await get_workout_by_month(db, user_id, year_month)

    year, month_num = year_month.split("-")
    month_name = MONTHS_RU.get(month_num, month_num)

    await callback.message.edit_text(
        f"📜 <b>Тренировки за {month_name} {year}:</b>\n\nВыбери дату:",
        reply_markup=get_history_kb(workouts, show_archive_btn=False),
        parse_mode="HTML"
    )


@router.callback_query(F.data.startswith("hist_view_"))
async def process_history_view(callback: CallbackQuery, db: aiosqlite.Connection):
    await callback.answer()

    workout_id = int(callback.data.split("_")[2])
    raw_details = await get_workout_details(db, workout_id)

    if not raw_details:
        await callback.message.answer("⚠️ Не удалось найти подходы для этой тренировки.")
        return

    history_dict = {}
    for exc_name, set_num, weight, reps in raw_details:
        if exc_name not in history_dict:
            history_dict[exc_name] = []
        history_dict[exc_name].append(f"  {set_num}. <code>{weight} кг</code> x <code>{reps}</code>")

    msg_lines = ["📋 <b>Детали тренировки:</b>\n"]
    for exc_name, sets in history_dict.items():
        msg_lines.append(f"🏋️‍♂️ <b>{exc_name}</b>")
        msg_lines.extend(sets)
        msg_lines.append("")

    text = "\n".join(msg_lines)
    await callback.message.answer(text, parse_mode="HTML")