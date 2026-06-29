from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()

builder.button(text="🏋️‍♂️ Начать тренировку")
builder.button(text="⚖️ Вес тела")
builder.button(text="💧 Вода")
builder.button(text="👤 Мой профиль")
builder.button(text="📜 История")

builder.adjust(1, 2, 2)
resize_keyboard = True
reply_markup = builder.as_markup()