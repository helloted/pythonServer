#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.08.04
店铺相关Layer处理
"""

from flask import Blueprint
from flask import request
from super_models.history_model import EventsHistroy
from web_server.models import SessionContext
from web_server.utils.handles import transfer
from web_server.utils.response import response_success,response_failed
from web_server.utils import errors
import time
from redis_manager import r_store_info
from super_models.store_model import Store
from log_util.web_demo_logger import logger


node_store=Blueprint('store_layer',__name__,)


@node_store.route('/', methods=['GET'])
@transfer
def store_detail():
    page = request.args.get('page')
    amount = request.args.get('amount')