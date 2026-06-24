from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

def get_categories_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💪 Грудь", callback_data="cat_Грудь"),
            InlineKeyboardButton(text="🦵 Ноги", callback_data="cat_Ноги")
        ],
        [
            InlineKeyboardButton(text="🛡️ Спина", callback_data="cat_Спина"),
            InlineKeyboardButton(text="🪨 Плечи", callback_data="cat_Плечи")
        ],
        [
            InlineKeyboardButton(text="🏁 Завершить тренировку", callback_data="finish_workout")
        ]
    ])

def get_resume_workout_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="➡️ Продолжить", callback_data="resume_workout"),
            InlineKeyboardButton(text="❌ Сбросить и начать заново", callback_data="reset_workout")
        ]
    ])


def get_exercises_kb(exercises: list, category: str) -> InlineKeyboardMarkup:
    keyboard = []

    for exc_id, name in exercises:
        keyboard.append([
            InlineKeyboardButton(text=name, callback_data=f"exc_{exc_id}")
        ])

    keyboard.append([
        InlineKeyboardButton(text="➕ Добавить своё", callback_data=f"add_custom_{category}")
    ])
    keyboard.append([
        InlineKeyboardButton(text="↩️ К категориям", callback_data="back_to_categories")
    ])

    return InlineKeyboardMarkup(inline_keyboard=keyboard)

def get_active_exercise_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="↩️ Удалить последний", callback_data="undo_set")],
        [InlineKeyboardButton(text="🔄 Закончить упражнение", callback_data="finish_exercise")]
    ])