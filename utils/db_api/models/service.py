from sqlalchemy import Column, Integer, BigInteger, String, sql, ForeignKey
from sqlalchemy.orm import relationship

from utils.db_api.base import Base


class Service(Base):
    __tablename__ = 'service'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    name = Column(String())
    description = Column(String())
    price = Column(Integer())

    query: sql.Select