from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Записаться')
    ],
    [
        KeyboardButton(text='Где нас найти')
    ],
    [
        KeyboardButton(text='Портфолио')
    ]
])