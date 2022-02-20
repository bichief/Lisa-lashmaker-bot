from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from data import config

link = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text='Ознакомиться с работами', url=config.LINK)
    ]
])