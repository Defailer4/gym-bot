import aiosqlite
from database.users import get_user_goals
from database.weight import get_last_weight
from database.water import get_today_water

def generate_water_bar(current: int, goal: int) -> str:
    if goal <= 0:
        return "⚪⚪⚪⚪⚪"
    filled_count = min(int((current / goal)* 5), 5)
    empty_count = 5 - filled_count
    return "🔵" * filled_count + "⚪" * empty_count

async def get_profile_text_and_kb(db: aiosqlite.Connection, user_id: int) -> str:
    water_goal, weight_goal = await get_user_goals(db, user_id)
    current_weight = await get_last_weight(db, user_id)
    current_water = await get_today_water(db, user_id)

    weight_str = f"<code>{current_weight} кг</code>" if current_weight else "<i>не записан</i>"

    if weight_goal:
        goal_str = f"<code>{weight_goal} кг</code>"
        if current_weight:
            diff = abs(current_weight - weight_goal)
            status = "осталось" if current_weight > weight_goal else "набрать"
            goal_str += f" ({status} <code>{round(diff, 1)} кг</code>)"
    else:
        goal_str = "<i>не задана</i>"


    water_bar = generate_water_bar(current_water, water_goal)
    water_text = f"<code>{round(current_water/1000, 1)} / {round(water_goal/1000, 1)} л</code> {water_bar}"

    bench_press = "<code>0 кг</code>"
    squat = "<code>0 кг</code>"
    deadlift = "<code>0 кг</code>"
    total_sum = "<code>0 кг</code>"
    rank = "Без разряда"

    return (
        "👤 <b>Ваш профиль</b>\n\n"
        "📊 <b>Физические показатели</b>\n"
        f"├── ⚖️ Текущий вес: {weight_str}\n"
        f"├── 🎯 Цель: {goal_str}\n"
        f"└── 💧 Вода сегодня: {water_text}\n\n"
        "🏋️‍♂️ <b>Силовые рекорды</b>\n"
        f"├── 🛡️ Жим лежа: {bench_press}\n"
        f"├── 🦵 Приседания: {squat}\n"
        f"└── 🏋️‍♂️ Становая тяга: {deadlift}\n\n"
        "🏆 <b>Сумма троеборья</b>\n"
        f"└── 🔥 {total_sum} (Класс: {rank})"
    )