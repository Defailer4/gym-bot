from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup
from aiogram.utils.keyboard import InlineKeyboardBuilder

def get_profile_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="📊 История прогресса", callback_data="profile_history")],
        [InlineKeyboardButton(text="⚙️ Настроить цели", callback_data="profile_settings")],
    ])

def get_profile_settings_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💧 Цель воды", callback_data="edit_goal_water"),
            InlineKeyboardButton(text="⚖️ Цель веса", callback_data="edit_goal_weight")
        ],
        [InlineKeyboardButton(text="🔙 Назад в профиль", callback_data="back_to_profile")]
    ])

def get_profile_history_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="⚖️ График веса", callback_data="show_weight_log"),
            InlineKeyboardButton(text="💧 Лог воды", callback_data="show_water_log")
        ],
        [
            InlineKeyboardButton(text="💪 Веса в упражнениях", callback_data="show_exercise_log")
        ],
        [InlineKeyboardButton(text="🔙 Назад в профиль", callback_data="back_to_profile")]
    ])

def get_user_exercises_kb(exercises_list: list) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()
    for ex_id, ex_name in exercises_list:
        builder.button(text=ex_name, callback_data=f"ex_graph_{ex_id}")
    builder.adjust(1)
    builder.row(InlineKeyboardButton(text="🔙 Назад в меню истории", callback_data="profile_history"))
    return builder.as_markup()