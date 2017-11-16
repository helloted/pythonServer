#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.03
热门店铺模型
"""
from sqlalchemy import Column, Integer, String,BigInteger, DECIMAL
from super_models.database import Base

class HotCategory(Base):
    __tablename__ = 'hot_category'

    id = Column(BigInteger, primary_key=True)

    category = Column(String(128),index=True)

    category_img = Column(String(256))

    region_code = Column(Integer)


