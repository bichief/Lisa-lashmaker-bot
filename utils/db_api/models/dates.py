from sqlalchemy import Column, Integer, BigInteger, String, sql, ForeignKey, ForeignKeyConstraint

from utils.db_api.base import Base


class Dates(Base):
    __tablename__ = 'dates_service'

    id = Column(Integer(), primary_key=True, autoincrement=True)
    service_name = Column(String())
    date = Column(String())

    query: sql.Select