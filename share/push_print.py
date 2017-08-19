#coding=utf-8

# import sys, os;sys.path.append(os.path.realpath("../.."))
import os
import socket
import time
import struct
import json
from tool import current_time_msec,current_time
import hashlib
from tool import aes_enc_b64

host = "localhost"
port = 5050

# host = '47.74.130.48'
# port = 8050

ADDR = (host, port)

client = socket.socket()
client.connect(ADDR)

device_sn = "6201001000002"

def init_connect():

    sign = '122|'+device_sn

    signenc = aes_enc_b64(sign)

    initdata = {"cmd": "init_connect",
                "content": {"serail_num": device_sn,
                            "sign": signenc
                            },
                "seq": 1,
                "version": "1"
                }

    body = json.dumps(initdata)
    header = body.__len__()
    headPack = struct.pack("!1I", header)
    sendData = headPack + body.encode()

    client.send(sendData)
    res = client.recv(1024)
    print 'response:', res

def print_push():

    sign = '122|'+device_sn

    signenc = aes_enc_b64(sign)

    initdata = {'device_sn':'6201001000002',
                'cmd':'cloud_print',
                'seq':1
                }

    body = json.dumps(initdata)
    header = body.__len__()
    headPack = struct.pack("!1I", header)
    sendData = headPack + body.encode()

    client.send(sendData)
    res = client.recv(1024)
    print 'response:', res


def adddeal():
    a = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))
    b = ''.join(map(lambda xx:(hex(ord(xx))[2:]),os.urandom(16)))
    item1 = {'name': 'Big Hamberger', 'quantity': 1, 'subtotal': 8000}
    item2 = {'name': 'Orenge Juice', 'quantity': 2, 'subtotal': 9000}

    list = (item1, item2)

    seed_token = 'seed'

    time = current_time_msec() - 1000 * 24 * 60 * 60

    text = device_sn + seed_token + str(time)
    base = aes_enc_b64(text)
    hah = hashlib.sha1(base).hexdigest()

    verify = hah[:6]

    deal_sn = device_sn + str(current_time() - 24 * 60 * 60) + verify


    data1 = {"cmd": "upload_deal",
             "content": {"list": list,
                         'device_sn': device_sn,
                         'deal_sn': deal_sn,
                         'total_price': 17000,
                         'deal_time': time
                         },
             "seq": 5,
             "version": "1",
             }

    body = json.dumps(data1)
    header = body.__len__()
    headPack = struct.pack("!1I", header)
    sendData1 = headPack + body.encode()
    client.send(sendData1)
    res = client.recv(1024)
    print 'response:', res


def heart_beat():
    data2 = {"cmd": "heart_beat",
             "seq": 3,
             "version": "1",
             }

    body = json.dumps(data2)
    header = body.__len__()
    headPack = struct.pack("!1I", header)

    sendData1 = headPack + body.encode()

    client.send(sendData1)

    # res = client.recv(1024)
    # print 'response:', res



if __name__ == '__main__':
    while True:
        print_push()
        time.sleep(5)


