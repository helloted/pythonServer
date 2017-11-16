#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.04
点评处理
"""
import gevent
from flask import Blueprint
from flask import request
from app_server.utils.request_handle import request_unpack,login_required
from app_server.response import success_resp,failed_resp
from app_server.response.errors import *
from app_server.models import SessionContext
from app_server.models.article_model import Article
from app_server.models.user_model import User
from app_server.utils.imgtool import image_save
import json, time
from super_controllers.id_dispath import get_article_id, get_comment_id
from app_server.models.comment_model import Comment
from app_server.models.favorite_model import LikeArticle,FavoriteArticle
from app_server.models.user_model import User
from app_server.controllers.article_controller import article_to_dict
from super_models.store_model import Store
from app_server.controllers.special_store_controller import convert_little_store
from log_util.app_logger import logger

node_article=Blueprint('article_layer',__name__,)


@node_article.route('/add', methods=['POST'])
@request_unpack
@login_required
def article_add(body):
    user_id = request.args.get('user_id')
    if not body:
        body = request.json
    deal_sn = body.get('deal_sn')
    store_id = body.get('store_id')
    score = body.get('score')
    per = body.get('per')
    anonymous = body.get('anonymous')
    if anonymous == '0':
        anonymous = False
    if anonymous == '1':
        anonymous = True
    text = body.get('text')

    if not deal_sn or not store_id:
        resp = failed_resp(ERROR_Parameters)
        logger.info(resp.log)
        return resp.data

    imgs = []
    img_count = 0
    img_files = request.files.getlist("imgs")
    for img in img_files:
        img_count += 1
        down_path = image_save(user_id,img)
        imgs.append(down_path)

    logger.info('after image')

    article_id = get_article_id()
    if article_id:
        article = Article()
        article.article_id = article_id
        article.poster_id = int(user_id)
        article.post_time = int(time.time())
        article.text = text
        article.imgs = json.dumps(imgs)
        article.img_count = img_count
        article.store_id = store_id
        article.deal_sn = deal_sn
        article.score = score
        article.per = per
        article.anonymous = anonymous

        with SessionContext() as session:
            store = session.query(Store).filter_by(store_id=store_id).first()
            if store:
                article.region_code = store.region_code
            session.add(article)
            session.commit()
            session.result = success_resp()
        logger.info('after session')
        logger.info(session.result.log)
        return session.result.data
    else:
        logger.info('after else')
        resp = failed_resp(ERROR_DataBase)
        logger.info(resp.log)
        return resp.data


@node_article.route('/list', methods=['GET'])
@request_unpack
def article_list():
    store_id = request.args.get('store_id')
    page = request.args.get('page')
    amount = request.args.get('amount')
    if not store_id or not page or not amount:
        resp = failed_resp(ERROR_Parameters)
        logger.info(resp.log)
        return resp.data

    page_int = int(page)
    amount_int = int(amount)

    offset = (page_int-1) * amount_int


    with SessionContext() as session:
        articles = session.query(Article).order_by((Article.post_time.desc())).\
                            filter_by(store_id=store_id).limit(amount_int).offset(offset).all()
        data = []
        for art in articles:
            artic_dict = article_to_dict(art,session)

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

            data.append(artic_dict)
        session.result = success_resp(data)

    logger.info(session.result.log)
    return session.result.data


@node_article.route('/', methods=['GET'])
@request_unpack
def article():
    article_id = request.args.get('article_id')
    if not article_id:
        resp = failed_resp(ERROR_Parameters)
        logger.info(resp.log)
        return resp.data

    with SessionContext() as session:
        article = session.query(Article).filter_by(article_id=article_id).first()
        if article:
            data = {}
            for key, value in vars(article).items():
                if key == 'id' or key == '_sa_instance_state':
                    continue
                if key == 'imgs' and value:
                    data[key] = json.loads(value)
                    continue
                data[key] = value

                poster_id = article.poster_id
                anonymous = article.anonymous
                if poster_id and not anonymous:
                    poster = session.query(User).filter_by(user_id=poster_id).first()
                    data['poster_id'] = poster_id
                    data['poster_name'] = poster.name
                    data['poster_icon'] = poster.icon
                else:
                    data['poster_id'] = 0
                    data['poster_name'] = 'anonymous poster'
                    data['poster_icon'] = 'www.baidu.com/png'

                # 评论
                comments = []
                coms = session.query(Comment).order_by((Comment.time.desc())).filter_by(article_id=article_id).limit(10).offset(0).all()
                for com in coms:
                    com_dict = {}
                    for key, value in vars(com).items():
                        if key == 'id' or key == '_sa_instance_state':
                            continue
                        com_dict[key] = value
                    commenter_id = com.commenter_id
                    commenter = session.query(User).filter_by(user_id=commenter_id).first()
                    com_dict['commenter_name'] = commenter.name
                    com_dict['commenter_icon'] = commenter.icon

                    comments.append(com_dict)

                data['comments'] = comments

                # 点赞的人
                like_users = []
                likes = session.query(LikeArticle).filter_by(article_id=article_id).all()
                for like in likes:
                    user = session.query(User).filter_by(user_id=like.user_id).first()
                    user_dict = {}
                    user_dict['user_id'] = user.user_id
                    user_dict['name'] = user.name
                    user_dict['icon'] = user.icon
                    like_users.append(user_dict)
                data['like_users'] = like_users

                # 收藏的人数
                favorite_amount = session.query(FavoriteArticle).filter_by(article_id=article_id).count()
                data['favorite_amount'] = favorite_amount

                comment_amount = session.query(Comment).filter_by(article_id=article_id).count()
                data['comment_amount'] = comment_amount

                like_amount = session.query(LikeArticle).filter_by(article_id=article_id).count()
                data['like_amount'] = like_amount


                # 收藏、点赞
                data['favorite'] = False
                data['like'] = False
                user_id = request.args.get('user_id')
                if user_id:
                    favorite = session.query(FavoriteArticle).filter_by(article_id=article_id, user_id=user_id).first()
                    data['favorite'] = bool(favorite)

                    like = session.query(LikeArticle).filter_by(article_id=article_id, user_id=user_id).first()
                    data['like'] = bool(like)

                store = session.query(Store).filter_by(store_id=article.store_id).first()
                store_dict = convert_little_store(store)

                data['store'] = store_dict
            session.result = success_resp(data)
        else:
            session.result = failed_resp(ERROR_Article_Null)

    logger.info(session.result.log)
    return session.result.data


@node_article.route('/delete', methods=['POST'])
@request_unpack
@login_required
def article_delete(body):
    article_id = body.get('article_id')
    if not article_id:
        resp = failed_resp(ERROR_Parameters)
        logger.info(resp.log)
        return resp.data
    with SessionContext() as session:
        article = session.query(Article).filter_by(article_id=article_id).first()
        if article:
            session.delete(article)
            session.commit()
            session.result = success_resp()
        else:
            session.result = failed_resp(ERROR_Article_Null)
    logger.info(session.result.log)
    return session.result.data


@node_article.route('/comment_add', methods=['POST'])
@request_unpack
@login_required
def comment_add(body):
    user_id = request.args.get('user_id')
    text = body.get('text')
    article_id = body.get('article_id')
    comment_type = int(body.get('type'))

    replied_user_id = None
    replied_user_name = None
    replied_comment_id = None

    if comment_type == 1:
        replied_comment_id = body.get('replied_comment_id')
        replied_user_id = body.get('replied_user_id')
        replied_user_name = body.get('replied_user_name')

        if not replied_user_name or not replied_user_id or not replied_comment_id:
            resp = failed_resp(ERROR_Parameters)
            logger.info(resp.log)
            return resp.data

    comment_id = get_comment_id()
    if comment_id:
        comment = Comment()
        comment.article_id = article_id
        comment.comment_id = comment_id
        comment.commenter_id = int(user_id)
        comment.time = int(time.time())
        comment.text = text
        comment.type = comment_type

        comment.replied_comment_id = replied_comment_id
        comment.replied_user_id = replied_user_id
        comment.replied_user_name = replied_user_name

        with SessionContext() as session:
            session.add(comment)
            session.commit()

            com_dict = {}

            user = session.query(User).filter_by(user_id=user_id).first()

            com_dict['commenter_name'] = user.name
            com_dict['commenter_icon'] = user.icon
            com_dict['article_id'] = article_id
            com_dict['comment_id'] = comment_id
            com_dict['commenter_id'] = int(user_id)
            com_dict['time'] = int(time.time())
            com_dict['text'] = text
            com_dict['type'] = comment_type

            com_dict['replied_comment_id'] = replied_comment_id
            com_dict['replied_user_id']= replied_user_id
            com_dict['replied_user_name'] = replied_user_name

            session.result = success_resp(com_dict)
        logger.info(session.result.log)
        return session.result.data
    else:
        resp = failed_resp(ERROR_DataBase)
        logger.info(resp.log)
        return resp.data


@node_article.route('/comments', methods=['GET'])
@request_unpack
def comments():
    article_id = request.args.get('article_id')
    page = request.args.get('page')
    amount = request.args.get('amount')
    if not article_id or not page or not amount:
        resp = failed_resp(ERROR_Parameters)
        logger.info(resp.log)
        return resp.data

    page_int = int(page) - 1
    amount_int = int(amount)
    offset = page_int * amount_int
    with SessionContext() as session:
        data = []
        results = session.query(Comment).order_by((Comment.time.desc())).filter_by(article_id=article_id).limit(amount_int).offset(offset).all()
        for com in results:
            com_dict = {}
            for key, value in vars(com).items():
                if key == 'id' or key == '_sa_instance_state':
                    continue
                com_dict[key] = value

            commenter_id = com.commenter_id
            commenter = session.query(User).filter_by(user_id=commenter_id).first()
            com_dict['commenter_name'] = commenter.name
            com_dict['commenter_icon'] = commenter.icon

            data.append(com_dict)
        session.result = success_resp(data)
    logger.info(session.result.log)
    return session.result.data


@node_article.route('/comment_delete', methods=['POST'])
@request_unpack
@login_required
def comment_delete(body):
    comment_id = body.get('comment_id')
    with SessionContext() as session:
        comment = session.query(Comment).filter_by(comment_id=comment_id).first()
        if comment:
            session.delete(comment)
            session.commit()
            session.result = success_resp()
        else:
            session.result = failed_resp(ERROR_Comment_Null)
    logger.info(session.result.log)
    return session.result.data


@node_article.route('/like', methods=['POST'])
@request_unpack
@login_required
def article_like(body):
    article_id = body.get('article_id')
    if 'add' in body:
        pass
    else:
        return failed_resp(ERROR_Parameters)
    add = body.get('add')
    user_id = request.args.get('user_id')
    if not article_id or not user_id:
        resp = failed_resp(ERROR_Parameters)
        logger.info(resp.log)
        return resp.data
    with SessionContext() as session:
        like = session.query(LikeArticle).filter_by(article_id=article_id, user_id=user_id).first()

        if not like and not add:
            session.result = success_resp()

        if add and like:
            session.result = failed_resp(ERROR_Article_ReLike)

        if add and not like:
            like = LikeArticle()
            like.article_id = article_id
            like.user_id = user_id
            like.time = int(time.time())

            session.add(like)
            session.commit()

            session.result = success_resp()

        if like and not add :
            session.delete(like)
            session.commit()
            session.result = success_resp()

    logger.info(session.result.log)
    return session.result.data


@node_article.route('/favorite', methods=['POST'])
@request_unpack
@login_required
def article_favorite(body):
    article_id = body.get('article_id')
    if 'add' in body:
        pass
    else:
        resp = failed_resp(ERROR_Parameters)
        logger.info(resp.log)
        return resp.data
    add = body.get('add')
    user_id = request.args.get('user_id')
    if not article_id or not user_id:
        resp = failed_resp(ERROR_Parameters)
        logger.info(resp.log)
        return resp.data
    with SessionContext() as session:
        fav = session.query(FavoriteArticle).filter_by(article_id=article_id, user_id=user_id).first()
        if add and fav:
            session.result = failed_resp(ERROR_Article_ReFavorite)

        if not fav and not add:
            session.result = success_resp()


        if add and not fav:
            favorite = FavoriteArticle()
            favorite.article_id = article_id
            favorite.user_id = user_id
            favorite.time = int(time.time())

            session.add(favorite)
            session.commit()

            session.result = success_resp()

        if fav and not add:
            session.delete(fav)
            session.commit()
            session.result = success_resp()

    logger.info(session.result.log)
    return session.result.data


@node_article.route('/like_list', methods=['GET'])
@request_unpack
def like_list():
    article_id = request.args.get('article_id')
    page = request.args.get('page')
    amount = request.args.get('amount')
    if not article_id or not page or not amount:
        resp = failed_resp(ERROR_Parameters)
        logger.info(resp.log)
        return resp.data

    page_int = int(page)
    amount_int = int(amount)

    offset = (page_int-1) * amount_int
    with SessionContext() as session:
        likes = session.query(LikeArticle).filter_by(article_id=article_id).limit(amount_int).offset(offset).all()
        # 点赞的人
        like_users = []
        for like in likes:
            user = session.query(User).filter_by(user_id=like.user_id).first()
            user_dict = {}
            user_dict['user_id'] = user.user_id
            user_dict['name'] = user.name
            user_dict['icon'] = user.icon
            like_users.append(user_dict)

        session.result = success_resp(like_users)

    logger.info(session.result.log)
    return session.result.data



