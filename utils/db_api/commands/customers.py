from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from utils.db_api.base import async_sessionmaker
from utils.db_api.models.customers import Customers
from utils.send_for_referrals import send_ref


async def add_customer(telegram_id):
    try:
        async with async_sessionmaker() as session:
            await session.merge(Customers(telegram_id=telegram_id))
            await session.commit()
    except IntegrityError:
        return True


async def get_info(telegram_id):
    try:
        async with async_sessionmaker() as session:
            info = select(Customers).where(Customers.telegram_id == telegram_id)

            result = await session.execute(info)

            for row in result.scalars():
                return f'{row.name}&{row.phone}'
    except AttributeError:
        print('+')
        return False


async def update_phone(telegram_id, phone):
    async with async_sessionmaker() as session:
        info = (
            update(Customers).where(Customers.telegram_id == telegram_id).values(phone=phone)
        )
        await session.execute(info)
        await session.commit()


async def update_name(telegram_id, name):
    async with async_sessionmaker() as session:
        info = (
            update(Customers).where(Customers.telegram_id == telegram_id).values(name=name)
        )
        await session.execute(info)
        await session.commit()


async def update_service_name(telegram_id, service_name):
    async with async_sessionmaker() as session:
        info = (
            update(Customers).where(Customers.telegram_id == telegram_id).values(service_name=service_name)
        )
        await session.execute(info)
        await session.commit()


async def update_date(telegram_id, data):
    async with async_sessionmaker() as session:
        info = (
            update(Customers).where(Customers.telegram_id == telegram_id).values(day=data)
        )
        await session.execute(info)
        await session.commit()


async def update_time(telegram_id, time):
    async with async_sessionmaker() as session:
        info = (
            update(Customers).where(Customers.telegram_id == telegram_id).values(time=time)
        )
        await session.execute(info)
        await session.commit()


async def get_all_from_customers(telegram_id):
    async with async_sessionmaker() as session:
        info = select(Customers).where(Customers.telegram_id == telegram_id)

        result = await session.execute(info)

        for row in result.scalars():
            return f'{row.name}&{row.phone}&{row.time}&{row.day}&{row.service_name}'


async def get_from_customers():
    async with async_sessionmaker() as session:
        info = select(Customers)
        array = []
        result = await session.execute(info)

        for row in result.scalars():
            array.append(
                f'{row.id} | {row.name} | {row.phone} | {row.time} | {row.day} | {row.service_name} | {row.referral_balance}')
        return array


async def collect_all_information():
    async with async_sessionmaker() as session:
        info = select(Customers)
        array = []
        result = await session.execute(info)

        for row in result.scalars():
            array.append(
                'ID | TG_ID | Имя | Номер | Заблокирован\n'
                f'{row.id} | {row.telegram_id} | {row.name} | {row.phone} | {row.blocked}\n\n'
                f'ID реферала | Имя реферала | Бонусный баланс\n'
                f'{row.referral} | {row.referral_name} | {row.referral_balance}\n\n'
                f'Запись (если none - значит, не записан)\n'
                f'День | Время | Название услуги\n'
                f'{row.day} | {row.time} | {row.service_name}')
        return array


async def get_users():
    try:
        array = []
        async with async_sessionmaker() as session:
            info = select(Customers.telegram_id)

            result = await session.execute(info)

            for row in result.scalars():
                array.append(row)
        return array
    except AttributeError:
        print('+')
        return False


async def get_referral_name(telegram_id):
    try:
        async with async_sessionmaker() as session:
            info = select(Customers).where(Customers.telegram_id == int(telegram_id))

            result = await session.execute(info)

            for row in result.scalars():
                return row.name
    except AttributeError:
        print('+')
        return False


async def insert_referral_name(telegram_id, referral_name, referral_id):
    try:
        async with async_sessionmaker() as session:
            info = (
                update(Customers).where(Customers.telegram_id == telegram_id).values(referral_name=referral_name,
                                                                                     referral=referral_id)
            )
            await session.execute(info)
            await session.commit()
    except:
        pass


async def update_referral_balance(telegram_id):
    async with async_sessionmaker() as session:
        data = select(Customers).where(Customers.telegram_id == int(telegram_id))

        result = await session.execute(data)

        for row in result.scalars():
            referral_id = row.referral
            print(referral_id)
            name = row.name

        select_balance = select(Customers).where(Customers.telegram_id == int(referral_id))

        information_balance = await session.execute(select_balance)

        for row in information_balance.scalars():
            old_balance = row.referral_balance

        new_balance = old_balance + 100

        info = (
            update(Customers).where(Customers.telegram_id == int(referral_id)).values(referral_balance=new_balance)
        )
        await session.execute(info)
        await session.commit()

        await send_ref(telegram_id=referral_id, name=name)


async def get_balance(telegram_id):
    try:
        async with async_sessionmaker() as session:
            info = select(Customers).where(Customers.telegram_id == int(telegram_id))

            result = await session.execute(info)

            for row in result.scalars():
                return row.referral_balance
    except AttributeError:
        print('+')
        return False


async def deduct_referral_balance(customer_id, amount):
    async with async_sessionmaker() as session:
        data = select(Customers).where(Customers.id == int(customer_id))

        result = await session.execute(data)

        for row in result.scalars():
            old_balance = row.referral_balance

        new_balance = old_balance - int(amount)

        info = (
            update(Customers).where(Customers.id == int(customer_id)).values(referral_balance=new_balance)
        )
        await session.execute(info)
        await session.commit()


async def finding_by_phone(phone):
    async with async_sessionmaker() as session:
        info = select(Customers).where(Customers.phone == phone)
        array = []
        result = await session.execute(info)

        for row in result.scalars():
            array.append(
                'ID | TG_ID | Имя | Номер | Заблокирован\n'
                f'{row.id} | {row.telegram_id} | {row.name} | {row.phone} | {row.blocked}\n\n'
                f'ID реферала | Имя реферала | Бонусный баланс\n'
                f'{row.referral} | {row.referral_name} | {row.referral_balance}\n\n'
                f'Запись (если none - значит, не записан)\n'
                f'День | Время | Название услуги\n'
                f'{row.day} | {row.time} | {row.service_name}')
        if len(array) == 0:
            return False
        else:
            return array


async def blocked_users_check():
    async with async_sessionmaker() as session:
        info = select(Customers)
        array = []
        result = await session.execute(info)

        for row in result.scalars():
            array.append(f'{row.id} | {row.telegram_id} | {row.name} | {row.phone}')
        return array


async def update_block_status(telegram_id):
    async with async_sessionmaker() as session:
        info = (
            update(Customers).where(Customers.telegram_id == int(telegram_id)).values(blocked='yes')
        )
        await session.execute(info)
        await session.commit()


async def get_blocked_users():
    async with async_sessionmaker() as session:
        info = select(Customers).where(Customers.blocked == 'yes')
        array = []
        result = await session.execute(info)

        for row in result.scalars():
            array.append(row.telegram_id)
        return array
