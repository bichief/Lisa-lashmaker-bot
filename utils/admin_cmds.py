import os

import aiofiles

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
        await f.write('ID | Название | День недели | Время')
        await f.write('\n')
        for row in rows:
            await f.write(row)
            await f.write('\n')
        f.close()