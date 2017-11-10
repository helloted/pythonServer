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

    # 订单SN，唯一性
    sn = Column(String(64),unique=True,index=True)

    # 订单时间
    time = Column(BigInteger,index=True)
    datetime = Column(DateTime)

    # 总价
    total_price = Column(Integer)

    # 应纳税
    tax = Column(Integer)

    # 备注
    remark = Column(String(200))

    # 原单
    orgin = Column(TEXT)

    # 小票原始ID
    orgin_id = Column(String(64))

    # 菜单列表
    items_list = Column(JSON)

    # 设备SN
    device_sn = Column(String(32), ForeignKey('device.sn'),index=True)

    # 店铺ID
    store_id = Column(BigInteger)

    # 店铺名称
    store_name = Column(String(64))







