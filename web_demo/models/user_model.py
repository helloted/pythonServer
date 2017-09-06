#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.22
WEB用户模型
"""
from sqlalchemy import Column, Integer, String,BigInteger
from super_models.database import Base


class User(Base):
    __tablename__ = 'web_user'

    id = Column(BigInteger, primary_key=True)
    phone = Column(String(16))
    password = Column(String(64))

    register_time = Column(BigInteger)
    last_login_time = Column(BigInteger)

    icon = Column(String(128))

    name = Column(String(50))


