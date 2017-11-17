#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.10.25
抽奖模型
"""

from sqlalchemy import Column, Integer, String, BigInteger,JSON,TEXT,Boolean
from super_models.database import Base

class Lottery(Base):
    __tablename__ = 'lottery'

    id = Column(BigInteger, primary_key=True)

    # 订单SN，唯一性,与deal_sn相等
    order_sn = Column(String(64),unique=True,index=True)

    # 订单时间(毫秒)
    order_time = Column(BigInteger)

    # 抽奖时间
    lottery_time = Column(BigInteger)

    # 抽奖用户
    user_id = Column(BigInteger)

    # 中奖状态
    # 0 为未中奖
    # 1 为1等奖
    # 2 为2等奖
    lottery_status = Column(Integer)

    # 奖品类型
    # 1 为手机流量
    lottery_type = Column(Integer)

    # 奖品内容内容
    lottery_content = Column(String(64))

    # 中奖提示
    lottery_info = Column(String(128))