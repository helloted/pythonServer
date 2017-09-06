#coding=utf-8
import socket,json,struct,time
from gevent import socket, monkey; monkey.patch_all()
from log_util.web_demo_logger import logger
import gevent
from multiprocessing import Queue
from redis_manager import redis_center
import threading

from tool import aes_enc_b64


host = "localhost"
port = 5050

ADDR = (host, port)

device_sn = "6201001000000"

client = socket.socket()
buffer = bytes()
headerSize = 4

send_q = Queue()
received_q = Queue()


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




def push():
    ps = redis_center.pubsub()
    ps.subscribe(['cmd_print',])
    for item in ps.listen():
        if item['type'] == 'message' and item['channel'] == 'cmd_print':
            data_str = item['data']
            try:
                data = eval(data_str)
                logger.info(data)
            except Exception,e:
                logger.error(e)
            else:
                data2 = {"cmd": "cloud_print",
                         "seq": 3,
                         "version": "1",
                         'content':data
                         }

                body = json.dumps(data2)
                header = body.__len__()
                headPack = struct.pack("!1I", header)
                sendData = headPack + body.encode()
                client.send(sendData)


def handle_data(body):
    print 'handel_body:', body

    cmd = body.get('cmd')
    seq = body.get('seq')

    if cmd == 'print_content':
        prin_res(seq)



def prin_res(seq):
    data2 = {"cmd": "print_response",
             "seq": seq,
             "version": "1",
             'data': {'device_sn': device_sn,
                      'post_time': 100}
             }

    body = json.dumps(data2)
    header = body.__len__()
    headPack = struct.pack("!1I", header)

    sendData1 = headPack + body.encode()

    client.send(sendData1)



def heart_beat():
    while True:
        data2 = {"cmd": "heart_beat",
                 "seq": 3,
                 "version": "1",
                 'content': {'changed': False,
                              'port_connecting':False}
                 }

        body = json.dumps(data2)
        header = body.__len__()
        headPack = struct.pack("!1I", header)

        sendData1 = headPack + body.encode()

        client.send(sendData1)

        gevent.sleep(5)


def upload_hex():
    while True:
        data2 = {"cmd": "upload_orderhex",
                 "seq": 3,
                 "version": "1",
                 'content': 'this is upload hex'
                 }

        body = json.dumps(data2)
        header = body.__len__()
        headPack = struct.pack("!1I", header)

        sendData1 = headPack + body.encode()

        client.send(sendData1)

        gevent.sleep(5)



def received_handel(client):
    global buffer
    while True:
        stream = client.recv(1024)
        if stream:
            buffer += stream

            while True:
                if len(buffer) < headerSize:
                    break
                headPack = struct.unpack('!1I', buffer[:headerSize])

                # 获取消息正文长度
                bodySize = headPack[0]

                # 分包情况处理，跳出函数继续接收数据
                if len(buffer) < headerSize + bodySize:
                    logger.info("缓存区（%s Byte）不完整，总共(%s Byte），跳出循环" % (len(buffer), headerSize + bodySize))
                    break

                body = buffer[headerSize:headerSize + bodySize]
                buffer = buffer[headerSize + bodySize:]

                handle_data(json.loads(body))


def socket_run():
    try:
        client.connect(ADDR)
    except Exception,e:
        print 'connect failed'
        print e
    else:
        print 'connect success'
        gevent.spawn(received_handel, client)
        init_connect()
        gevent.spawn(upload_hex())


if __name__ == '__main__':
    socket_run()