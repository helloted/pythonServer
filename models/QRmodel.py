#encoding:utf-8

"""
caohaozhi@swindtech.com
2018.04.08
二维码
"""

from sqlalchemy import Column, Integer, String, BigInteger,DateTime,Boolean,VARBINARY
from models.database import Base

class QRModel(Base):
    __tablename__ = 'qrcode'

    id = Column(BigInteger, primary_key=True)
    sn = Column(BigInteger,unique=True)
    code = Column(VARBINARY(64),unique=True)

    # 生成历史记录
    history_sn = Column(BigInteger)

    # 分配/申请的序号
    apply_sn = Column(String(32))

    # 管理员分配id
    dispatch_id = Column(BigInteger)

    # 产品信息id
    product_info_id = Column(BigInteger)






