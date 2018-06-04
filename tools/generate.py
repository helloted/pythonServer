#coding=utf-8
import time,os
import base64
import random
import hashlib
import string
import sys
from models.database import SessionContext
from models.QRmodel import QRModel
from log_util.app_logger import logger
from models.create_history_model import CreateHistoryModel
import traceback

current_milli_time = lambda: int(round(time.time() * 1000))

import base64
from Crypto.Cipher import AES

def aes_enc_b64(data,aes_key=None):
    if not aes_key:
       aes_key = '9876543210uvwxyz'
    size = AES.block_size
    count = size - len(data)%size
    if count is not 0:
        data+=(chr(0)*count)
    cipher = AES.new(aes_key)
    return base64.b64encode(cipher.encrypt(data))


def create_code(start_sn,count,history_sn):
    superPath = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
    folderPath = superPath + '/files/qrcode/'
    flag = 1
    sn = start_sn
    file_name = folderPath + str(history_sn) + '.txt'
    try:
        with open(file_name, 'a+') as file:
            sql_list = []
            temp = 0

            # 挨个生成二维码
            for i in xrange(count):
                m_sec = current_milli_time()
                full_str = str(m_sec) + full_num(flag)
                if flag < 990:
                    up = random.randint(1,9)
                    flag += up
                else:
                    flag = 1

                ran = random.randint(10,99)
                full_str = str(ran) + full_str
                res_str = change(int(full_str))
                code_str = '1' + res_str
                sn_str = full_sn(sn)

                # 写入文件
                url_str = 'https://clubori.com/' + code_str
                line = sn_str + ',' + url_str + '\n'
                file.write(line)
                sn += 1

                # 写入数据库
                sql = {'sn': int(sn_str), 'code': code_str,'history_sn':history_sn}
                if temp < 1000:
                    temp += 1
                else:
                    insert_model(sql_list)
                    temp = 1
                    sql_list = []
                sql_list.append(sql)
            insert_model(sql_list)
    except Exception,e:
        logger.error(traceback.format_exc())
        with SessionContext() as session:
            his = session.query(CreateHistoryModel).filter(CreateHistoryModel.history_sn==history_sn).first()
            if his:
                his.status = 3
                session.commit()
        logger.info('generate code failed:{sn}'.format(sn=history_sn))
    else:
        with SessionContext() as session:
            his = session.query(CreateHistoryModel).filter(CreateHistoryModel.history_sn==history_sn).first()
            if his:
                his.status = 2
                session.commit()
                logger.info('generate {sn} code success'.format(sn=history_sn))


def insert_model(sql_list):
    with SessionContext() as session:
        session.execute(QRModel.__table__.insert(), sql_list)
        session.commit()

def full_sn(sn):
    if sn < 10:
        return '1000000{sn}'.format(sn=sn)
    elif sn < 100:
        return '100000{sn}'.format(sn=sn)
    elif sn < 1000:
        return '10000{sn}'.format(sn=sn)
    elif sn < 10000:
        return '1000{sn}'.format(sn=sn)
    elif sn < 100000:
        return '100{sn}'.format(sn=sn)
    elif sn < 1000000:
        return '10{sn}'.format(sn=sn)
    elif sn < 10000000:
        return '1{sn}'.format(sn=sn)
    elif sn < 99999999:
        return str(sn)
    else:
        logger.error(sn)
        raise ValueError

__my_char = string.digits + string.letters
__count = len(__my_char)
__radix_char = '8GSh3dg6OA1PtU2ycx5jDbukFXRzQa9Ip4rVWZm7Ms0lNqLiwCoYvTEBfKJHne'
__radix = len(__radix_char)

def change(num):
    result = ""
    while num > 0:
        i = num % __count
        result = __my_char[i] + result
        num /= __radix
    return result

def full_num(num):
    if num < 10:
        return '00{num}'.format(num=num)
    elif num < 100:
        return '0{num}'.format(num=num)
    elif num < 1000:
        return str(num)
    else:
        raise ValueError


def create_new():
    flag = 1
    sn = 1
    temp_dic = {}
    for i in xrange(100000):
        m_sec = current_milli_time()
        full_str = str(m_sec) + full_num(flag)
        if flag < 990:
            up = random.randint(1, 9)
            flag += up
        else:
            flag = 1

        ran = random.randint(10, 99)
        full_str = str(ran) + full_str
        res_str = change(int(full_str))
        res_str = '1' + res_str

        # 写入文件
        url_str = 'https://clubori.com/' + res_str

        value = temp_dic.get(res_str)
        if value:
            print res_str
        else:
            temp_dic[res_str] = 'one'


if __name__ == '__main__':
    create_new()