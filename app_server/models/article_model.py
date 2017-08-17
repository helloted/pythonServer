#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
用户点评模型
"""
from sqlalchemy import Column, Integer, String,BigInteger,TEXT,Float,JSON,Boolean
from super_models.database import Base


class Article(Base):
    __tablename__ = 'article'

    id = Column(BigInteger, primary_key=True)

    article_id = Column(BigInteger,unique=True,nullable=False,index=True)
    store_id = Column(BigInteger, nullable=False, index=True)
    deal_sn = Column(String(64))

    region_code = Column(Integer)

    poster_id = Column(BigInteger)

    post_time = Column(BigInteger)

    score = Column(Float)

    per = Column(Integer)

    text = Column(TEXT)

    imgs = Column(JSON)
    img_count = Column(Integer)


    anonymous = Column(Boolean)


    essence = Column(Boolean)

