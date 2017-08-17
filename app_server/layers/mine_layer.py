#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.10
我的页面网络请求
"""
from flask import Blueprint
from flask import request
from app_server.utils.request_handle import basic_unpack,login_required
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


node_mine=Blueprint('mine_layer',__name__,)


@node_mine.route('/favorite_store', methods=['GET'])
@basic_unpack
@login_required
def favorite_store():
    user_id = request.args.get('user_id')
    with SessionContext() as session:
        favorites = session.query(FavoriteStore).filter_by(user_id=user_id).all()
        data = []
        for fav in favorites:
            store = session.query(Store).filter_by(store_id=fav.store_id).first()
            little = convert_little_store(store)
            data.append(little)
        session.result = success_resp(data)
    return session.result


@node_mine.route('/favorite_article', methods=['GET'])
@basic_unpack
@login_required
def favorite_article():
    user_id = request.args.get('user_id')
    with SessionContext() as session:
        favorites = session.query(FavoriteArticle).filter_by(user_id=user_id).all()
        data = []
        for fav in favorites:
            article = session.query(Article).filter_by(article_id=fav.article_id).first()
            dict =article_to_dict(article,session)
            data.append(dict)
        session.result = success_resp(data)
    return session.result


@node_mine.route('/post', methods=['GET'])
@basic_unpack
def article_list():
    user_id = request.args.get('user_id')
    if not user_id:
        return failed_resp(ERROR_Parameters)

    with SessionContext() as session:
        articles = session.query(Article).filter_by(poster_id=user_id).all()
        data = []
        for art in articles:
            one = {}
            for key, value in vars(art).items():
                if key == 'id' or key == '_sa_instance_state':
                    continue
                if key == 'imgs' and value:
                    one[key] = json.loads(value)
                    continue
                one[key] = value

            poster_id = art.poster_id
            anonymous = art.anonymous
            if poster_id and not anonymous:
                poster = session.query(User).filter_by(user_id=poster_id).first()
                one['poster_id'] = poster_id
                one['poster_name'] = poster.name
                one['icon'] = poster.icon
            else:
                one['poster_id'] = None
                one['poster_name'] = None
                one['icon'] = None
            data.append(one)
        session.result = success_resp(data)

    return session.result