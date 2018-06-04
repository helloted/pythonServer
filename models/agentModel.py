#encoding:utf-8

"""
caohaozhi@swindtech.com
2018.04.08
二维码
"""

from sqlalchemy import Column, Integer, String, BigInteger,DateTime,Boolean,JSON
from models.database import Base

class AgentModel(Base):
    __tablename__ = 'agent'

    id = Column(BigInteger, primary_key=True)

    phone = Column(String(16))

    name = Column(String(64))

    password = Column(String(32))

    email = Column(String(64))

    brand = Column(String(64))

    product_place = Column(String(128))

    customs = Column(JSON)

    # 0为最高管理员，1为1级分销商
    level = Column(Integer)
