from sqlalchemy import select, update
from sqlalchemy.exc import IntegrityError

from utils.db_api.base import async_sessionmaker
from utils.db_api.models.customers import Customers


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


async def update_service_customer(telegram_id, name_service, time_service):
    async with async_sessionmaker() as session:
        info = (
            update(Customers).where(Customers.telegram_id == telegram_id).values(name_service=name_service,
                                                                                 time_service=time_service)
        )
        await session.execute(info)
        await session.commit()
