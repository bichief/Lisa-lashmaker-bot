from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from utils.db_api.commands.time_service import get_time


async def time_markup(day):
    global btn
    time = InlineKeyboardMarkup(row_width=2)
    array = await get_time(day=day)
    if not array:
        return False

    for row in array:
        regex = row.split('&')
        btn = InlineKeyboardButton(text=f'{regex[0]}', callback_data=f'time_{regex[0]}_{regex[1]}')
        time.add(btn)

    return time

# btn = InlineKeyboardButton(text=f'{row} - ЗАНЯТО', callback_data=f'time_{row}_{name}')
# time.add(btn)
