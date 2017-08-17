#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.29
首页横幅广告模型
"""
from sqlalchemy import Column, Integer, String,BigInteger, DECIMAL
from super_models.database import Base

class Banner(Base):
    __tablename__ = 'banner'

    id = Column(BigInteger, primary_key=True)

    banner_id = Column(BigInteger,index=True)

    region_code = Column(Integer)

    img =  Column(String(256))

    start_time = Column(BigInteger)

    end_time = Column(BigInteger)

    type = Column(Integer)

    url = Column(String(256))

