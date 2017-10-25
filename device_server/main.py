#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.01
设备长连接的入口
"""

import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
import gevent
from gevent import socket, monkey; monkey.patch_all()
from time import ctime
import controllers.device_controller as deviceController
import controllers.deal_controller as dealController
import struct
import json
from log_util.device_logger import logger
import controllers.push_controller as push_controller
from device_server.response.errors import ERROR_CMD_Error
from device_server.response.res import fail_response
import zlib
from device_server.utils.comment import aes_decode


headerSize = 4

sockets_dict = {}

def handel_data(data,tcp_socket):
    if tcp_socket.version == 3:
        try:
            data = tcp_socket.decompress.decompress(data)
        except Exception, e:
            logger.error(e)
            tcp_socket.close()

    if tcp_socket.version == 4:
        try:
            data = aes_decode(data)
            data = tcp_socket.decompress.decompress(data)
        except Exception, e:
            logger.error(e)
            tcp_socket.close()

    if tcp_socket.version == 5:
        try:
            data = aes_decode(data,aes_key=tcp_socket.aes_key)
            data = tcp_socket.decompress.decompress(data)
        except Exception, e:
            logger.error(e)
            tcp_socket.close()

    try:
        data = json.loads(data)
    except Exception,e:
        logger.error(e)
        tcp_socket.close()

    seq = data.get('seq')
    seq_int = int(seq)
    cmd = data.get('cmd')
    if (seq_int % 2) == 0:
        # 主动推给客户端的之后的回复
        logger.info(data)
        if cmd == 'update_token':
            push_controller.received_update_token(data,tcp_socket)
        elif cmd == 'print_content':
            push_controller.print_response(data,tcp_socket)
    else:
        if cmd == 'pre_connect':
            logger.debug('<<-->> pre_connect <<-->>')
            deviceController.pre_connect(data,tcp_socket)
            return

        if cmd == 'init_connect':
            logger.info(
                '{device} -> HF, cmd:{cmd}, data:{data}'.format(device=tcp_socket.device_sn, cmd=cmd, data=data))
            deviceController.init_connect(data, tcp_socket, sockets_dict)
            return

        if tcp_socket.device_sn == '':
            send = fail_response(data,ERROR_CMD_Error)
            tcp_socket.send(send.data)
            tcp_socket.close()
            logger.info(send.log)
            return

        logger.info('{device} -> HF, cmd:{cmd}, data:{data}'.format(device=tcp_socket.device_sn, cmd=cmd, data=data))

        if cmd == 'position_report':
            deviceController.position_report(data, tcp_socket)
        elif cmd == 'heart_beat':
            deviceController.heart_beat(data, tcp_socket)
        elif cmd == 'upload_deal':
            dealController.upload_deal(data, tcp_socket)
        elif cmd == 'upload_capture':
            dealController.upload_capture(data, tcp_socket)
        elif cmd == 'upload_orderhex':
            dealController.upload_orderhex(data,tcp_socket)
        elif cmd == 'request_app':
            deviceController.request_app(data,tcp_socket)
        else:
            logger.error('{cmd} is not contain'.format(cmd=cmd))
            tcp_socket.close()


def handle_buffer(tcp_socket):
    # 循环从buffer里处理数据
    while True:
        # 缓存区小于消息头部长度,说明没有数据包，跳出循环
        if len(tcp_socket.buffer) < headerSize:
            break
        # 读取包头
        # struct中:!代表Network order，1I代表1个unsigned int数据,4个字节
        headPack = struct.unpack('!1I', tcp_socket.buffer[:headerSize])

        # 获取消息正文长度
        bodySize = headPack[0]

        # 分包情况处理，跳出函数继续接收数据
        if len(tcp_socket.buffer) < headerSize + bodySize:
            logger.info("缓存区（%s Byte）不完整，总共(%s Byte），这一次不剪切处理，跳过" % (len(tcp_socket.buffer), headerSize + bodySize))
            break

        # 正常则继续
        # 读取消息正文的内容
        body = tcp_socket.buffer[headerSize:headerSize + bodySize]

        # 处理数据
        # data = json.loads(body)
        handel_data(body,tcp_socket)

        # 数据读取完毕，把读取完的数据从缓存区切走
        tcp_socket.buffer = tcp_socket.buffer[headerSize + bodySize:]  # 获取下一个数据包，类似于把数据pop出


def handle_request(tcp_socket):
    try:
        while True:
            # 等待连接的新数据，不断从连接里拿到新数据放到缓存区里
            stream = tcp_socket.recv(1024)
            if stream:
                tcp_socket.buffer += stream
                handle_buffer(tcp_socket)
            else:
                tcp_socket.shutdown(socket.SHUT_WR)
    except Exception as e:
        print(e)
    finally:
        tcp_socket.close()

if __name__ == '__main__':

    gevent.spawn(push_controller.receive_push_queue)

    gevent.spawn(push_controller.receive_web_redis_publish)

    host = 'localhost'
    port = 5050
    num = 100
    timeout = 1800

    s = socket.socket()
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.bind((host, port))

    # 最多同时500个TCP连接
    s.listen(num)

    while True:
        # 等待新连接，有新连接成功才往下走
        tcp_socket, address = s.accept()
        tcp_socket.device_sn = 'Before_Sign'
        tcp_socket.store_id = 0
        tcp_socket.buffer = bytes()
        tcp_socket.version = 0
        tcp_socket.aes_key = ''
        tcp_socket.decompress = zlib.decompressobj(16 + zlib.MAX_WBITS)
        # logger.info ("connect success from (%r):%r" % (address, ctime()))
        tcp_socket.settimeout(timeout)
        gevent.spawn(handle_request, tcp_socket)