import aiosqlite
from aiogram import Router, F, types
from aiogram.types import BufferedInputFile

from keyboards.profile_kb import get_profile_history_kb, get_profile_main_kb, get_user_exercises_kb

from database.graphics_queries import get_weight_history, get_water_history, get_user_exercises_with_stats, get_exercise_history_by_id
from utils.graphs import generate_weight_chart, generate_water_chart, generate_exercise_chart

router = Router()


@router.callback_query(F.data == "profile_history")
async def show_history_menu(callback: types.CallbackQuery):
    await callback.message.edit_text(
        text="📊 Выберите, какую историю прогресса вы хотите посмотреть:",
        reply_markup=get_profile_history_kb()
    )
    await callback.answer()


@router.callback_query(F.data == "show_weight_log")
async def handle_show_weight_graph(callback: types.CallbackQuery, db: aiosqlite.Connection):
    user_id = callback.from_user.id
    data = await get_weight_history(db, user_id)

    if not data or len(data) < 2:
        await callback.answer(
            text="⚠️ Недостаточно данных. Внесите вес хотя бы дважды.",
            show_alert=True
        )
        return

    await callback.answer("Создаю график веса...")

    try:
        chart_buffer = await generate_weight_chart(data)
        photo = BufferedInputFile(chart_buffer.read(), filename="weight_chart.png")

        await callback.message.answer_photo(
            photo=photo,
            caption="📈 График динамики изменения вашего веса."
        )
    except Exception as e:
        await callback.message.answer("Не удалось построить график. Попробуйте позже.")
        print(f"Ошибка построения графика веса: {e}")


@router.callback_query(F.data == "show_water_log")
async def handle_show_water_graph(callback: types.CallbackQuery, db: aiosqlite.Connection):
    user_id = callback.from_user.id
    data = await get_water_history(db, user_id, limit=7)

    if not data:
        await callback.answer(
            text="⚠️ У вас пока нет записей о выпитой воде.",
            show_alert=True
        )
        return

    await callback.answer("Создаю график воды...")

    try:
        chart_buffer = await generate_water_chart(data)
        photo = BufferedInputFile(chart_buffer.read(), filename="water_chart.png")

        await callback.message.answer_photo(
            photo=photo,
            caption="💧 Статистика потребления воды за последние дни.",
            reply_markup=get_profile_history_kb()
        )
    except Exception as e:
        await callback.message.answer("Не удалось построить график воды.")
        print(f"Ошибка графика воды: {e}")


@router.callback_query(F.data == "show_exercise_log")
async def handle_show_exercises_menu(callback: types.CallbackQuery, db: aiosqlite.Connection):
    user_id = callback.from_user.id
    exercises = await get_user_exercises_with_stats(db, user_id)

    if not exercises:
        await callback.answer(
            text="⚠️ У вас пока нет упражнений с достаточным количеством тренировок (нужно выполнить упражнение хотя бы в двух разных тренировках).",
            show_alert=True
        )
        return

    await callback.message.edit_text(
        text="💪 Выберите упражнение, чтобы посмотреть график изменения рабочих весов:",
        reply_markup=get_user_exercises_kb(exercises)
    )
    await callback.answer()


@router.callback_query(F.data.startswith("ex_graph_"))
async def handle_generate_specific_exercise_graph(callback: types.CallbackQuery, db: aiosqlite.Connection):
    user_id = callback.from_user.id
    exercise_id = int(callback.data.split("_")[2])

    await callback.answer("Строю график...")
    exercise_name, data = await get_exercise_history_by_id(db, user_id, exercise_id)

    try:
        chart_buffer = await generate_exercise_chart(exercise_name, data)
        photo = BufferedInputFile(chart_buffer.read(), filename="exercise_chart.png")

        await callback.message.answer_photo(
            photo=photo,
            caption=f"📈 Динамика максимального веса в упражнении: {exercise_name}",
            reply_markup=get_profile_history_kb()
        )
    except Exception as e:
        await callback.message.answer("Не удалось построить график.")
        print(f"Ошибка графика тренировок: {e}")