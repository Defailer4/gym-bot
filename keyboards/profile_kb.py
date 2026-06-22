from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_profile_main_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text = "⚙️ Настроить цели", callback_data = "profile_settings")],
    ])

def get_profile_settings_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [
            InlineKeyboardButton(text="💧 Цель воды", callback_data="edit_goal_water"),
            InlineKeyboardButton(text="⚖️ Цель веса", callback_data="edit_goal_weight")
        ],
        [InlineKeyboardButton(text="🔙 Назад в профиль", callback_data="back_to_profile")]
    ])