import re

from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text
from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from keyboards.inline.date_markup import date
from keyboards.inline.lash_markup import markup
from keyboards.inline.time_markup import time_markup
from loader import dp
from states.get_contacts import GetContacts
from utils.db_api.commands.customers import get_info, update_phone, update_name, update_service_customer
from utils.db_api.commands.service import check_rows, get_info_service
from utils.db_api.commands.time_service import delete_time
from utils.send_for_admin import new_customer
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
    await call.message.delete()
    global msg
    global reg
    reg = call.data.split('_')
    information = await get_info_service(name=reg[1])
    row = information.split('&')

    await call.message.answer(f'Название - {row[0]}\n'
                              f'Описание - {row[1]}\n'
                              f'Цена - {row[2]}\n'
                              f'Нажмите на удобное для вас время ниже:', reply_markup=date)


@dp.callback_query_handler(Text(startswith='date_'))
async def get_time_for_service(call: types.CallbackQuery):
    await call.message.delete()
    global data
    data = call.data.split('_')
    keyboard = await time_markup(name=reg[1], day=data[1])

    await call.message.answer('Выберите удобное для вас время.', reply_markup=keyboard)


@dp.callback_query_handler(Text(startswith='time_'))
async def get_service(call: types.CallbackQuery):
    await call.message.delete()
    global regex, msg
    regex = call.data.split('_')

    check = await get_info(call.from_user.id)
    if check.split('&')[0] == 'none':
        msg = await call.message.answer(f'Отлично, Вы записываетесь на {regex[2]}\n'
                                        f'Дата записи: {data[1]} - {regex[1]}\n\n'
                                        f'Напишите свой номер телефона\n'
                                        f'Пример: +79051235467')
        await GetContacts.first()
    else:

        msg = await call.message.answer(f'Отлично, Вы записываетесь на {regex[2]}\n'
                                        f'Дата записи: {regex[1]}\n\n'
                                        f'В скором времени с вами свяжутся :)')
        information = await get_info(telegram_id=call.from_user.id)
        await new_customer(name=information.split('&')[0], phone=information.split('&')[1])
        await delete_time(time_id=regex[3])
        await update_service_customer(telegram_id=call.from_user.id, name_service=regex[2], time_service=regex[1])


@dp.message_handler(state=GetContacts.Phone)
async def get_phone(message: types.Message):
    await msg.delete()
    global number, mess
    text = message.text

    phone = await validator(phone=text)

    if phone:
        mess = await message.answer('Отлично, теперь введите Ваше имя.')
        await update_phone(telegram_id=message.from_user.id, phone=text)
        number = text
        await GetContacts.Name.set()
    else:
        mess = await message.answer('Номер введён неверно, попробуйте еще раз.')
        await GetContacts.Phone.set()


@dp.message_handler(state=GetContacts.Name)
async def get_name(message: types.Message, state: FSMContext):
    await mess.delete()
    name = message.text
    await update_name(telegram_id=message.from_user.id, name=name)
    await message.answer('Отлично!\n'
                         'С вами скоро свяжутся.')
    await state.reset_state()
    await delete_time(time_id=regex[3])
    await new_customer(name, phone=number)
