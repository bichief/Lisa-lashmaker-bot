from sqlalchemy import select, delete
from sqlalchemy.exc import IntegrityError

from utils.db_api.base import async_sessionmaker
from utils.db_api.models.service import Service


async def get_name_service():
    try:
        array = []

        async with async_sessionmaker() as session:
            name = select(Service.name)

            result = await session.execute(name)

            for row in result.scalars():
                if row not in array:
                    array.append(row)
            return array
    except IntegrityError:
        print('ERROR!!')

async def check_rows():
    rows = await get_name_service()
    if len(rows) == 0:
        return True
    else:
        return rows


async def get_info_service(name):
    async with async_sessionmaker() as session:
        info = select(Service).where(Service.name == name)

        result = await session.execute(info)

        for row in result.scalars():
            return f'{row.name}&{row.description}&{row.price}'

async def get_service_id():
    array = []
    async with async_sessionmaker() as session:
        info = select(Service)

        result = await session.execute(info)

        for row in result.scalars():
            array.append(f'{row.id} | {row.name}')
        return array


async def get_service_all():
    array = []
    async with async_sessionmaker() as session:
        info = select(Service)

        result = await session.execute(info)

        for row in result.scalars():
            array.append(f'{row.id} | {row.name} | {row.description} | {row.price}')
        return array

async def add_service_to_db(name, desc, price):
    async with async_sessionmaker() as session:
        await session.merge(Service(name=name, description=desc, price=int(price)))
        await session.commit()

async def delete_service_db(service_id):
    async with async_sessionmaker() as session:
        info = (
            delete(Service).where(Service.id == int(service_id))
        )
        await session.execute(info)
        await session.commit()
