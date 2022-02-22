import asyncio

from aiogram import types
from aiogram.dispatcher.filters.builtin import CommandStart, Text

from keyboards.default.menu_markup import main_menu
from keyboards.inline.link_markup import link

import utils.db_api.commands.customers as cs
from loader import dp


@dp.message_handler(CommandStart())
async def start_cmd(message: types.Message):
        deep_link = message.get_args()

        await cs.add_customer(telegram_id=message.from_user.id)

        photo = 'AgACAgIAAxkBAAIC-WISndFP2HL-nK6SFVKQBgZRPN5sAAIEuTEb1rCYSEQtrmGZLBmCAQADAgADeQADIwQ'

        if deep_link == '':
            await message.answer_photo(photo,
                                       caption='🙋‍♀Пора закончить твои зависимые отношения с тушью, и я тебе в этом помогу!\n'
                                               '🙆‍♀Выбирай скорее дату и время, пока всё не разобрали!',
                                       reply_markup=main_menu)
        else:
            referral_name = await cs.get_referral_name(telegram_id=deep_link)
            await cs.insert_referral_name(telegram_id=message.from_user.id, referral_id=deep_link,
                                          referral_name=referral_name)
            await message.answer_photo(photo,
                                       caption='🙋‍♀Пора закончить твои зависимые отношения с тушью, и я тебе в этом помогу!\n'
                                               '🙆‍♀Выбирай скорее дату и время, пока всё не разобрали!\n\n'
                                               '👩‍💻Вы зарегестрировались по реферальной ссылке.\n'
                                               f'💁‍♀Имя вашего реферала - {referral_name}',
                                       reply_markup=main_menu)



@dp.message_handler(Text(equals='Где нас найти'))
async def location(message: types.Message):
    photo = 'AgACAgIAAxkBAAID1mITlDh6DPc7Dsmt0xXWLnOr16YcAAKduTEbg_2ZSNTPGnt1-IOJAQADAgADeQADIwQ'
    await message.answer_photo(photo, '🙆‍♀Вы можете нас найти по данному адресу:\n'
                                      'г. Тверь, Пр-т Чайковского 28/2, БЦ Тверьгеофизика, 1 подъезд, 3 этаж, 315 кабинет')
    await asyncio.sleep(0.5)
    await message.answer_location(latitude='56.845135',
                                  longitude='35.904791')


@dp.message_handler(Text(equals='Портфолио'))
async def portfolio(message: types.Message):
    photo = 'AgACAgIAAxkBAAID2GITlFyPqfFVLK-hZmPXtSEH_ixPAAKeuTEbg_2ZSIF8GTODfd1_AQADAgADeQADIwQ'
    await message.answer_photo(photo, '🙆‍♀Если Вы хотите ознакомиться с моими работами, то нажмите на кнопку ниже.',
                               reply_markup=link)
    await message.answer(message.photo.file_id[-1])
