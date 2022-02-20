from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.commands.time_service import get_date


async def date_markup(name):
    global btn
    time = InlineKeyboardMarkup(row_width=2)

    array = await get_date(name=name)
    if not array:
        btn = InlineKeyboardButton(text='Свободных дат нет.', callback_data='empty')
        time.add(btn)
        return time

    for row in array:
        btn = InlineKeyboardButton(text=f'{row}', callback_data=f'date_{row}_{name}')
        time.add(btn)
    return time