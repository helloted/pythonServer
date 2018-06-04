# encoding:utf-8

"""
caohaozhi@swindtech.com
2018.04.08
二维码
"""

from sqlalchemy import Column, Integer, String, BigInteger, DateTime, Boolean, JSON
from models.database import Base


class ProductInfoModel(Base):
    __tablename__ = 'product_info'

    id = Column(BigInteger, primary_key=True)

    # 管理员分配时用的ID
    dispatch_id = Column(BigInteger)

    time = Column(BigInteger)

    # 经销商的ID
    agent_id = Column(BigInteger)

    # 数量
    count = Column(BigInteger)

    # 起始值
    start_sn = Column(BigInteger)

    # 终止值
    end_sn = Column(BigInteger)

    # 产品公司名
    company = Column(String(64))

    # 产品品牌名
    brand = Column(String(64))

    others = Column(JSON)

    # 状态1已生成记录，未分配成功，2已分配成功，3已废弃，已分配代表该二维码有效
    status = Column(Integer)
