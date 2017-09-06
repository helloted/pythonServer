
# session = Session()
#
# device = Device()
#
# device.sn = '6201001000001'
#
# session.add(device)
#
# try:
#     session.commit()
#     print 'success'
# except Exception, e:
#     session.rollback()
#     print Exception, ":", e

import os
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
from super_models.device_model import Device
# from devices_server.response.errors import Errors
# from devices_server.response.res import fail_response
# from devices_server.controllers.deal_controller import verify_sn
from super_models.database import SessionContext,Session
from log_util.device_logger import logger
import json

import socket

sn = '62010010000011496832905442seed'

def change():
    print sn
    # print ord('a')
    for c in sn:
        print c

if __name__ == '__main__':
    session = Session()
    devices = session.query(Device).all()
    for dev in devices:
        dev.cut_cmds = json.dumps(['1b 6d 0d'])
        dev.order_invalid_keys = json.dumps(['*** Reprint ***'])
        dev.order_valid_keys = json.dumps(['Cabang','Mulai'])

    session.commit()

