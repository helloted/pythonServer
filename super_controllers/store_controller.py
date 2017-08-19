#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.07.03
HotStoreModel控制
"""

from super_controllers.id_dispath import get_store_id
from super_models.database import SessionContext
from app_server.response.resp import dberror_handle
from super_models.store_model import Store
import json


def store_add(region_code=None,district=None,name=None,phone=None,lng=None,lat=None,score=None,per=None,location=None,open_time=None,close_time=None,set_up=None):
    store_id = get_store_id()
    if store_id:
        store = Store()
        store.store_id = store_id
        store.region_code = region_code
        store.district = district
        store.name = name
        store.phone = phone
        store.lng = lng
        store.lat = lat
        store.score = score
        store.per = per
        store.location = location
        store.open_time = open_time
        store.close_time = close_time
        store.set_up = set_up

        with SessionContext() as session:
            session.add(store)
            session.commit()


def store_update(store_id,region_code=None,district=None,icon=None,name=None,phone=None,lng=None,lat=None,score=None,per=None,
                 location=None,open_time=None,close_time=None,set_up=None,banners_list=None,menus_list=None,services=None):
    with SessionContext(dberror_handle) as session:
        store = session.query(Store).filter_by(store_id=store_id).first()
        if store:
            if region_code:
                store.region_code = region_code
            if icon:
                store.icon = icon
            if district:
                store.district = district
            if name:
                store.name = name
            if phone:
                store.phone = phone
            if lng:
                store.lng = lng
            if lat:
                store.lat = lat
            if store:
                store.score = score
            if per:
                store.per = per
            if location:
                store.location = location
            if open_time:
                store.open_time = open_time
            if close_time:
                store.close_time = close_time
            if set_up:
                store.set_up = set_up
            if banners_list:
                store.banners_list = json.dumps(banners_list)
            if menus_list:
                store.menus_list = menus_list
            if services:
                store.services = services
            session.commit()
            return 0
        else:
            return 101


def store_delete(store_id):
    with SessionContext() as session:
        store = session.query(Store).filter_by(store_id=store_id).first()
        if store:
            session.delete(store)
            session.commit()
            return 0
        else:
            return 101


def store_query(store_id):
    with SessionContext(dberror_handle) as session:
        store = session.query(Store).filter_by(store_id=store_id).first()
        return store


if __name__ == '__main__':
    store_update(1,banners_list=['http://img.sj33.cn/uploads/allimg/201402/7-140206204500561.png',],menus_list=['http://img.sj33.cn/uploads/allimg/201402/7-140206204500561.png',],services='Wifi|Air condition')
    # store_add(name='HelloKitty',region_code=1)