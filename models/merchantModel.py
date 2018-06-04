#encoding:utf-8

"""
caohaozhi@swindtech.com
2018.04.08
二维码
"""

from sqlalchemy import Column, Integer, String, BigInteger,DateTime,Boolean
from models.database import Base

class MerchantModel(Base):
    __tablename__ = 'merchant'

    id = Column(BigInteger, primary_key=True)

    name = Column(String(64))
    phone = Column(String(16))
    password = Column(String(32))
    email = Column(String(64))
    brand = Column(String(64))
