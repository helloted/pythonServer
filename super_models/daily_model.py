#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.18
每日统计
"""

from sqlalchemy import Column, Integer, String, BigInteger,DateTime
from super_models.database import Base

class Daily(Base):
    __tablename__ = 'daily'

    id = Column(BigInteger, primary_key=True)
    time = Column(BigInteger,index=True)
    datetime = Column(DateTime)

    total_device = Column(Integer)
    online_device = Column(Integer)