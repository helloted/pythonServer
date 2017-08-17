#coding=utf-8

import sys, os; sys.path.append(os.path.realpath("../.."))
import socket
import time
import struct
import json
from share.tool import current_time_msec



host = "localhost"
port = 5050

# host = '47.74.130.48'
# port = 8050

ADDR = (host, port)

import hashlib

def token():
    sha = hashlib.sha1('helloworld')
    print sha


def init_connect():
    initdata = {"cmd": "init_connect",
            "content": {"serail_num": "6201001000001",
                        "sign": "qYlRChJTmdfkDuHUeT0zoC/HW6umNV3UirQTCFHZmik="
                         },
            "seq": 3,
            "version": "1"
            }

    body = json.dumps(initdata)
    header = body.__len__()
    headPack = struct.pack("!1I", header)
    sendData = headPack+body.encode()

    client.send(sendData)


def adddeal():
    item1 = {'name':'中文','quantity':1,'subtotal':80000}
    item2 = {'name':'meal','quantity':2,'subtotal':6700}

    list = (item1,item2)

    device_sn = '6201001000001'
    seed_token = 'seed'

    time = current_time_msec

    text = device_sn + seed_token + str(time)
    base = aes_enc_b64(text)
    hah = hashlib.sha1(base).hexdigest()

    verify = hah[:6]

    post_verify = deal_sn[-6:]

    data1 = {"cmd": "upload_deal",
            "content": {"list": list,
                        'device_sn': device_sn,
                        'deal_sn': 'thisisdealsn',
                        'total_price': 5000,
                        'deal_time': current_time_msec()
                        },
            "seq": 3,
            "version": "1",
            }


    body = json.dumps(data1)
    header = body.__len__()
    headPack = struct.pack("!1I", header)

    sendData1 = headPack+body.encode()


    print 'sendsize:',sendData1.__len__()
    client.send(sendData1)


def heart_beat():
    data2 = {"cmd": "heart_beat",
            "seq": 3,
            "version": "1",
            }


    body = json.dumps(data2)
    header = body.__len__()
    headPack = struct.pack("!1I", header)


    sendData1 = headPack+body.encode()

    while True:
        # 正常数据包
        client.send(sendData1)

        print 'send over'

        res = client.recv(1024)
        print 'response:', res

        time.sleep(15)










    # # 分包数据定义
    # ver = 2
    # body = json.dumps(dict(hello="world2"))
    # print(body)
    # cmd = 102
    # header = [ver, body.__len__(), cmd]
    # headPack = struct.pack("!3I", *header)
    # sendData2_1 = headPack+body[:2].encode()
    # sendData2_2 = body[2:].encode()

    # # 分包测试
    # client.send(sendData2_1)
    # time.sleep(0.2)
    # client.send(sendData2_2)
    # time.sleep(3)

    # 粘包数据定义
    # ver = 3
    # body1 = json.dumps(dict(hello="world3"))
    # print(body1)
    # cmd = 103
    # header = [ver, body1.__len__(), cmd]
    # headPack1 = struct.pack("!3I", *header)
    #
    # ver = 4
    # body2 = json.dumps(dict(hello="world4"))
    # print(body2)
    # cmd = 104
    # header = [ver, body2.__len__(), cmd]
    # headPack2 = struct.pack("!3I", *header)
    #
    # sendData3 = headPack1+body1.encode()+headPack2+body2.encode()

    # # 粘包测试
    # client.send(sendData3)
    # time.sleep(3)
    # client.close()