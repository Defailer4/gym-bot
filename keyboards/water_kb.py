from aiogram.utils.keyboard import InlineKeyboardBuilder
from aiogram.types import InlineKeyboardMarkup

def get_water_kb():
    builder = InlineKeyboardBuilder()

    builder.button(text="+ 250 мл", callback_data="water_add_250")
    builder.button(text="+ 500 мл", callback_data="water_add_500")

    builder.button(text="↩️ Отменить последнее", callback_data="water_rollback")

    builder.adjust(2,1)

    return builder.as_markup()