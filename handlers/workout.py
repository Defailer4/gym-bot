import aiosqlite
from aiogram import F, Router
from aiogram.types import Message, CallbackQuery, ReplyKeyboardRemove
from aiogram.fsm.state import StatesGroup, State
from aiogram.fsm.context import FSMContext

from keyboards.workout_kb import get_categories_kb, get_resume_workout_kb, get_exercises_kb, get_active_exercise_kb
from database.workout import get_active_workout, create_workout, get_exercises_by_category, cancel_workout, add_workout_set, get_workout_sets, undo_last_set, complete_workout, add_custom_exercise

router = Router()


class WorkoutStates(StatesGroup):
    choosing_category = State()
    choosing_exercise = State()
    waiting_for_set_data = State()
    adding_custom_exercise = State()


@router.message(F.text == "🏋️‍♂️ Начать тренировку")
async def start_workout_command(message: Message, db: aiosqlite.Connection, state: FSMContext):
    user_id = message.from_user.id

    active_workout_id = await get_active_workout(db, user_id)

    if active_workout_id:
        await state.update_data(workout_id=active_workout_id)

        await message.answer(
            "⚠️ <b>У тебя уже есть незавершенная тренировка!</b>\n\n"
            "Хочешь продолжить её или сбросить и начать новую?",
            reply_markup=get_resume_workout_kb(),
            parse_mode="HTML"
        )
        return

    workout_id = await create_workout(db, user_id)

    await state.update_data(workout_id=workout_id)
    await state.set_state(WorkoutStates.choosing_category)

    await message.answer(
        "🏋️‍♂️ <b>Тренировка началась!</b>\n\nВыбери мышечную группу для разминочки или рабочих подходов:",
        reply_markup=get_categories_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("cat_"), WorkoutStates.choosing_category)
async def process_category_choice(callback: CallbackQuery, db: aiosqlite.Connection, state: FSMContext):
    await callback.answer()

    category = callback.data.split("_")[1]
    user_id = callback.from_user.id

    await state.update_data(current_category=category)

    exercises = await get_exercises_by_category(db, category, user_id)

    await state.set_state(WorkoutStates.choosing_exercise)

    await callback.message.edit_text(
        f"📂 Категория: <b>{category}</b>\n\nВыбери упражнение из списка или добавь новое:",
        reply_markup=get_exercises_kb(exercises, category),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "back_to_categories", WorkoutStates.choosing_exercise)
async def back_to_categories_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(WorkoutStates.choosing_category)

    await callback.message.edit_text(
        "🏋️‍♂️ <b>Выбери мышечную группу:</b>",
        reply_markup=get_categories_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "resume_workout")
