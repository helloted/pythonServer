#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
APP—Server的一些公用方法
"""

from log_util.app_logger import logger

def db_error_record(exc_val):
    logger.error(exc_val)
