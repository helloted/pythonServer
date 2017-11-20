#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.10
我的页面网络请求
"""
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir,os.pardir))
from flask import Blueprint
from flask import request
from app_server.utils.request_handle import request_unpack,login_required
from app_server.models.favorite_model import FavoriteStore,FavoriteArticle
from app_server.models import SessionContext
from super_models.store_model import Store
from app_server.controllers.special_store_controller import convert_little_store
from app_server.response import failed_resp,success_resp
from app_server.response.errors import *
from app_server.models.article_model import Article
import json
from app_server.models.user_model import User
from app_server.controllers.article_controller import article_to_dict
from log_util.app_logger import logger
from super_models.lottery_model import Lottery
from super_models.order_model import Order
from super_models.store_model import Store


node_mine=Blueprint('mine_layer',__name__,)

@node_mine.route('/update', methods=['GET'])
@request_unpack
@login_required
def update():
    paras = request.args
    user_id = paras.get('user_id')
    with SessionContext() as session:
        data = {}
        count = session.query(Article).filter(Article.poster_id == user_id).count()
        data['review_amount'] = count

        lottery_count = session.query(Lottery).filter(Lottery.user_id == user_id).count()
        data['lottery_count'] = lottery_count
        session.result = success_resp(data)
    logger.info(session.result.log)
    return session.result.data


@node_mine.route('/favorite_store', methods=['GET'])
@request_unpack
@login_required
def favorite_store():
    paras = request.args
    user_id = paras.get('user_id')
    page = paras.get('page')
    amount = paras.get('amount')
    if not page or not amount:
        resp = failed_resp(ERROR_Parameters)
        logger.info(resp.log)
        return logger.info(resp.data)
    page_int = int(page)
    amount_int = int(amount)
    offset = (page_int-1) * amount_int
    with SessionContext() as session:
        favorites = session.query(FavoriteStore).filter_by(user_id=user_id).limit(amount_int).offset(offset).all()
        data = []
        for fav in favorites:
            store = session.query(Store).filter_by(store_id=fav.store_id).first()
            little = convert_little_store(store)
            data.append(little)
        session.result = success_resp(data)
    logger.info(session.result.log)
    return session.result.data


@node_mine.route('/favorite_article', methods=['GET'])
@request_unpack
@login_required
def favorite_article():
    paras = request.args
    user_id = paras.get('user_id')
    page = paras.get('page')
    amount = paras.get('amount')
    if not page or not amount:
        resp = failed_resp(ERROR_Parameters)
        logger.info(resp.log)
        return logger.info(resp.data)
    page_int = int(page)
    amount_int = int(amount)
    offset = (page_int-1) * amount_int
    with SessionContext() as session:
        favorites = session.query(FavoriteArticle).filter_by(user_id=user_id).limit(amount_int).offset(offset).all()
        data = []
        for fav in favorites:
            article = session.query(Article).filter_by(article_id=fav.article_id).first()
            dict =article_to_dict(article,session)
            data.append(dict)
        session.result = success_resp(data)
    logger.info(session.result.log)
    return session.result.data


@node_mine.route('/post', methods=['GET'])
@login_required
@request_unpack
def article_list():
    paras = request.args
    user_id = paras.get('user_id')
    page = paras.get('page')
    amount = paras.get('amount')
    if not page or not amount:
        resp = failed_resp(ERROR_Parameters)
        logger.info(resp.log)
        return logger.info(resp.data)
    page_int = int(page)
    amount_int = int(amount)
    offset = (page_int-1) * amount_int
    if not user_id:
        return failed_resp(ERROR_Parameters)

    with SessionContext() as session:
        articles = session.query(Article).filter_by(poster_id=user_id).limit(amount_int).offset(offset).all()
        data = []
        for art in articles:
            one = article_to_dict(art,session)
            data.append(one)
        session.result = success_resp(data)

    logger.info(session.result.log)
    return session.result.data


@node_mine.route('/consumptions', methods=['GET'])
@request_unpack
@login_required
def consumptions():
    paras = request.args
    user_id = paras.get('user_id')
    page = paras.get('page')
    amount = paras.get('amount')
    page_int = int(page)
    amount_int = int(amount)
    offset = (page_int-1) * amount_int
    data = []
    with SessionContext() as session:
        results = session.query(Lottery,Order,Store).order_by((Lottery.order_time.desc())).filter(Lottery.user_id==user_id,Order.order_sn==Lottery.order_sn,Store.store_id==Order.store_id).limit(amount_int).offset(offset).all()
        if results:
            for result in results:
                order = result[1]
                store = result[2]
                consumption = {}
                if order:
                    consumption['order_time'] = order.order_time
                    consumption['order_sn'] = order.order_sn
                    consumption['total_price'] = order.total_price
                if store:
                    consumption['store_id'] = store.store_id
                    consumption['store_name'] = store.name
                    consumption['store_icon'] = store.icon
                data.append(consumption)
        session.result = success_resp(data)
    logger.info(session.result.log)
    return session.result.data


if __name__ == '__main__':
    user_id = 4
    page_int = 1
    amount_int = 10
    offset = (page_int-1) * amount_int
    data = []
    with SessionContext() as session:
        results = session.query(Lottery,Order,Store).order_by((Lottery.order_time.desc())).filter(Lottery.user_id==user_id,Order.order_sn==Lottery.order_sn,Store.store_id==Order.store_id).limit(amount_int).offset(offset).all()
        if results:
            for result in results:
                order = result[1]
                store = result[2]
                consumption = {}
                if order:
                    consumption['order_time'] = order.order_time
                    consumption['order_sn'] = order.order_sn
                    consumption['total_price'] = order.total_price
                if store:
                    consumption['store_id'] = store.store_id
                    consumption['store_name'] = store.name
                    consumption['store_icon'] = store.icon
                data.append(consumption)