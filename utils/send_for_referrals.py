from aiogram import types

from loader import bot


async def send_ref(telegram_id, name):
    await bot.send_message(
        chat_id=telegram_id,
        text=f'Через вашу ссылку записалась {name}\n'
             f'Ваш баланс пополнен на 100 бонусов.'
    )