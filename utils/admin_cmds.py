import os

import aiofiles

from loader import bot
from utils.db_api.commands.customers import get_from_customers, collect_all_information, finding_by_phone, \
    blocked_users_check
from utils.db_api.commands.service import get_service_id
from utils.db_api.commands.time_service import get_time_id


async def insert_txt():
    rows = await get_service_id()

    if os.path.exists('service.txt'):
        os.remove('service.txt')

    async with aiofiles.open('service.txt', mode='a', encoding='utf-8') as f:
        await f.write('ID | Название')
        await f.write('\n')
        for row in rows:
            await f.write(row)
            await f.write('\n')
        f.close()


async def insert_txt_delete():
    rows = await get_time_id()

    if os.path.exists('time.txt'):
        os.remove('time.txt')

    async with aiofiles.open('time.txt', mode='a', encoding='utf-8') as f:
        await f.write('ID | День недели | Время')
        await f.write('\n')
        for row in rows:
            await f.write(row)
            await f.write('\n')
        f.close()


async def insert_service_add():
    rows = await get_service_id()

    if os.path.exists('service.txt'):
        os.remove('service.txt')

    async with aiofiles.open('service.txt', mode='a', encoding='utf-8') as f:
        await f.write('ID | Название | Описание | Цена')
        await f.write('\n')
        await f.write('\n')
        for row in rows:
            await f.write(row)
            await f.write('\n')
        f.close()


async def insert_clients_all():
    rows = await get_from_customers()

    if os.path.exists('clients.txt'):
        os.remove('clients.txt')

    async with aiofiles.open('clients.txt', mode='a', encoding='utf-8') as f:
        await f.write('ID | Имя | Номер | Время | День | Название | Баланс')
        await f.write('\n')
        await f.write('\n')
        for row in rows:
            await f.write(row)
            await f.write('\n')
        f.close()


async def insert_all_about_users():
    rows = await collect_all_information()

    if os.path.exists('clients.txt'):
        os.remove('clients.txt')

    async with aiofiles.open('clients.txt', mode='a', encoding='utf-8') as f:
        for row in rows:
            await f.write(row)
            await f.write('\n')
            await f.write('\n')
        f.close()


async def insert_by_phone(phone, message):
    rows = await finding_by_phone(phone)

    if rows is False:
        await message.answer('Ошибка, пользователя с таким номером в Базе Данных не существует.')
    else:

        if os.path.exists('clients.txt'):
            os.remove('clients.txt')

        async with aiofiles.open('clients.txt', mode='a', encoding='utf-8') as f:
            try:
                for row in rows:
                    await f.write(row)
                    await f.write('\n')
                    await f.write('\n')
            except:
                pass
            f.close()

        async with aiofiles.open('clients.txt', mode='rb') as f:
            await bot.send_document(message.chat.id, f,
                                    caption='Все данные об пользователе находится в файле.')
            f.close()


async def insert_blocked_users():
    rows = await blocked_users_check()

    if os.path.exists('block.txt'):
        os.remove('block.txt')

    async with aiofiles.open('block.txt', mode='a', encoding='utf-8') as f:
        await f.write('ID | TG_ID | Имя | Номер')
        await f.write('\n')
        for row in rows:
            await f.write(row)
            await f.write('\n')
            await f.write('\n')
        f.close()