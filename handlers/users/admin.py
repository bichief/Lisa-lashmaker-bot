import aiofiles
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text

from data import config
from handlers.users.start import start_cmd
from keyboards.default.admin_markup import admin, edit_db_time, add_db_time
from loader import dp, bot
from states.admin import Admin
from utils.admin_cmds import insert_txt, insert_txt_delete
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
