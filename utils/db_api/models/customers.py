from sqlalchemy import Column, Integer, BigInteger, String, sql

from utils.db_api.base import Base


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger(), unique=True, nullable=False)
    name = Column(String(), default='none')
    phone = Column(String(), default='none')
    time = Column(String(), default='none')
    day = Column(String(), default='none')
    service_name = Column(String(), default='none')

    query: sql.Select