async def resume_workout_callback(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    await state.set_state(WorkoutStates.choosing_category)

    await callback.message.edit_text(
        "💪 <b>Отлично, продолжаем!</b>\n\nВыбери мышечную группу:",
        reply_markup=get_categories_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "reset_workout")
async def reset_workout_callback(callback: CallbackQuery, db: aiosqlite.Connection, state: FSMContext):
    await callback.answer()

    data = await state.get_data()
    old_workout_id = data.get("workout_id")

    if old_workout_id:
        await cancel_workout(db, old_workout_id)

    new_workout_id = await create_workout(db, callback.from_user.id)

    await state.update_data(workout_id=new_workout_id)
    await state.set_state(WorkoutStates.choosing_category)

    await callback.message.edit_text(
        "♻️ <b>Старая тренировка удалена. Начинаем с чистого листа!</b>\n\nВыбери мышечную группу:",
        reply_markup=get_categories_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data.startswith("exc_"), WorkoutStates.choosing_exercise)
async def process_exercise_choice(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    exercise_id = int(callback.data.split("_")[1])

    await state.update_data(exercise_id=exercise_id, active_message_id=callback.message.message_id)
    await state.set_state(WorkoutStates.waiting_for_set_data)

    text = (
        "🟢 <b>Упражнение началось!</b>\n\n"
        "Отправь вес и количество повторений через пробел.\n"
        "<i>Например: 100 8</i>\n\n"
        "📋 <b>Твои подходы:</b>\n"
        "<i>Пока пусто</i>"
    )

    await callback.message.edit_text(text, reply_markup=get_active_exercise_kb(), parse_mode="HTML")

@router.message(WorkoutStates.waiting_for_set_data)
async def process_set_input(message: Message, db: aiosqlite.Connection, state: FSMContext):
    try:
        parts = message.text.replace(",", ".").split()
        if len(parts) != 2:
            raise ValueError
        weight = float(parts[0])
        reps = int(parts[1])
        if weight < 0 or reps <= 0:
            raise ValueError
    except ValueError:
        msg = await message.answer("⚠️ Неверный формат! Введи два числа через пробел (например: 80 10).")
        await message.delete()
        return

    data = await state.get_data()
    workout_id = data.get("workout_id")
    exercise_id = data.get("exercise_id")
    active_msg_id = data.get("active_message_id")

    await add_workout_set(db, workout_id, exercise_id, weight, reps)
    await message.delete()

    sets = await get_workout_sets(db, workout_id, exercise_id)

    sets_text = "\n".join([f"{s[0]}. {s[1]} кг x {s[2]} повт." for s in sets])

    text = (
        "🟢 <b>Упражнение в процессе...</b>\n\n"
        "Отправь вес и повторения для следующего подхода (например: 100 8):\n\n"
        "📋 <b>Твои подходы:</b>\n"
        f"{sets_text}"
    )

    await message.bot.edit_message_text(
        text=text,
        chat_id=message.chat.id,
        message_id=active_msg_id,
        reply_markup=get_active_exercise_kb(),
        parse_mode="HTML"
    )

@router.callback_query(F.data == "undo_set", WorkoutStates.waiting_for_set_data)
async def undo_set_callback(callback: CallbackQuery, db: aiosqlite.Connection, state: FSMContext):
    data = await state.get_data()
    workout_id = data.get("workout_id")
    exercise_id = data.get("exercise_id")

    await undo_last_set(db, workout_id, exercise_id)

    sets = await get_workout_sets(db, workout_id, exercise_id)

    if not sets:
        sets_text = "<i>Пока пусто</i>"
    else:
        sets_text = "\n".join([f"{s[0]}. {s[1]} кг x {s[2]} повт." for s in sets])

    text = (
        "🟢 <b>Упражнение в процессе...</b>\n\n"
        "Отправь вес и повторения для следующего подхода (например: 100 8):\n\n"
        "📋 <b>Твои подходы:</b>\n"
        f"{sets_text}"
    )

    await callback.message.edit_text(text, reply_markup=get_active_exercise_kb(), parse_mode="HTML")
    await callback.answer("Последний подход удален 🗑️")

@router.callback_query(F.data == "finish_exercise", WorkoutStates.waiting_for_set_data)
async def finish_exercise_callback(callback: CallbackQuery, state: FSMContext):
    await state.set_state(WorkoutStates.choosing_category)

    await callback.message.edit_text(
        "✅ <b>Упражнение завершено!</b>\n\nВыбери следующую мышечную группу:",
        reply_markup=get_categories_kb(),
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data == "finish_workout")
async def finish_workout_callback(callback: CallbackQuery,db: aiosqlite.Connection, state: FSMContext):
    data = await state.get_data()
    workout_id = data.get("workout_id")

    if workout_id:
        await complete_workout(db, workout_id)
    await state.clear()

    await callback.message.edit_text(
        "🏁 <b>Тренировка успешно завершена!</b>\n\n"
        "Ты отлично отпахал сегодня. Отдыхай, восстанавливайся!💪🔥",
        parse_mode="HTML"
    )
    await callback.answer()

@router.callback_query(F.data.startswith("add_custom_"), WorkoutStates.choosing_exercise)
async def process_and_add_custom_exercise_btn(callback: CallbackQuery, state: FSMContext):
    await callback.answer()

    category =callback.data.split("_")[2]
    await state.update_data(current_category=category)

    await state.set_state(WorkoutStates.adding_custom_exercise)

    await callback.message.edit_text(
        f"📝 <b>Добавление упражнения в категорию «{category}»</b>\n\n"
        "Напиши название нового упражнения (например: <i>Сгибания Зоттмана</i>):",
        parse_mode="HTML"
    )

@router.message(WorkoutStates.adding_custom_exercise, F.text)
async def process_custom_exercise_name(message: Message, db:aiosqlite.Connection, state: FSMContext):
    new_name = message.text.strip()

    if len(new_name) < 2 or len(new_name) > 40:
        await message.answer("⚠️ Название должно быть от 2 до 40 символов. Попробуй еще раз:")
        return

    data = await state.get_data()
    category = data.get("current_category")
    user_id = message.from_user.id

    success = await add_custom_exercise(db, new_name, category, user_id)

    if not success:
        await message.answer("⚠️ Упражнение с таким названием уже существует! Придумай другое:")
        return

    await message.delete()
    exercises = await get_exercises_by_category(db, category, user_id)

    await state.set_state(WorkoutStates.choosing_exercise)

    await message.answer(
        f"✅ Упражнение <b>«{new_name}»</b> успешно добавлено!\n\n"
        f"📂 Категория: <b>{category}</b>\n\nВыбери упражнение из списка:",
        reply_markup=get_exercises_kb(exercises, category),
        parse_mode="HTML"
    )