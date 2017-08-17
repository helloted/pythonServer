#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
StoreModel控制
"""

from super_models.store_model import Store
from super_models.database import SessionContext
from app_server.response import dberror_handle

def convert_little_store(store):
    little = {}
    little['store_id'] = store.store_id
    little['name'] = store.name
    little['score'] = store.score
    little['per'] = store.per
    little['comment_amount'] = store.comment_amount
    little['lng'] = 0
    if store.lng:
        little['lng'] = float(store.lng)
    little['lat'] = 0
    if store.lat:
        little['lat'] = float(store.lat)
    little['district'] = store.district
    little['icon'] = store.icon
    little['category'] = store.category
    return little


def get_recommend_stores(region_code=None):
    with SessionContext(dberror_handle) as session:
        stores = session.query(Store).filter_by(region_code=region_code).all()
        recommends = []
        for store in stores:
            little = convert_little_store(store)
            recommends.append(little)
        return recommends
