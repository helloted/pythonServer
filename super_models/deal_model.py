#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.08
交易模型
"""

from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey,JSON,DateTime,TEXT
from super_models.database import Base

class Deal(Base):
    __tablename__ = 'deal'

    id = Column(BigInteger, primary_key=True)
    sn = Column(String(64),unique=True,index=True)
    time = Column(BigInteger,index=True)
    datetime = Column(DateTime)
    total_price = Column(Integer)
    tax = Column(Integer)
    remark = Column(String(200))

    orgin = Column(TEXT)

    orgin_id = Column(String(64))

    device_sn = Column(String(32), ForeignKey('device.sn'),index=True)
    store_id = Column(BigInteger, ForeignKey('store.store_id'))
    store_name = Column(String(64))

    items_list = Column(JSON)





