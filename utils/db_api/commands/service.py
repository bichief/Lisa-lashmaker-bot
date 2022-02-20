from sqlalchemy import select
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
        pass

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