#coding=utf-8

from sqlalchemy import Column, Integer, String,BigInteger, ForeignKey,JSON,Boolean
from sqlalchemy.orm import relationship, backref
from super_models.database import Base


class Device(Base):
    __tablename__ = 'device'

    id = Column(BigInteger, primary_key=True)
    sn = Column(String(32),unique=True,index=True)
    phone = Column(String(16))
    install_time = Column(BigInteger)


    store_id = Column(BigInteger, ForeignKey('store.store_id'))

    deals = relationship("Deal",backref="device")

    seedtokens = relationship("SeedToken",backref="device")

    problem = Column(Boolean,default=False)

    newest_setting_version = Column(BigInteger, default=0)
    local_setting_version = Column(BigInteger, default=0)

    wifi_name = Column(String(64),default='')
    wifi_password = Column(String(64),default='')
    wifi_encrypt_type = Column(String(32),default='2')
    wifi_list = Column(JSON)

    capture_baudrate = Column(String(32),default='9600')
    app_print_baudrate = Column(String(32),default='9600')
    app_received_baudrate = Column(String(32),default='9600')


    net_port = Column(String(32),default='9100')

    port_connecting = Column(Boolean)
    network_state = Column(String(32))
    device_state = Column(String(32))

    bluetooth_white_list = Column(JSON)
    ip_white_list = Column(JSON)

    app_version = Column(String(32),default='')
    newest_url = Column(String(128),default='')


class SeedToken(Base):
    __tablename__ = 'seedtoken'

    id = Column(BigInteger, primary_key=True)
    token = Column(String(20))
    enable_time = Column(BigInteger)

    device_sn = Column(String(32), ForeignKey('device.sn'))

