
from loader import bot


async def new_customer(name, phone):
    await bot.send_message(chat_id=1955750981,
                           text=f'К вам записалась {name}\n'
                                f'Контактный номер - {phone}')