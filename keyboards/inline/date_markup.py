from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

date = InlineKeyboardMarkup(row_width=2, inline_keyboard=[
    [
        InlineKeyboardButton(text='Понедельник', callback_data='date_monday'),
    ],
    [
        InlineKeyboardButton(text='Вторник', callback_data='date_tuesday'),
    ],
    [
        InlineKeyboardButton(text='Среда', callback_data='date_wednesday'),
    ],
    [
        InlineKeyboardButton(text='Четверг', callback_data='date_thursday'),
    ],
    [
        InlineKeyboardButton(text='Пятница', callback_data='date_friday'),
    ],
    [
        InlineKeyboardButton(text='Суббота', callback_data='date_saturday'),
    ],
    [
        InlineKeyboardButton(text='Вокресенье', callback_data='date_sunday')
    ]
])
