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

    # 设置版本号
    newest_setting_version = Column(BigInteger, default=0)

    # 设备当前设置号
    local_setting_version = Column(BigInteger, default=0)

    # Wifi
    wifi_name = Column(String(64),default='')
    wifi_password = Column(String(64),default='')
    wifi_encrypt_type = Column(String(32),default='2')
    wifi_list = Column(JSON)

    # 波特率
    capture_baudrate = Column(String(32),default='9600')
    app_print_baudrate = Column(String(32),default='9600')
    app_received_baudrate = Column(String(32),default='9600')

    # 端口
    net_port = Column(String(32),default='9100')

    # 端口是否连接
    port_connecting = Column(Boolean)

    # 网络状态
    network_state = Column(String(32))

    # 设备状态
    device_state = Column(String(32))

    # 蓝牙白名单
    bluetooth_white_list = Column(JSON)

    # ip白名单
    ip_white_list = Column(JSON)

    # 设备APP当前版本
    app_version = Column(String(32),default='')

    # 最新版本的URL
    newest_url = Column(String(128),default='')

    # logo URLS
    logo_urls = Column(JSON)

    # 新logo
    logo_new = Column(Boolean)

    # 是否添加二维码
    add_qr = Column(Boolean)

    # 订单有效关键字
    order_valid_keys = Column(JSON)

    # 订单无效关键字
    order_invalid_keys = Column(JSON)

    # 切刀命令
    cut_cmds = Column(JSON)

    # 判定命令,位置
    justification = Column(Integer)


class SeedToken(Base):
    __tablename__ = 'seedtoken'

    id = Column(BigInteger, primary_key=True)
    token = Column(String(20))
    enable_time = Column(BigInteger)

    device_sn = Column(String(32), ForeignKey('device.sn'))

