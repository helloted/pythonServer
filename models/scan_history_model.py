#encoding:utf-8

"""
caohaozhi@swindtech.com
2018.04.08
二维码
"""

from sqlalchemy import Column, Integer, String, BigInteger,DateTime,Boolean,VARBINARY,DECIMAL
from models.database import Base

class ScanHistoryModel(Base):
    __tablename__ = 'scan_history'

    id = Column(BigInteger, primary_key=True)

    code = Column(VARBINARY(64))

    time = Column(BigInteger)

    lng = Column(DECIMAL(13,10),default=0.01)

    lat = Column(DECIMAL(13,10),default=0.01)

    location = Column(String(256))

    merchant_id = Column(BigInteger)