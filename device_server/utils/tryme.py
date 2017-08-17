
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

# from devices_server.response.errors import Errors
# from devices_server.response.res import fail_response
# from devices_server.controllers.deal_controller import verify_sn
from super_models.database import SessionContext
from log_util.device_logger import logger

import socket

sn = '62010010000011496832905442seed'

def change():
    print sn
    # print ord('a')
    for c in sn:
        print c

if __name__ == '__main__':
    logger.info('hello')

