#coding=utf-8

from gevent._socket2 import _closedsocket
from log_util.device_logger import logger
import socket

sockets_dict = {}

def set_socket(device_sn,tcp_socket):
    global sockets_dict
    sockets_dict[device_sn] = tcp_socket

def get_socket(device_sn):
    global sockets_dict
    tcp_socket = sockets_dict.get(device_sn)

    # if not tcp_socket:
    #     logger.info('do not has this devcie socket')
    #     return None

    if tcp_socket and isinstance(tcp_socket,_closedsocket):
        sockets_dict.pop(device_sn)
        logger.info('pop offline socket {device}'.format(device=device_sn))
        return None
    else:
        return tcp_socket


    # try:
    #     temp = tcp_socket.recv(0)
    # except Exception:
    #
    #     return None
    # else:
    #     return tcp_socket


def kill_socket(device_sn):
    the_socket = get_socket(device_sn)
    if the_socket:
        the_socket.shutdown(socket.SHUT_WR)
        the_socket.close()
        sockets_dict.pop(device_sn)
        logger.info(('killed the socket',device_sn))
    else:
        print 'kill failed'



def pop_socket(device_sn):
    global sockets_dict
    sockets_dict.pop(device_sn)