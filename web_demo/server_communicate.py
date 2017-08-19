#coding=utf-8

import json,struct,time
from gevent import socket, monkey; monkey.patch_all()
from log_util.web_demo_logger import logger
import gevent
from multiprocessing import Queue
from redis_manager import redis_center
import threading


host = "localhost"
port = 5050
ADDR = (host, port)
client = None
buffer = bytes()
headerSize = 4

send_q = Queue()
received_q = Queue()


def push():
    ps = redis_center.pubsub()
    ps.subscribe(['cmd_print','cmd_setting','cmd_update_app'])
    for item in ps.listen():
        if item['type'] == 'message' and item['channel'] == 'cmd_print':
            print '-------------------'
            data_str = item['data']
            try:
                data = eval(data_str)
                logger.info(data)
            except Exception,e:
                logger.error(e)
            else:
                data = {'source':'web_server',
                        "cmd": "cloud_print",
                         "seq": 5,
                         "version": "1",
                         'content':data
                         }
                body = json.dumps(data)
                header = body.__len__()
                headPack = struct.pack("!1I", header)
                sendData = headPack + body.encode()
                send_data(sendData,0)

        if item['type'] == 'message' and item['channel'] == 'cmd_setting':
            print '==================listened'
            data_str = item['data']
            try:
                data = eval(data_str)
                logger.info(data)
            except Exception,e:
                logger.error(e)
            else:
                data = {'source':'web_server',
                        "cmd": "cloud_setting",
                         "seq": 9,
                         "version": "1",
                         'content':data
                         }
                body = json.dumps(data)
                header = body.__len__()
                headPack = struct.pack("!1I", header)
                sendData = headPack + body.encode()
                send_data(sendData,0)


        if item['type'] == 'message' and item['channel'] == 'cmd_update_app':
            data_str = item['data']
            try:
                data = eval(data_str)
                logger.info(data)
            except Exception,e:
                logger.error(e)
            else:
                data = {'source':'web_server',
                        "cmd": "update_app",
                         "seq": 11,
                         "version": "1",
                         'content':data
                         }
                body = json.dumps(data)
                header = body.__len__()
                headPack = struct.pack("!1I", header)
                sendData = headPack + body.encode()
                send_data(sendData,0)



def heart_beat():
    global client
    while True:
        data = {'source':'web_server',
                 "cmd": "heart_beat",
                 "seq": 3,
                 "version": "1",
                 }
        body = json.dumps(data)
        header = body.__len__()
        headPack = struct.pack("!1I", header)
        sendData = headPack + body.encode()
        send_data(sendData,20)



def send_data(data,sleep_time):
    global client
    try:
        client.send(data)
    except Exception, e:
        socket_connect()
    else:
        pass
    finally:
        gevent.sleep(sleep_time)



def socket_connect():
    global client
    try:
        client = socket.socket()
        client.connect(ADDR)
    except Exception,e:
        logger.info(e)
        time.sleep(1)
        socket_connect()
    else:
        logger.info('reconnect success')
        pass


def handle_data(body):
    content = body.get('content')
    seq = body.get('seq')
    if seq == 3:
        logger.info('hart beat response')
    if seq == 5:
        logger.info(body)
        device_sn = content.get('device_sn')
        post_time = content.get('post_time')
        channel = device_sn + str(post_time)
        redis_center.publish(channel, body)


def received_handel():
    global client
    global buffer
    while True:
        try:
            stream = client.recv(1024)
        except Exception,e:
            socket_connect()
        else:
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
        finally:
            gevent.sleep(0)


def socket_run():
    socket_connect()
    gevent.spawn(received_handel)
    gevent.spawn(heart_beat)
    gevent.spawn(push)
