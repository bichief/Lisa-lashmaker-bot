from aiogram import types
from aiogram.dispatcher.filters import Text

from loader import dp
from utils.db_api.commands.customers import get_balance


@dp.message_handler(Text(equals='Реферальная система'))
async def referral_message(message: types.Message):

    balance = await get_balance(telegram_id=message.from_user.id)

    await message.answer('Понравился мастер и хочешь приветси подругу?\n\n'
                         'Воспользуйся нашей реферальной системой, чтобы вы получили бонус в размере <b>100 баллов</b>!\n'
                         'Твоей подруге необходимо <b>записаться</b> на одну из доступных услуг и <b>прийти</b>, за это и начисляется бонус.\n\n'
                         f'Ваша ссылка для приглащения:\n'
                         f't.me/kdfksdfksd_bot?start={message.from_user.id}\n\n\n'
                         f'Ваш баланс: <b>{balance} баллов.</b>\n'
                         '(1 балл = 1 рубль)', disable_web_page_preview=True)
