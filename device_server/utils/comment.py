#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.01
一些公用的算法，如加密解密
"""
"""
pip  install pycrypto‎
"""

import base64
from Crypto.Cipher import AES
import struct
import os
import hashlib
import collections
import json


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

def head_pack(data):
    headPack = struct.pack("!1I", data.__len__())
    send = headPack+data
    return send

def token_random():
    token = hashlib.sha1(os.urandom(20)).hexdigest()
    return token


def get():
    token = hashlib.sha1('hello').hexdigest()
    time = 1496832905442
    print token



if __name__ == '__main__':
    token = hashlib.sha1('62010010000011496832905441seed').hexdigest()
    print token
    pre = 'seedtokenen1496832905441'
    print pre
    result = aes_enc_b64(pre)
    print  result

    sh = hashlib.sha1(result).hexdigest()

    print sh

    print hashlib.sha1('This').hexdigest()