from aiogram import types
from aiogram.dispatcher import FSMContext
from aiogram.dispatcher.filters import Text

from keyboards.inline.date_markup import date_keyboard
from keyboards.inline.lash_markup import markup
from keyboards.inline.time_markup import time_markup
from loader import dp
from states.get_contacts import GetContacts
from utils.db_api.commands.customers import get_info, update_phone, update_name, update_date, update_time, \
    update_service_name, get_all_from_customers, update_referral_balance
from utils.db_api.commands.service import check_rows, get_info_service
from utils.db_api.commands.time_service import delete_time
from utils.send_for_admin import new_customer
from utils.validators_phone import validator


@dp.message_handler(Text(equals='Записаться'))
async def recording(message: types.Message):
    try:
        if await check_rows() is True:
            await message.answer('💁‍♀К сожалению, услуги отсутствуют.')
        else:
            keyboard = await markup()

            photo = 'AgACAgIAAxkBAAIDzGITkqgqVjG11a87Tq-B21vxRdiuAAKNuTEbg_2ZSNsHfH_VyRj5AQADAgADeQADIwQ'

            await message.answer_photo(photo=photo, caption='💁‍♀Предлагаю тебе выбрать желаемый эффект:',
                                       reply_markup=keyboard)
    except:
        pass


@dp.callback_query_handler(Text(startswith='service_'))
async def get_service(call: types.CallbackQuery):
    try:
        await call.message.delete()
        global msg, super_msg
        global reg

        reg = call.data.split('_')
        information = await get_info_service(name=reg[1])

        await update_service_name(telegram_id=call.from_user.id, service_name=reg[1])
        row = information.split('&')

        photo = 'AgACAgIAAxkBAAID1GITkuQDWdAGXWNvuuAEstuVFmzIAAKYuTEbg_2ZSNQ_l4W7n_W8AQADAgADeQADIwQ'

        super_msg = await call.message.answer_photo(photo, f'💁‍♀Название услуги - <b>{row[0]}</b>\n\n'
                                                           f'{row[1]}\n\n'
                                                           f'💰Цена - <b>{row[2]} р.</b>\n\n'
                                                           f'📅Теперь выбери наиболее удобную дату для записи',
                                                    reply_markup=date_keyboard)
    except:
        pass


@dp.callback_query_handler(Text(startswith='date_'))
async def get_time_for_service(call: types.CallbackQuery):
    try:
        await call.message.delete()
        global data

        data = call.data.split('_')
        date = data[1]
        await update_date(telegram_id=call.from_user.id, data=date)

        keyboard = await time_markup(day=data[1])

        photo = 'AgACAgIAAxkBAAID0mITkrcLJKK2ydvsFX-BGFoczY5YAAKXuTEbg_2ZSBFUe-kL695VAQADAgADeQADIwQ'

        await call.message.answer_photo(photo,
                                        '🙆‍♀Выбери свободное время для записи', reply_markup=keyboard)
    except:
        pass


@dp.callback_query_handler(Text(startswith='time_'))
async def get_service(call: types.CallbackQuery):
    try:
        await call.message.delete()
        global regex, msg

        regex = call.data.split('_')
        time = regex[1]
        await update_time(telegram_id=call.from_user.id, time=time)

        check = await get_info(call.from_user.id)
        if check.split('&')[0] == 'none':
            photo = 'AgACAgIAAxkBAAIDzmITkq5sKtW7uVgGDdSamYtz2UZFAAKUuTEbg_2ZSEx6FYfv8YzNAQADAgADeQADIwQ'

            await call.message.answer_photo(photo=photo,
                                        caption='👩‍💻Для завершения записи укажи свой контактный номер телефона\n'
                                                'Чтобы я связалась с тобой для уточнения всех деталей\n\n'
                                                'Пример: +79556950553')
            await GetContacts.first()
        else:
            photo = 'AgACAgIAAxkBAAID0GITkrOvSelYRu8oMS9giFUvhGqZAAKWuTEbg_2ZSJlLkFNCGglxAQADAgADeQADIwQ'

            await call.message.answer_photo(photo=photo, caption='Ты успешно записана!\n'
                                                             'Вскоре я свяжусь с тобой, чтобы подтвердить запись!\n'
                                                             'Надеюсь вскоре увидеть тебя в своем уютном кабинете! 🤗')
            array = await get_all_from_customers(telegram_id=call.from_user.id)

            req = array.split('&')

            name_client = req[0]
            phone = req[1]
            time = req[2]
            day = req[3]
            service_name = req[4]

            await update_referral_balance(telegram_id=call.from_user.id)
            await new_customer(name_client, phone=phone, time=time, day=day, service=service_name)
            await delete_time(time_id=regex[2])
    except:
        pass


@dp.message_handler(state=GetContacts.Phone)
async def get_phone(message: types.Message):
    try:
        global mess
        text = message.text

        phone = await validator(phone=text)

        if phone:
            mess = await message.answer('Отлично, теперь введите Ваше имя.')
            await update_phone(telegram_id=message.from_user.id, phone=text)
            await GetContacts.Name.set()
        else:
            mess = await message.answer('Номер введён неверно, попробуйте еще раз.')
            await GetContacts.Phone.set()
    except:
        pass


@dp.message_handler(state=GetContacts.Name)
async def get_name(message: types.Message, state: FSMContext):
    try:
        await mess.delete()

        name = message.text
        await update_name(telegram_id=message.from_user.id, name=name)

        photo = 'AgACAgIAAxkBAAID0GITkrOvSelYRu8oMS9giFUvhGqZAAKWuTEbg_2ZSJlLkFNCGglxAQADAgADeQADIwQ'

        await message.answer_photo(photo=photo, caption='Ты успешно записана!\n'
                                                    'Вскоре я свяжусь с тобой, чтобы подтвердить запись!\n'
                                                    'Надеюсь вскоре увидеть тебя в своем уютном кабинете! 🤗')
        await state.reset_state()
        await delete_time(time_id=regex[2])
        await update_referral_balance(telegram_id=message.from_user.id)

        array = await get_all_from_customers(telegram_id=message.from_user.id)

        information = array.split('&')

        name_client = information[0]
        phone = information[1]
        time = information[2]
        day = information[3]
        service_name = information[4]

        await new_customer(name_client, phone=phone, time=time, day=day, service=service_name)
    except:
        pass


@dp.callback_query_handler(Text(equals='back'))
async def go_back(call: types.CallbackQuery):
    await super_msg.delete()
    await recording(message=call.message)
