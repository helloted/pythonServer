# encoding:utf-8

"""
caohaozhi@swindtech.com
2018.04.08
二维码
"""

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Boolean, JSON
from models.database import Base


class ApplyModel(Base):
    __tablename__ = 'apply'

    id = Column(BigInteger, primary_key=True)

    # 经销商ID
    agent_id = Column(BigInteger)

    # 申请时间
    apply_time = Column(BigInteger)

    # 分配时间
    dispathc_time = Column(BigInteger)

    apply_sn = Column(String(32))

    # 数量
    count = Column(BigInteger)

    # 起始值
    start_sn = Column(BigInteger)

    # 终止值
    end_sn = Column(BigInteger)

    # 状态1未分配，2已分配，3已取消，已分配代表该二维码有效
    status = Column(Integer)

    company = Column(String(64))

    brand = Column(String(64))

    others = Column(JSON)


