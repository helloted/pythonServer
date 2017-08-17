#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
HotCategoryModel控制
"""

from app_server.models.hot_category_model import HotCategory
from super_models.database import SessionContext
from app_server.response import dberror_handle


def get_hot_sotres(region_code=None):
    with SessionContext(dberror_handle) as session:
        hots = session.query(HotCategory).filter_by(region_code=region_code).all()
        hot_list = []
        for hot in hots:
            hot_dict = {}
            hot_dict['category'] = hot.category
            hot_dict['img'] = hot.img
            hot_dict['stores'] = hot.stores
            hot_list.append(hot_dict)
        return hot_list


def hot_category_add(category,img=None,stores=None,region_code=None):
    with SessionContext(dberror_handle) as session:
        hot_category = HotCategory()
        hot_category.category = category
        hot_category.img = img
        hot_category.stores = stores
        hot_category.region_code = region_code
        session.add(hot_category)
        session.commit()


def hot_category_update(id,category=None,img=None,stores=None,region_code=None):
    with SessionContext(dberror_handle) as session:
        hot_category = session.query(HotCategory).filter_by(id=id).first()
        if hot_category:
            if category:
                hot_category.category = category
            if img:
                hot_category.img = img
            if stores:
                hot_category.stores = stores
            if region_code:
                hot_category.region_code = region_code
            session.commit()
            return 0
        else:
            return 101

def hot_category_delete(id):
    with SessionContext(dberror_handle) as session:
        hot_category = session.query(HotCategory).filter_by(id=id).first()
        if hot_category:
            session.delete(hot_category)
            session.commit()
            return 0
        else:
            return 101

def hot_category_query(id):
    with SessionContext(dberror_handle) as session:
        hot_category = session.query(HotCategory).filter_by(id=id).first()
        return hot_category


def add_hot():
    hot_category_add('Chinese Food',img='http://pic.90sjimg.com/back_pic/00/04/27/49/850f91ae69da1df596423db51c0e8486.jpg',stores='1,2,3',region_code=1)
    hot_category_add('Western Food',
                     img='http://pic.90sjimg.com/back_pic/00/00/69/40/6244287a34ab20ff0956cec2d78aa44e.jpg',
                     stores='1,2,3,5', region_code=1)


if __name__ == '__main__':
    add_hot()
