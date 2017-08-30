from sqlalchemy import Column, Integer, String,BigInteger, DECIMAL, Float,JSON
from super_models.database import Base
from sqlalchemy.orm import relationship


class Store(Base):
    __tablename__ = 'store'

    id = Column(BigInteger, primary_key=True)

    store_id = Column(BigInteger, nullable=False,unique=True)

    store_sn = Column(String(64))

    devices = relationship("Device", backref="store")
    deals = relationship("Deal", backref="store")

    region_code = Column(Integer)
    region = Column(String(64))


    icon = Column(String(128))

    name = Column(String(50))
    phone = Column(String(16))


    lng = Column(DECIMAL(13,10),default=0)

    lat = Column(DECIMAL(13,10),default=0)

    district = Column(String(64))

    score = Column(Float,default=4.0)
    per = Column(Integer,default=0)

    comment_amount = Column(Integer,default=0)

    favorites_amount = Column(Integer,default=0)

    location = Column(String(256))

    category = Column(String(64))

    open_time = Column(Integer,default=0)

    close_time = Column(Integer,default=0)

    set_up = Column(BigInteger,default=0)

    banners_list = Column(JSON)

    menus_list = Column(JSON)

    services = Column(String(512))

    cuisines = Column(String(256))







