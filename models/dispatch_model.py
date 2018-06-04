# encoding:utf-8

"""
caohaozhi@swindtech.com
2018.04.08
二维码
"""

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Boolean, JSON
from models.database import Base


class DispatchModel(Base):
    __tablename__ = 'dispatch'

    id = Column(BigInteger, primary_key=True)

    # 分配时间
    dispatch_time = Column(BigInteger)

    # 数量
    count = Column(BigInteger)

    # 起始值
    start_sn = Column(BigInteger)

    # 终止值
    end_sn = Column(BigInteger)

    # 状态1已生成记录，未分配成功，2已分配成功，3已废弃，已分配代表该二维码有效
    status = Column(Integer)

    # 经销商ID
    agent_id = Column(BigInteger)

    # 其他
    others = Column(JSON)
