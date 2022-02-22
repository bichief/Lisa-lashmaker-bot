from aiogram.types import ReplyKeyboardMarkup, KeyboardButton, InlineKeyboardMarkup, InlineKeyboardButton

admin = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Время'),
        KeyboardButton(text='Услуги')
    ],
    [
        KeyboardButton(text='Пользователи')
    ],
    [
        KeyboardButton(text='Списать баллы')
    ],
    [
        KeyboardButton(text='Рассылка пользователям')
    ],
    [
        KeyboardButton(text='Вернуться в меню')
    ]
])

edit_db_time = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Добавить время')
    ],
    [
        KeyboardButton(text='Удалить время')
    ],
    [
        KeyboardButton(text='Вернуться в меню')
    ]
])

add_db_time = InlineKeyboardMarkup(row_width=1, inline_keyboard=[
    [
        InlineKeyboardButton(text='📍 Понедельник', callback_data='edit_monday')
    ],
    [
        InlineKeyboardButton(text='📍 Вторник', callback_data='edit_tuesday')
    ],
    [
        InlineKeyboardButton(text='📍 Среда', callback_data='edit_wednesday')
    ],
    [
        InlineKeyboardButton(text='📍 Четверг', callback_data='edit_thursday')
    ],
    [
        InlineKeyboardButton(text='📍 Пятница', callback_data='edit_friday')
    ],
    [
        InlineKeyboardButton(text='📍 Суббота', callback_data='edit_saturday')
    ],
    [
        InlineKeyboardButton(text='📍 Воскресенье', callback_data='edit_sunday')
    ],
])

edit_service_db_key = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Добавить услугу')
    ],
    [
        KeyboardButton(text='Удалить услугу')
    ]
])

users_markup = ReplyKeyboardMarkup(resize_keyboard=True, keyboard=[
    [
        KeyboardButton(text='Все пользователи')
    ],
    [
        KeyboardButton(text='Найти пользователя по номеру телефона')
    ],
    [
        KeyboardButton(text='Добавить пользователя в ЧС')
    ]
])