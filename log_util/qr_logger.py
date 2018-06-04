# -*- coding: utf-8 -*-

import logging,logging.handlers
import sys
import os

import time
date = time.strftime("%Y%m%d")

# 获取logger实例，如果参数为空则返回root logger
logger = logging.getLogger('QR_Logger')

formatter = logging.Formatter('%(asctime)s %(levelname)s  %(message)s --> %(filename)s(%(lineno)d):%(funcName)s()')

super_path = os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir, os.pardir))
if not os.path.exists(super_path + '/logs/qrcode'):
    os.makedirs(super_path + '/logs/qrcode')

file_path = super_path + '/logs/qrcode/qr.log'

# 文件日志
file_handler = logging.handlers.TimedRotatingFileHandler(file_path,when='D',interval=1,backupCount=40)
file_handler.setFormatter(formatter)  # 可以通过setForm

# 控制台日志
console_handler = logging.StreamHandler(sys.stdout)
console_handler.formatter = formatter  # 也可以直接给formatter赋值

# 为logger添加的日志处理器
logger.addHandler(file_handler)
logger.addHandler(console_handler)

# 指定日志的最低输出级别，默认为WARN级别
logger.setLevel(logging.DEBUG)