import aiofiles
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.utils.exceptions import BotBlocked

from data import config
from handlers.users.start import start_cmd
from keyboards.default.admin_markup import admin, edit_db_time, add_db_time, edit_service_db_key
from loader import dp, bot
from states.admin import Admin
from utils.admin_cmds import insert_txt, insert_txt_delete, insert_service_add
from utils.db_api.commands.customers import get_users
from utils.db_api.commands.service import add_service_to_db, delete_service_db
from utils.db_api.commands.time_service import time_add_db, delete_time


@dp.message_handler(Command('login'))
async def admin_login(message: types.Message):
    global msg
    msg = await message.answer('Вы успешно вошли в админ-панель.\n\n'
                               'Выберите необходимый функционал на клавиатуре', reply_markup=admin)


@dp.message_handler(Text(equals='Вернуться в меню'))
async def go_menu(message):
    await start_cmd(message)


@dp.message_handler(Text(equals='Время'))
async def edit_time(message: types.Message):
    await message.answer('Выберите необходимое действие со временем записи.', reply_markup=edit_db_time)


@dp.message_handler(Text(equals='Добавить время'))
async def add_time(message: types.Message):
    await message.answer('Выберите день, в котором Вы бы хотели добавить время для записи.', reply_markup=add_db_time)


@dp.callback_query_handler(Text(startswith='edit_'))
async def second_step_add_time(call: types.CallbackQuery):
    global day
    regex = call.data.split('_')
    day = regex[1]  # день
    await insert_txt()
    async with aiofiles.open('service.txt', mode='rb') as f:
        await bot.send_document(call.from_user.id, f,
                                caption='Введите название Услуги, для которой необходимо изменить время')
        f.close()
    await Admin.first()


@dp.message_handler(state=Admin.ID)
async def state_machine_add_time(message: types.Message):
    global service_name
    service_name = message.text  # ид товара
    await message.answer('Хорошо, теперь отправьте мне время ЧЕРЕЗ запятую БЕЗ пробела.\n\n'
                         'Пример: 9:30,10:00,11:00')
    await Admin.Time.set()


@dp.message_handler(state=Admin.Time)
async def help_me_pls(message: types.Message, state: FSMContext):
    time = message.text.split(',')

    for row in time:
        await time_add_db(day=day, service_name=service_name, time=row)

    await message.answer('Время успешно добавлено!', reply_markup=admin)
    await state.reset_state()


@dp.message_handler(Text(equals='Удалить время'))
async def delete_db_time(message: types.Message):
    await insert_txt_delete()
    async with aiofiles.open('time.txt', mode='rb') as f:
        await bot.send_document(message.chat.id, f,
                                caption='Введите ID, который необходимо удалить\n\n'
                                        '(один за раз)')
        f.close()
    await Admin.Time_id.set()


@dp.message_handler(state=Admin.Time_id)
async def delete_second(message: types.Message, state: FSMContext):
    time_id = message.text
    await delete_time(time_id)
    await message.answer('Время успешно удалено!')
    await state.reset_state()


@dp.message_handler(Text(equals='Услуги'))
async def add_service(message: types.Message):
    await message.answer('Хорошо.\n'
                         'Выберите необходимое действие с услугами.', reply_markup=edit_service_db_key)


@dp.message_handler(Text(equals='Добавить услугу'))
async def add_db_service(message: types.Message):
    await message.answer('Введите текс для добавления услуги в следующем формате!\n\n'
                         'Название|Описание|Цена')
    await Admin.Add_service.set()


@dp.message_handler(state=Admin.Add_service)
async def service_commit(message: types.Message, state: FSMContext):
    service = message.text.split('|')
    await add_service_to_db(name=service[0], desc=service[1], price=service[2])
    await message.answer('Услуга была успешно добавлена!')
    await state.reset_state(with_data=False)


@dp.message_handler(Text(equals='Удалить услугу'))
async def edit_service(message: types.Message):
    await insert_service_add()
    async with aiofiles.open('service.txt', mode='rb') as f:
        await bot.send_document(message.chat.id, f,
                                caption='Введите ID, который необходимо удалить \n\n'
                                        '(один за раз)')
        f.close()
    await Admin.Delete_service.set()


@dp.message_handler(state=Admin.Delete_service)
async def delete_service(message: types.Message, state: FSMContext):
    service_id = message.text
    await delete_service_db(service_id)
    await message.answer('Услуга была успешно удалена!')
    await state.reset_state()

@dp.message_handler(Text(equals='Рассылка пользователям'))
async def for_all_users(message: types.Message):
    await message.answer('Супер, введите сообщение для рассылки.')
    await Admin.For_all.set()

@dp.message_handler(state=Admin.For_all)
async def send_for_all(message: types.Message, state: FSMContext):
    text = message.text

    allowed = 0
    blocked = 0

    array = await get_users()
    print(array)
    try:
        for row in array:
            await bot.send_message(
                chat_id=row,
                text=text
            )
            allowed += 1
    except BotBlocked:
        blocked += 1

    await message.answer('Сообщение было успешно доставлено.\n\n'
                         f'Отправилось - {allowed} пользователям\n'
                         f'Не отправилось - {blocked} пользователям')
    await state.reset_state()
