import re

from aiogram import types
from aiogram.dispatcher.filters import Text

from keyboards.inline.date_markup import date_markup
from keyboards.inline.lash_markup import markup
from keyboards.inline.time_markup import time_markup
from loader import dp
from states.get_contacts import GetContacts
from utils import validators_phone
from utils.db_api.commands.customers import get_info, update_phone, update_name, update_service_customer
from utils.db_api.commands.service import check_rows, get_info_service
from utils.db_api.commands.time_service import update_time_state
from utils.validators_phone import validator


@dp.message_handler(Text(equals='Записаться'))
async def recording(message: types.Message):
    if await check_rows() is True:
        await message.answer('К сожалению, услуги отсутствуют.')
    else:
        keyboard = await markup()
        await message.answer('Выберите необходимую вам услугу:', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='service_'))
async def get_service(call: types.CallbackQuery):
    global msg
    global reg
    reg = call.data.split('_')
    information = await get_info_service(name=reg[1])
    row = information.split('&')

    keyboard = await date_markup(name=reg[1])

    await call.message.answer(f'Название - {row[0]}\n'
                              f'Описание - {row[1]}\n'
                              f'Цена - {row[2]}\n'
                              f'Нажмите на удобное для вас время ниже:', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='date_'))
async def get_time_for_service(call: types.CallbackQuery):
    global data
    data = call.data.split('_')
    keyboard = await time_markup(name=reg[1])

    await call.message.answer('Выберите удобное для вас время.', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='time_'))
async def get_service(call: types.CallbackQuery):
    global regex
    regex = call.data.split('_')

    check = await get_info(call.from_user.id)
    if check.split('&')[0] == 'none':
        await call.message.answer(f'Отлично, Вы записываетесь на {regex[2]}\n'
                                  f'Дата записи: {data[1]} - {regex[1]}\n\n'
                                  f'Напишите свой номер телефона\n'
                                  f'Пример: +79051235467')
        await GetContacts.first()
    else:

        await call.message.answer(f'Отлично, Вы записываетесь на {regex[2]}\n'
                                  f'Дата записи: {regex[1]}\n\n'
                                  f'В скором времени с вами свяжутся :)')
        await update_time_state(time_id=regex[3])
        await update_service_customer(telegram_id=call.from_user.id, name_service=regex[2], time_service=regex[1])


@dp.message_handler(state=GetContacts.Phone)
async def get_phone(message: types.Message):
    text = message.text

    phone = await validator(phone=text)

    if phone:
        await message.answer('Отлично, теперь введите Ваше имя.')
        await update_phone(telegram_id=message.from_user.id, phone=text)
        await GetContacts.Name.set()
    else:
        await message.answer('Номер введён неверно, попробуйте еще раз.')
        await GetContacts.Phone.set()


@dp.message_handler(state=GetContacts.Name)
async def get_name(message: types.Message):
    name = message.text
    await update_name(telegram_id=message.from_user.id, name=name)
    await message.answer('Отлично!\n'
                         'С вами скоро свяжутся.')
    await update_time_state(time_id=regex[3])
