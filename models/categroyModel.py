#encoding:utf-8

"""
caohaozhi@swindtech.com
2018.04.08
二维码
"""

from sqlalchemy import Column, Integer, String, BigInteger,DateTime,Boolean
from models.database import Base

class Category(Base):
    __tablename__ = 'categroy'

    id = Column(BigInteger, primary_key=True)



    paraent_name = Column(String(128))

    level = Column(Integer)

    name = Column(String(128))

