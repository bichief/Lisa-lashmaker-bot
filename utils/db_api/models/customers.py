from sqlalchemy import Column, Integer, BigInteger, String, sql

from utils.db_api.base import Base


class Customers(Base):
    __tablename__ = 'customers'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    telegram_id = Column(BigInteger(), unique=True, nullable=False)
    referral = Column(String(), default='none')
    referral_name = Column(String(), default='none')
    referral_balance = Column(Integer(), default=0)
    name = Column(String(), default='none')
    phone = Column(String(), default='none')
    time = Column(String(), default='none')
    day = Column(String(), default='none')
    service_name = Column(String(), default='none')
    blocked = Column(String(), default='no')

    query: sql.Select



