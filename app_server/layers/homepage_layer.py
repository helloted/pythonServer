#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.01
APP首页处理
"""
import gevent
from flask import Blueprint
from flask import request
from app_server.utils.request_handle import request_unpack
from app_server.controllers.banner_controller import get_current_banners
from app_server.controllers.hot_category_controller import get_hot_sotres
from app_server.controllers.special_store_controller import get_recommend_stores
from app_server.response import success_resp,failed_resp
from app_server.models import SessionContext
from app_server.models.article_model import Article
from app_server.models.favorite_model import LikeArticle,FavoriteArticle
from app_server.models.user_model import User
from app_server.models.comment_model import Comment
import json
from app_server.response import errors
from log_util.app_logger import logger

node_homepage=Blueprint('homepage_layer',__name__,)


@node_homepage.route('/', methods=['GET'])
@request_unpack
def homepage():
    paras = request.args
    region_code = paras.get('region_code')

    worker_banners = gevent.spawn(get_current_banners, region_code)
    worker_hots = gevent.spawn(get_hot_sotres, region_code)
    worker_recommends = gevent.spawn(get_recommend_stores, region_code)
    gevent.joinall([worker_banners, worker_hots, worker_recommends])

    banners = worker_banners.value
    hot_stores = worker_hots.value
    recommend_stores = worker_recommends.value

    data = {}
    data['banners'] = banners
    data['hots'] = hot_stores
    data['recomments'] = recommend_stores

    return success_resp(data).data


@node_homepage.route('/banners', methods=['GET'])
@request_unpack
def banner_query():
    paras = request.args
    region_code = paras.get('region_code')

    banners = get_current_banners(region_code)
    data = banners

    resp = success_resp(data)
    logger.info(resp.log)

    return resp.data


@node_homepage.route('/hots', methods=['GET'])
@request_unpack
def hots():
    paras = request.args
    region_code = paras.get('region_code')

    hots = get_hot_sotres(region_code)
    data = hots

    return success_resp(data).data


@node_homepage.route('/recommands', methods=['GET'])
@request_unpack
def recommands():
    paras = request.args
    region_code = paras.get('region_code')

    recommands = get_recommend_stores(region_code)

    data = recommands

    return success_resp(data).data


@node_homepage.route('/goods_show', methods=['GET'])
@request_unpack
def goods_show():
    paras = request.args
    region_code = paras.get('region_code')
    page = request.args.get('page')
    amount = request.args.get('amount')
    if not region_code or not page or not amount:
        return failed_resp(errors.ERROR_Parameters)

    page_int = int(page)
    amount_int = int(amount)

    offset = (page_int-1) * amount_int

    with SessionContext() as session:
        results = session.query(Article).order_by((Article.post_time.desc())).filter(Article.essence==True,Article.img_count > 0,Article.region_code==region_code).limit(amount_int).offset(offset).all()

        data = []
        for art in results:
            artic_dict = {}
            if art.imgs:
                imgs = json.loads(art.imgs)
                if len(imgs):
                    artic_dict['cover'] = imgs[0]
                else:
                    artic_dict['cover'] = 'http://swindtech-img.oss-ap-southeast-1.aliyuncs.com/test.webp'

            artic_dict['article_id'] = art.article_id
            artic_dict['post_time'] = art.post_time

            # 收藏的人数
            favorite_amount = session.query(FavoriteArticle).filter_by(article_id=art.article_id).count()
            artic_dict['favorite_amount'] = favorite_amount

            comment_amount = session.query(Comment).filter_by(article_id=art.article_id).count()
            artic_dict['comment_amount'] = comment_amount

            like_amount = session.query(LikeArticle).filter_by(article_id=art.article_id).count()
            artic_dict['like_amount'] = like_amount

            # 收藏、点赞
            artic_dict['favorite'] = False
            artic_dict['like'] = False
            user_id = request.args.get('user_id')
            if user_id:
                favorite = session.query(FavoriteArticle).filter_by(article_id=art.article_id, user_id=user_id).first()
                artic_dict['favorite'] = bool(favorite)

                like = session.query(LikeArticle).filter_by(article_id=art.article_id, user_id=user_id).first()
                artic_dict['like'] = bool(like)

            # 点评人信息
            poster_id = art.poster_id
            anonymous = art.anonymous
            if poster_id and not anonymous:
                poster = session.query(User).filter_by(user_id=poster_id).first()
                artic_dict['poster_id'] = poster_id
                artic_dict['poster_name'] = poster.name
                artic_dict['icon'] = poster.icon
            else:
                artic_dict['poster_id'] = 0
                artic_dict['poster_name'] = 'anonymous'
                artic_dict['icon'] = 'http://swindtech-img.oss-ap-southeast-1.aliyuncs.com/89f627585abd1d9cb56fd72e2e119b32.webp'

            data.append(artic_dict)

        session.result = success_resp(data)
    logger.info(session.result.log)
    return session.result.data


