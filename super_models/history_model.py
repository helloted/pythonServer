#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.20
离线历史统计
"""

from sqlalchemy import Column, Integer, String, BigInteger,DateTime,Float
from super_models.database import Base

class OfflineHistroy(Base):
    __tablename__ = 'offline_histroy'

    id = Column(BigInteger, primary_key=True)

    device_sn = Column(String(32))

    store_id = Column(BigInteger)
    store_name = Column(String(50))

    start_time = Column(BigInteger)
    end_time = Column(BigInteger)

    time_between = Column(Integer)


class EventsHistroy(Base):
    __tablename__ = 'events_history'

    id = Column(BigInteger, primary_key=True)

    time = Column(BigInteger)

    # 0未 1是OK
    status = Column(Integer,default=0)

    store_id = Column(BigInteger)
    store_name = Column(String(50))

    # 1是机器离线历史，2是端口离线历史，3是税收波动历史
    type = Column(Integer)

    # type1、2 离线历史，端口掉线历史
    device_sn = Column(String(32))
    start_time = Column(BigInteger)
    end_time = Column(BigInteger)
    time_between = Column(Integer)


    # type3 波动历史
    value = Column(Integer)
    float_value = Column(Float)



class FluctuatesHistroy(Base):
    __tablename__ = 'fluctuates_histroy'

    id = Column(BigInteger, primary_key=True)

    time = Column(BigInteger)

    store_id = Column(BigInteger)
    store_name = Column(String(50))

    # 1是总金额、2是总税、3是总单数
    type = Column(Integer)

    value = Column(Float)

