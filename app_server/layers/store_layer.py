#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.04
APP-Store页处理
"""
import gevent
from flask import Blueprint
from flask import request
from app_server.utils.request_handle import basic_unpack,login_required
from app_server.response import success_resp,failed_resp
from log_util.app_logger import logger
from app_server.models import SessionContext
from super_models.store_model import Store
import json, time
from app_server.response.errors import *
from app_server.models.favorite_model import FavoriteStore
from app_server.models.article_model import Article
from app_server.controllers.article_controller import article_to_dict
from sqlalchemy import or_,and_
from app_server.controllers.special_store_controller import convert_little_store
from math import acos,sin,cos,pi,radians,asin,sqrt
from sqlalchemy import func
from app_server.utils.imgtool import image_save
from werkzeug.datastructures import ImmutableMultiDict

node_store=Blueprint('store_layer',__name__,)


@node_store.route('/', methods=['GET'])
@basic_unpack
def store_detail():
    paras = request.args
    store_id = paras.get('store_id')
    with SessionContext() as session:
        store = session.query(Store).filter_by(store_id=store_id).first()
        if not store:
            return failed_resp(ERROR_Parameters)
        data = {}
        data['similars'] = None

        hot_articles = []
        articles = session.query(Article).filter_by(store_id=store_id,essence=True).limit(2).offset(0).all()
        for art in articles:
            art_dict = article_to_dict(art,session)
            hot_articles.append(art_dict)
        data['hot_articles'] = hot_articles
        for key, value in vars(store).items():
            if key == 'id' or key == '_sa_instance_state':
                continue
            if key == 'lng' and value or key == 'lat' and value:
                data[key] = float(value)
                continue
            if key == 'banners_list' and value or key == 'menus_list' and value:
                data[key] = json.loads(value)
                continue
            data[key] = value

        data['favorite'] = False
        # 是否已收藏该店铺
        user_id = paras.get('user_id')
        if user_id:
            favorite = session.query(FavoriteStore).filter_by(store_id=store_id, user_id=user_id).first()
            data['favorite'] = bool(favorite)

        return success_resp(data)


@node_store.route('/favorite', methods=['POST'])
@basic_unpack
@login_required
def store_favorite():
    body = request.json
    store_id = body.get('store_id')
    if 'add' in body:
        pass
    else:
        return failed_resp(ERROR_Parameters)
    add = body.get('add')
    user_id = request.args.get('user_id')
    if not store_id or not user_id:
        return failed_resp(ERROR_Parameters)
    with SessionContext() as session:
        fav = session.query(FavoriteStore).filter_by(store_id=store_id, user_id=user_id).first()
        if add and fav:
            session.result = failed_resp(ERROR_Store_ReFavorite)

        if not fav and not add:
            session.result = success_resp()

        if add and not fav:
            favorite = FavoriteStore()
            favorite.store_id = store_id
            favorite.user_id = user_id
            favorite.time = int(time.time())

            session.add(favorite)
            session.commit()

            session.result = success_resp()

        if fav and not add:
            session.delete(fav)
            session.commit()
            session.result = success_resp()

    return session.result


@node_store.route('/filter', methods=['GET'])
@basic_unpack
def store_filter():
    # 排序
    order = request.args.get('order')
    region_code = request.args.get('region_code')
    page = request.args.get('page')
    amount = request.args.get('amount')
    if not order or not region_code or not page or not amount:
        return failed_resp(ERROR_Parameters)

    page = int(page)
    amount = int(amount)
    offset = (page-1)*amount
    order = int(order)
    region_code = int(region_code)

    store_open = request.args.get('open')
    per = request.args.get('per')

    with SessionContext() as session:

        query = session.query(Store).filter_by(region_code=region_code)

        if order == 0:
            pass
        elif order == 1:
            query = query.order_by((Store.favorites_amount.desc()))
        elif order == 2:
            query = query.order_by((Store.favorites_amount.desc()))
        elif order == 3:
            query = query.order_by((Store.score.desc()))

        if store_open:
            store_open = int(store_open)
            now = int(time.time())
            if store_open == 0:
                query = query.filter(and_(Store.open_time < now, Store.close_time > now))
            else:
                query = query.filter(or_(Store.open_time > now, Store.close_time < now))

        if per:
            pass

        stores = query.limit(amount).offset(offset).all()

        data = []
        for store in stores:
            store_dict = convert_little_store(store)
            data.append(store_dict)

        session.result = success_resp(data)

    return session.result





def haversine(lon1, lat1, lon2, lat2):  # 经度1，纬度1，经度2，纬度2 （十进制度数）

    # 将十进制度数转化为弧度
    lon1, lat1, lon2, lat2 = map(radians, [lon1, lat1, lon2, lat2])

    # haversine公式
    dlon = lon2 - lon1
    dlat = lat2 - lat1
    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * asin(sqrt(a))
    r = 6380  # 地球平均半径，单位为公里
    return c * r * 1000

# def filter_stores():
#     with SessionContext() as session:
#         stores = session.execute('select * from Store where '
#                              'lat > {user_lat}-1 and lat < {user_lat} +1 and lng > {user_lng}-1 and lng < {user_lng} +1 '
#                              'order by ACOS(SIN(({user_lat} * 3.1415) / 180 ) *SIN((lat * 3.1415) / 180 ) +'
#                              'COS(({user_lat} * 3.1415) / 180 ) * COS((lat * 3.1415) / 180 ) *'
#                              'COS(({user_lng}* 3.1415) / 180 - (lng * 3.1415) / 180 ) ) * 6380 asc limit 10'.format(user_lat=user_lat,user_lng=user_lng))



@node_store.route('/list', methods=['GET'])
@basic_unpack
def store_list():
    region_code = request.args.get('region_code')
    page = request.args.get('page')
    amount = request.args.get('amount')
    if not region_code or not page or not amount:
        return failed_resp(ERROR_Parameters)

    page = int(page)
    amount = int(amount)
    offset = (page-1)*amount
    region_code = int(region_code)

    with SessionContext() as session:

        stores = session.query(Store).filter_by(region_code=region_code).limit(amount).offset(offset).all()
        data = []
        for store in stores:
            store_dict = convert_little_store(store)
            data.append(store_dict)

        session.result = success_resp(data)

    return session.result


@node_store.route('/setting', methods=['POST'])
@basic_unpack
def store_update():
    body = request.form
    if not body:
        body = request.json
    if not body:
        return failed_resp(ERROR_Parameters)
    else:
        store_id = body.get('store_id')
        with SessionContext() as session:
            store = session.query(Store).filter_by(store_id=store_id).first()
            if not store:
                return failed_resp(ERROR_Parameters)
            for key in body:
                if key == 'banners_list' or key == 'menus_list':
                    store.__setattr__(key,json.dumps(body[key]))
                    continue
                store.__setattr__(key,body[key])
            session.commit()
            return success_resp()


@node_store.route('/icon', methods=['POST'])
@basic_unpack
def store_icon():
    img = request.files['img']
    body = request.form
    if not body:
        body = request.json
    store_id = body.get('store_id')
    if not store_id:
        store_id = 0
    full_path = image_save(store_id, img)
    with SessionContext() as session:
        store = session.query(Store).filter_by(store_id=store_id).first()
        store.icon = full_path
        session.commit()
        data = {}
        data['icon'] = full_path
        session.result = success_resp(data)
    return session.result


@node_store.route('/banner_add', methods=['POST','OPTIONS'])
@basic_unpack
def banner_add():
    if request.method == 'OPTIONS':
        return success_resp()

    img = request.files['img']
    body = request.form
    if not body:
        body = request.json
    store_id = body.get('store_id')
    if not store_id:
        store_id = 0
    full_path = image_save(store_id, img)
    with SessionContext() as session:
        store = session.query(Store).filter_by(store_id=store_id).first()
        banner_list = store.banners_list
        banner_array = []
        if banner_list:
            banner_array = json.loads(banner_list)

        banner_array.append(full_path)

        store.banners_list = json.dumps(banner_array)
        session.commit()
        data = {}
        data['banner'] = full_path
        session.result = success_resp(data)
    return session.result


@node_store.route('/banner_delete', methods=['POST'])
@basic_unpack
def banner_delete():
    body = request.form
    if not body:
        body = request.json
    store_id = body.get('store_id')
    img = body.get('img')
    store_id_int = int(store_id)
    with SessionContext() as session:
        store = session.query(Store).filter_by(store_id=store_id_int).first()
        banner_list = store.banners_list
        banner_array = []
        if banner_list:
            banner_array = json.loads(banner_list)

        banner_array = filter(lambda x: x != img, banner_array)

        store.banners_list = json.dumps(banner_array)
        session.commit()
        data = {}
        session.result = success_resp(data)
    return session.result


@node_store.route('/menu_add', methods=['POST','OPTIONS'])
@basic_unpack
def menu_add():
    if request.method == 'OPTIONS':
        return success_resp()
    img = request.files['img']
    body = request.form
    if not body:
        body = request.json
    store_id = body.get('store_id')
    if not store_id:
        store_id = 0
    full_path = image_save(store_id, img)
    with SessionContext() as session:
        store = session.query(Store).filter_by(store_id=store_id).first()
        menu_list = store.menus_list
        menu_array = []
        if menu_list:
            menu_array = json.loads(menu_list)

        menu_array.append(full_path)

        store.menus_list = json.dumps(menu_array)
        session.commit()
        data = {}
        data['menu'] = full_path
        session.result = success_resp(data)
    return session.result


@node_store.route('/menu_delete', methods=['POST'])
@basic_unpack
def menu_delete():
    body = request.form
    if not body:
        body = request.json
    store_id = body.get('store_id')
    img = body.get('img')
    with SessionContext() as session:
        store = session.query(Store).filter_by(store_id=store_id).first()
        menu_list = store.menus_list
        menu_array = []
        if menu_list:
            menu_array = json.loads(menu_list)

        menu_array = filter(lambda x: x != img, menu_array)

        store.menus_list = json.dumps(menu_array)
        session.commit()
        data = {}
        session.result = success_resp(data)
    return session.result
