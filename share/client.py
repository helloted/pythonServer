#coding=utf-8
import socket,json,struct,time
from gevent import socket, monkey; monkey.patch_all()
from log_util.web_demo_logger import logger
import gevent
from multiprocessing import Queue
from redis_manager import redis_center
import threading

from tool import aes_enc_b64


host = 'printer.swindtech.com'
port = 8050

ADDR = (host, port)

device_sn = "6201001000007"

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
                 "version": 2,
                 'content': '{"Id":34,"data_handle":[{"data":"1D2F00010A1B210020202020202020202020202020202020434F4D454255590A20202020202043454E5452414C205041524B204D414C4C204C542031202D203133310A202020202020202020202020544C50203038353130363037313131310A0A200A4E6F2E20537472756B202020203A20434243502D30303030313030303930312F46460A54676C20537472756B202020203A2033302D4175672D323031372032313A32363A31360A4B617373612F4F7264657223203A2031202F203532202D200A50656C6179616E2F4B617369723A2041646D696E6973747261202F204B4152494E410A2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D0A20202020312043686F636F6C617465202020202020202032332C303030202020202032332C3030300A2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D2D0A4772616E64546F74616C203A2020202020202020202020202020202020202020202032332C3030300A42617961722020202020203A2020202020202020202020202020202020202020202032332C3030300A20204361736820202020203A20202020202032332C3030300A4B656D62616C69616E20203A202020202020202020202020202020202020202020202020202020300A0A20202020546572696D61206B617369682061746173206B756E6A756E67616E20616E64610A2020202020204861726761207375646168207465726D73756B2070616A616B205042310A0A0A0A0A0A0A1B61011D286B03003143061D286B03003145301D286B200031503036323031303031303030303032313530343738303036346233373966661D286B03003151301B61000A0A0A0A0A0A0A0A1D5601","dataId":34,"id":34,"orderTime":1504780064305,"qr":"62010010000021504780064b379ff","sn":"62010010000021504780064b379ff"}],"haveQr":true,"orderType":0,"serial_num":"6201001000002","status":false,"time":0,"total_price":0}'
                 }

        body = json.dumps(data2)
        header = body.__len__()
        headPack = struct.pack("!1I", header)

        sendData1 = headPack + body.encode()

        client.send(sendData1)
        gevent.sleep(150)

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
        gevent.spawn(heart_beat())


if __name__ == '__main__':
    socket_run()