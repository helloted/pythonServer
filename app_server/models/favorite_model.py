#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.07
店铺收藏模型
"""
from sqlalchemy import Column, BigInteger
from super_models.database import Base

class FavoriteStore(Base):
    __tablename__ = 'favorite_store'

    id = Column(BigInteger, primary_key=True)

    user_id = Column(BigInteger,index=True)

    store_id = Column(BigInteger,index=True)

    time = Column(BigInteger)


class LikeArticle(Base):
    __tablename__ = 'like_article'

    id = Column(BigInteger, primary_key=True)

    user_id = Column(BigInteger, index=True)

    article_id = Column(BigInteger, index=True)

    time = Column(BigInteger)



class FavoriteArticle(Base):
    __tablename__ = 'favorite_article'

    id = Column(BigInteger, primary_key=True)

    user_id = Column(BigInteger, index=True)

    article_id = Column(BigInteger, index=True)

    time = Column(BigInteger)

