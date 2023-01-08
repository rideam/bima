# coding: utf-8
from sqlalchemy import BigInteger, CHAR, Column, DateTime, Float, Index, Integer, String, Text, Boolean, ForeignKey
from .db import Base
from sqlalchemy.orm import relationship

# from sqlalchemy.ext.declarative import declarative_base
# Base = declarative_base()
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



class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True)
    hashed_password = Column(String)
    is_active = Column(Boolean, default=True)

    items = relationship("Item", back_populates="owner")


class Item(Base):
    __tablename__ = "items"

    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, index=True)
    description = Column(String, index=True)
    owner_id = Column(Integer, ForeignKey("users.id"))

    owner = relationship("User", back_populates="items")