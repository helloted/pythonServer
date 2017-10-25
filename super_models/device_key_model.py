from sqlalchemy import Column, Integer, String, BigInteger, ForeignKey,JSON,DateTime
from super_models.database import Base


class DeviceKey(Base):
    __tablename__ = 'device_key'

    device_sn = Column(String(32), primary_key=True)
    key = Column(String(32))
    version = Column(Integer)
    time = Column(BigInteger)