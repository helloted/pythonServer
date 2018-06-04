# encoding:utf-8

"""
caohaozhi@swindtech.com
2018.04.08
二维码
"""

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Boolean, JSON
from models.database import Base


class CreateHistoryModel(Base):
    __tablename__ = 'create_history'

    id = Column(BigInteger, primary_key=True)

    # 历史事件
    history_sn = Column(BigInteger)

    time = Column(BigInteger)

    # 数量
    count = Column(BigInteger)

    # 起始值
    start_sn = Column(BigInteger)

    # 终止值
    end_sn = Column(BigInteger)

    # 状态 1表示正在生成，2表示生成生成成功，3表示生成失败
    status = Column(Integer)
