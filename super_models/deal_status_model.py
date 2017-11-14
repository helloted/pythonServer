#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.10.08
订单状态
"""

from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey,JSON,DateTime,TEXT
from super_models.database import Base

class DealStatus(Base):
    __tablename__ = 'deal_status'

    id = Column(BigInteger, primary_key=True)

    # 订单SN，唯一性
    deal_sn = Column(String(64),unique=True,index=True)

    # 设备SN
    device_sn = Column(String(32))

    # 订单时间
    deal_time = Column(BigInteger)

    # device_server收到的时间毫秒
    receive_time = Column(BigInteger)

    # 解析处理完成的时间毫秒
    handle_time = Column(BigInteger)

    # 类型 1为订单
    deal_type = Column(Integer)

    # 状态
    # 0 device_server 已接收，还未解析
    # 1 convert_server 解析成功
    # 2 解析失败, 存入在convert_failed文件夹
    # 3 通过WEB，从convert_failed文件夹删除
    status = Column(Integer)

    # 备注
    remark = Column(String(256))






