from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

import utils.db_api.commands.service as db


async def markup():
    products = InlineKeyboardMarkup(row_width=2)

    array = await db.get_name_service()

    for row in array:
        btn = InlineKeyboardButton(text=f'{row}', callback_data=f'service_{row}')
        products.add(btn)
    return products

