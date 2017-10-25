
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

from Crypto.Cipher import AES
import base64

def aes_enc_b64(data,aes_key=None):
    if not aes_key:
       aes_key = '1234567890123456'
    size = AES.block_size
    count = size - len(data)%size
    if count is not 0:
        data+=(chr(0)*count)

    cipher = AES.new(aes_key)
    return base64.b64encode(cipher.encrypt(data))

def b64_aes_dec(data,aes_key=None):
    b64_data = base64.b64decode(data)

    if not aes_key:
       aes_key = '1234567890123456'

    cipher = AES.new(aes_key)
    dec_data = cipher.decrypt(b64_data)

    return dec_data.rstrip('\0')

def aes_encode(data):
    aes_key = '1234567890123456'
    size = AES.block_size
    count = size - len(data)%size
    if count is not 0:
        data+=(chr(0)*count)

    cipher = AES.new(aes_key)
    return cipher.encrypt(data)

def aes_decode(data):
    aes_key = '1234567890123456'

    cipher = AES.new(aes_key)
    dec_data = cipher.decrypt(data)

    return dec_data.rstrip('\0')


from datetime import datetime

if __name__ == '__main__':
    a = datetime.now().strftime('%Y-%m-%d %H:%M:%S_%f')
    print type(a)