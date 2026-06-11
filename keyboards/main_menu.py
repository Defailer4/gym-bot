from aiogram.utils.keyboard import ReplyKeyboardBuilder

builder = ReplyKeyboardBuilder()

builder.button(text="🏋️ Начать тренировку")
builder.button(text="📊 Статистика")
builder.button(text="📜 История")

builder.adjust(1,1,1)

reply_markup = builder.as_markup()