from sqlalchemy import select, and_, delete

from utils.db_api.base import async_sessionmaker

from utils.db_api.models.time import Time


async def get_time(name, day):
    array = []
    async with async_sessionmaker() as session:
        info = select(Time).filter(and_(Time.service_name == name), (Time.day == day))

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


async def delete_time(time_id):
    async with async_sessionmaker() as session:
        info = (
            delete(Time).where(Time.id == int(time_id))
        )
        await session.execute(info)
        await session.commit()

async def time_add_db(day, service_name, time):
    async with async_sessionmaker() as session:
        await session.merge(Time(service_name=service_name, day=day, time=time, state='false'))
        await session.commit()

async def get_time_id():
    array = []
    async with async_sessionmaker() as session:
        info = select(Time)

        result = await session.execute(info)

        for row in result.scalars():
            array.append(f'{row.id} | {row.service_name} | {row.day} | {row.time}')
        return array

