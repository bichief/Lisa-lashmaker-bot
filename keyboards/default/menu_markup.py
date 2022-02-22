from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

main_menu = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Записаться')
    ],
    [
        KeyboardButton(text='Реферальная система')
    ],
    [
        KeyboardButton(text='Где нас найти')
    ],
    [
        KeyboardButton(text='Портфолио')
    ]
])

menu = InlineKeyboardMarkup(row_width=3, inline_keyboard=[
    [
        InlineKeyboardButton(text='test', callback_data='test')
    ]
])