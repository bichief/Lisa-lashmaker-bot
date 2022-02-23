import aiofiles
from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Command, Text
from aiogram.utils.exceptions import BotBlocked

from data import config
from handlers.users.start import start_cmd
from keyboards.default import menu_markup
from keyboards.default.admin_markup import admin, edit_db_time, add_db_time, edit_service_db_key, users_markup
from loader import dp, bot
from states.admin import Admin
from utils.admin_cmds import insert_txt_delete, insert_service_add, insert_clients_all, insert_all_about_users, \
    insert_by_phone, insert_blocked_users
from utils.db_api.commands.customers import get_users, deduct_referral_balance, update_block_status
from utils.db_api.commands.service import add_service_to_db, delete_service_db
from utils.db_api.commands.time_service import time_add_db, delete_time
from utils.validators_phone import validator


@dp.message_handler(Command('login'), user_id=[417436565, 1955750981])
async def admin_login(message: types.Message):
    global msg
    msg = await message.answer('Вы успешно вошли в админ-панель.\n\n'
                               'Выберите необходимый функционал на клавиатуре', reply_markup=admin)


@dp.message_handler(Text(equals='Вернуться в меню'), user_id=config.ADMINS)
async def go_menu(message: types.Message):
    await message.answer('Чтобы вернуться в меню, введите /start')


@dp.message_handler(Text(equals='Списать баллы'), user_id=config.ADMINS)
async def deduct_points(message: types.Message):
    await insert_clients_all()
    async with aiofiles.open('clients.txt', mode='rb') as f:
        await bot.send_document(message.chat.id, f,
                                caption='Введите ID клиента и сумму снятия бонусов, ЧЕРЕЗ пробел.\n\n'
                                        'Пример: 1 100')
        f.close()
    await Admin.Delete_balance.set()


@dp.message_handler(state=Admin.Delete_balance)
async def next_deduct_points(message: types.Message, state: FSMContext):
    data = message.text.split(' ')

    customer_id = data[0]
    amount = data[1]
    await deduct_referral_balance(customer_id, amount)

    await message.answer(f'<b>{amount}</b> баллов были успешно сняты!')
    await state.reset_state()


@dp.message_handler(Text(equals='Время'), user_id=config.ADMINS)
async def edit_time(message: types.Message):
    await message.answer('Выберите необходимое действие со временем записи.', reply_markup=edit_db_time)


@dp.message_handler(Text(equals='Добавить время'), user_id=config.ADMINS)
async def add_time(message: types.Message):
    await message.answer('Выберите день, в котором Вы бы хотели добавить время для записи.', reply_markup=add_db_time)


@dp.callback_query_handler(Text(startswith='edit_'), user_id=config.ADMINS)
async def second_step_add_time(call: types.CallbackQuery):
    global day
    regex = call.data.split('_')
    day = regex[1]  # день
    await call.message.answer('Введите время ЧЕРЕЗ запятную, БЕЗ пробелов.\n\n'
                              'Пример: 9:30,10:00,11:00')
    await Admin.ID.set()


@dp.message_handler(state=Admin.ID)
async def state_machine_add_time(message: types.Message, state: FSMContext):
    time = message.text.split(',')

    for row in time:
        await time_add_db(day=day, time=row)

    await message.answer('Время успешно добавлено!', reply_markup=admin)
    await state.reset_state()


@dp.message_handler(Text(equals='Удалить время'), user_id=config.ADMINS)
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


@dp.message_handler(Text(equals='Услуги'), user_id=config.ADMINS)
async def add_service(message: types.Message):
    await message.answer('Хорошо.\n'
                         'Выберите необходимое действие с услугами.', reply_markup=edit_service_db_key)


@dp.message_handler(Text(equals='Добавить услугу'), user_id=config.ADMINS)
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


@dp.message_handler(Text(equals='Удалить услугу'), user_id=config.ADMINS)
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


@dp.message_handler(Text(equals='Рассылка пользователям'), user_id=config.ADMINS)
async def for_all_users(message: types.Message):
    await message.answer('Супер, введите сообщение для рассылки.')
    await Admin.For_all.set()


@dp.message_handler(state=Admin.For_all)
async def send_for_all(message: types.Message, state: FSMContext):
    text = message.text

    allowed = 0
    blocked = 0

    array = await get_users()
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


@dp.message_handler(Text(equals='Пользователи'), user_id=config.ADMINS)
async def database_func(message: types.Message):
    await message.answer('В данном меню Вы можете просматривать данные пользователей, которые авторизованы в Боте.\n'
                         'Так же, заносить их в Черный Список', reply_markup=users_markup)

@dp.message_handler(Text(equals='Все пользователи'))
async def all_users_database(message: types.Message):
    await insert_all_about_users()
    async with aiofiles.open('clients.txt', mode='rb') as f:
        await bot.send_document(message.chat.id, f,
                                caption='Все данные о всех пользователях в Базе Данных находятся в этом файле.')
        f.close()

@dp.message_handler(Text(equals='Найти пользователя по номеру телефона'))
async def find_for_phone(message: types.Message):
    await message.answer('Хорошо, отправьте номер в следующем формате:\n'
                         '+79995554433')
    await Admin.Phone_find.set()

@dp.message_handler(state=Admin.Phone_find)
async def next_step_finding(message: types.Message, state: FSMContext):
    text = message.text

    phone = await validator(phone=text)

    if phone:
        await state.reset_state()
        await insert_by_phone(phone, message)
    else:
        await message.answer('Номер введен неверно, попробуйте еще раз.')

@dp.message_handler(Text(equals='Добавить пользователя в ЧС'))
async def add_blocked_user(message: types.Message):
    await insert_blocked_users()
    async with aiofiles.open('clients.txt', mode='rb') as f:
        await bot.send_document(message.chat.id, f,
                                caption='Хорошо, введите TG_ID пользователя\n')
        f.close()
    await Admin.Block.set()

@dp.message_handler(state=Admin.Block)
async def get_tg_id_block(message: types.Message, state: FSMContext):
    telegram_id = message.text
    await update_block_status(telegram_id)
    await message.answer(f'Пользователь {telegram_id} был успешно заблокирован.')
    await state.reset_state()
