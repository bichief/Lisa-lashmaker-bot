from sqlalchemy import Column, Integer, BigInteger, String, sql, ForeignKey, ForeignKeyConstraint

from utils.db_api.base import Base


class Time(Base):
    __tablename__ = 'time_service'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    service_name = Column(String())
    day = Column(String())
    time = Column(String())
    state = Column(String(), default='false')

    query: sql.Select