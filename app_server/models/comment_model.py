#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
用户评论模型
"""
from sqlalchemy import Column, Integer, String,BigInteger,TEXT
from super_models.database import Base


class Comment(Base):
    __tablename__ = 'comment'

    id = Column(BigInteger, primary_key=True)

    comment_id = Column(BigInteger,unique=True,nullable=False,index=True)
    article_id = Column(BigInteger, nullable=False, index=True)

    commenter_id = Column(BigInteger)

    time = Column(BigInteger)

    text = Column(TEXT)

    type = Column(Integer,default=0)

    replied_user_id = Column(BigInteger)

    replied_user_name = Column(String(64))

    replied_comment_id = Column(BigInteger)