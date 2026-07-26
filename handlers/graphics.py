import aiosqlite
from aiogram import Router, F, types
from aiogram.types import BufferedInputFile

from keyboards.profile_kb import get_profile_history_kb, get_profile_main_kb

from database.graphics_queries import get_weight_history, get_water_history
from utils.graphs import generate_weight_chart, generate_water_chart

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