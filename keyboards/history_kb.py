from aiogram.utils.keyboard import InlineKeyboardBuilder, InlineKeyboardMarkup
from datetime import datetime

MONTHS_RU = {
    "01": "Январь", "02": "Февраль", "03": "Март", "04": "Апрель",
    "05": "Май", "06": "Июнь", "07": "Июль", "08": "Август",
    "09": "Сентябрь", "10": "Октябрь", "11": "Ноябрь", "12": "Декабрь"
}


def get_history_kb(workouts, show_archive_btn: bool = True) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for w_id, start_time in workouts:
        try:
            dt = datetime.strptime(start_time, "%Y-%m-%d %H:%M:%S")
            date_str = dt.strftime("%d.%m в %H:%M")
        except ValueError:
            date_str = start_time[:16]

        builder.button(text=f"📅 {date_str}", callback_data=f"hist_view_{w_id}")

    if show_archive_btn:
        builder.button(text="🗄 Архив месяцев", callback_data="hist_archive")
    else:
        builder.button(text="🔙 К списку месяцев", callback_data="hist_archive")

    builder.adjust(1)
    return builder.as_markup()


def get_months_archive_kb(months) -> InlineKeyboardMarkup:
    builder = InlineKeyboardBuilder()

    for ym in months:
        year, month_num = ym.split("-")  
        month_name = MONTHS_RU.get(month_num, month_num)

        builder.button(text=f"📂 {month_name} {year}", callback_data=f"hist_month_{ym}")

    builder.adjust(1)
    return builder.as_markup()