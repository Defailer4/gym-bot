from aiogram.types import InlineKeyboardButton, InlineKeyboardMarkup

def get_cancel_weight_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="❌ Отменить ввод", callback_data="cancel_weight_input")]
    ])

def get_weight_rollback_kb() -> InlineKeyboardMarkup:
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="Откатить запись ↩️", callback_data="rollback_last_weight")]
    ])