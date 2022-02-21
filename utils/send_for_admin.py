
from loader import bot


async def new_customer(name, phone):
    await bot.send_message(chat_id=417436565,
                           text=f'К вам записалась {name}\n'
                                f'Контактный номер - {phone}\n\n'
                                f'Созвонитесь, дабы узнать подробности :)')