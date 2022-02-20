from sqlalchemy import select, update

from utils.db_api.base import async_sessionmaker
from utils.db_api.models.dates import Dates
from utils.db_api.models.service import Service
from utils.db_api.models.time import Time


async def get_time(name):
    array = []
    async with async_sessionmaker() as session:
        info = select(Time).where(Time.service_name == name)

        result = await session.execute(info)

        for row in result.scalars():
            if row.state == 'false':
                array.append(f'{row.time}&{row.id}')
            else:
                pass
        return array


async def get_time_state(name):
    async with async_sessionmaker() as session:
        array = []

        information = select(Time).where(Time.service_name == name)

        result = await session.execute(information)

        for row in result.scalars():
            array.append(row.state)
        return array


async def update_time_state(time_id):
    async with async_sessionmaker() as session:
        info = (
            update(Time).where(Time.id == int(time_id)).values(state='true')
        )
        await session.execute(info)
        await session.commit()


async def get_date(name):
    array = []
    async with async_sessionmaker() as session:
        info = select(Dates).where(Dates.service_name == name)

        result = await session.execute(info)

        for row in result.scalars():
            array.append(row.date)
        return array