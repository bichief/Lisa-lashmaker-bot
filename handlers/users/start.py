import asyncio

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Text

from keyboards.default.menu_markup import menu
from keyboards.inline.lash_markup import markup
from keyboards.inline.link_markup import link
from keyboards.inline.time_markup import time_markup

import utils.db_api.commands.customers as cs
from loader import dp


@dp.message_handler(CommandStart())
async def start_cmd(message: types.Message):
    check_state = await cs.add_customer(telegram_id=message.from_user.id)
    if check_state is True:
        print('Уже есть в БД')
    else:
        await message.answer(f"Здесь вы увидете приветственное сообщение\n"
                             f"при команде /start, собственно\n\n"
                             f"Ниже прикреплена клавиатура, воспользуйтейсь ей для записи", reply_markup=menu)


@dp.message_handler(Text(equals='Где нас найти'))
async def location(message: types.Message):
    await message.answer('Вы можете нас найти по данному адресу:')
    await asyncio.sleep(0.5)
    await message.answer_location(latitude='54.7818',
                                  longitude='32.0401')


@dp.message_handler(Text(equals='Портфолио'))
async def portfolio(message: types.Message):
    await message.answer('примерный текст,\n\n'
                         'Если Вы хотите ознакомиться с моими работами, то нажмите на кнопку ниже :)',
                         reply_markup=link)


@dp.callback_query_handler(Text(equals='number_1'))
async def service(call: types.CallbackQuery):
    photo_link = 'https://ia41.ru/wp-content/uploads/2020/09/blobid1559890085161.jpg'
    await call.message.answer_photo(photo=photo_link,
                                    caption='Тут можно добавить фото, описание и цену услуги\n\n'
                                            'Чтобы записаться, нажмите на доступное время',
                                    reply_markup=time_markup)


@dp.callback_query_handler(Text(equals='test_time_14'))
async def service_time(call: types.CallbackQuery):
    await call.message.answer("Хорошо,\n"
                              "Отправьте мне свой номер телефона.\n"
                              "(необходимо единожды)\n\n"
                              "Затем запосить имя, внести в Базу Данных и все, клиент сможет сам записываться без указания контактов")
