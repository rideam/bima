# coding: utf-8
from sqlalchemy import BigInteger, CHAR, Column, DateTime, Float, Index, Integer, String, Text
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()
metadata = Base.metadata


class Farmer(Base):
    __tablename__ = 'farmers'
    __table_args__ = (
        Index('PK_tbl_farmer', 'email', unique=True),
    )

    email = Column(String(50), primary_key=True, nullable=False)
    firstname = Column(String(50))
    lastname = Column(String(50))
    farmname = Column(String(50))
    address = Column(String(255))
