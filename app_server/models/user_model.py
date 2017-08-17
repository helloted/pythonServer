#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
APP用户模型
"""
from sqlalchemy import Column, Integer, String,BigInteger
from super_models.database import Base


class User(Base):
    __tablename__ = 'user'

    id = Column(BigInteger, primary_key=True)

    user_id = Column(BigInteger,unique=True,nullable=False,index=True)
    phone = Column(String(16))
    password = Column(String(64))

    register_time = Column(BigInteger)
    last_login_time = Column(BigInteger)

    icon = Column(String(128))

    name = Column(String(50))
    sex = Column(Integer)
    birthday = Column(BigInteger)
    city = Column(String(64))

