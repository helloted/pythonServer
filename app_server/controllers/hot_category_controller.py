#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
HotCategoryModel控制
"""
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir,os.pardir))
from app_server.models.hot_category_model import HotCategory
from super_models.store_model import Store
from super_models.database import SessionContext
from app_server.response import dberror_handle


def get_hot_category(region_code=None):
    with SessionContext(dberror_handle) as session:
        hots = session.query(HotCategory).filter_by(region_code=region_code).all()
        hot_list = []
        for hot in hots:
            hot_dict = {}
            hot_dict['category'] = hot.category
            hot_dict['img'] = hot.category_img
            count = session.query(Store).filter(Store.special_type == 1, Store.region_code == region_code,
                                                 Store.category == hot.category).count()
            hot_dict['count'] = count
            hot_list.append(hot_dict)
        return hot_list


def hot_category_add(category,img=None,region_code=None):
    with SessionContext(dberror_handle) as session:
        hot_category = HotCategory()
        hot_category.category = category
        hot_category.category_img = img
        hot_category.region_code = region_code
        session.add(hot_category)
        session.commit()


def hot_category_update(id,category=None,img=None,region_code=None):
    with SessionContext(dberror_handle) as session:
        hot_category = session.query(HotCategory).filter_by(id=id).first()
        if hot_category:
            if category:
                hot_category.category = category
            if img:
                hot_category.category_img = img
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


def add_hot_category():
    hot_category_add('Steak',img='http://swindtech-img.oss-ap-southeast-1.aliyuncs.com/steak_for_hot.jpg',region_code=1)
    hot_category_add('SeaFood',
                     img='http://swindtech-img.oss-ap-southeast-1.aliyuncs.com/seafood_page.jpg', region_code=1)
    hot_category_add('Japanese',
                     img='http://swindtech-img.oss-ap-southeast-1.aliyuncs.com/japanese_for_hot.jpg', region_code=1)
    hot_category_add('Indian',
                     img='http://swindtech-img.oss-ap-southeast-1.aliyuncs.com/india_for_hot.jpeg', region_code=1)



def add_hot_store(store_id):
    with SessionContext(dberror_handle) as session:
        store = session.query(Store).filter_by(store_id=store_id).first()
        if store:
            store.special_type = 1;
            session.commit()
            return 0
        else:
            return 101



if __name__ == '__main__':
    stores = [1,2,3,5,6,10,11,12,13,14,15,17,20,22,23,24,25,26,30,32,33,35,36,39,]
    for i in stores:
        add_hot_store(i)
