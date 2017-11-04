#coding=utf-8

from sqlalchemy import Column, String,BigInteger
from super_models.database import Base


class DeviceStore(Base):
    __tablename__ = 'device_store'

    id = Column(BigInteger, primary_key=True)

    device_sn = Column(String(32),unique=True)

    store_id = Column(BigInteger)

    store_name = Column(String(64))
