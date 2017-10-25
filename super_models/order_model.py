#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.10.25
订单模型
"""

from sqlalchemy import Column, Integer, String, BigInteger,JSON,TEXT
from super_models.database import Base

class Order(Base):
    __tablename__ = 'order_paper'

    id = Column(BigInteger, primary_key=True)

    # 订单SN，唯一性,与deal_sn相等
    order_sn = Column(String(64),unique=True,index=True)

    # 设备SN
    device_sn = Column(String(32),index=True)

    # 订单时间(毫秒)
    order_time = Column(BigInteger,index=True)

    # 总价(含税)
    total_price = Column(Integer)

    # 应纳税
    tax = Column(Integer)

    # 备注
    remark = Column(TEXT)

    # 原单
    original_text = Column(TEXT)

    # 小票原始ID
    original_id = Column(String(64))

    # 菜单列表
    items_list = Column(JSON)

    # 店铺ID
    store_id = Column(BigInteger)

    # 店铺名称
    store_name = Column(String(64))



