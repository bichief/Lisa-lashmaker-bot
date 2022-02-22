from sqlalchemy import Column, Integer, String, sql

from utils.db_api.base import Base


class Time(Base):
    __tablename__ = 'time_service'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    day = Column(String())
    time = Column(String())

    query: sql.Select