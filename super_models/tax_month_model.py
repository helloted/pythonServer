#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.10.25
店铺税收每个月模型
"""

from sqlalchemy import Column, Integer, String, BigInteger,JSON,TEXT
from super_models.database import Base

class Order(Base):
    __tablename__ = 'order_paper'

    id = Column(BigInteger, primary_key=True)

    # 店铺ID
    store_id = Column(BigInteger, nullable=False)

    #月份
    # 201711
    month = Column(Integer)

    # 税
    tax = Column(BigInteger)

