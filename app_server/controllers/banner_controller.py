#encoding:utf-8

"""
caohaozhi@swindtech.com
2017.06.27
Banner处理
"""

from super_models.database import  SessionContext
from super_controllers.id_dispath import get_banner_id
from app_server.models.banner_model import Banner
from app_server.response import dberror_handle

def get_current_banners(region_code):
    with SessionContext(dberror_handle) as session:
        banner_list = session.query(Banner).filter_by(region_code=region_code).all()
        banners = []
        for banner in banner_list:
            banner_dict = {}
            banner_dict['banner_id'] = banner.banner_id
            banner_dict['img'] = banner.img
            banner_dict['url'] = banner.url
            banner_dict['type'] = banner.type
            banners.append(banner_dict)
        return banners


def banner_add(region_code=None,img=None,start_time=None,end_time=None,type=None,url=None):
    banner_id = get_banner_id()
    if banner_id:
        banner = Banner()
        banner.banner_id = banner_id
        banner.region_code = region_code
        banner.img = img
        banner.start_time = start_time
        banner.end_time = end_time
        banner.type = type
        banner.url = url

        with SessionContext(dberror_handle) as session:
            session.add(banner)
            session.commit()


def banner_update(banner_id=None,region_code=None,img=None,start_time=None,end_time=None,type=None,url=None):
    with SessionContext(dberror_handle) as session:
        banner = session.query(Banner).filter_by(banner_id=banner_id).first()
        if banner:
            if region_code:
                banner.region_code = region_code
            if img:
                banner.img = img
            if start_time:
                banner.start_time = start_time
            if end_time:
                banner.end_time = end_time
            if type:
                banner.type = type
            if url:
                banner.url = url
            session.commit()
            return 0
        else:
            return 101


def banner_delete(banner_id=None):
    with SessionContext(dberror_handle) as session:
        banner = session.query(Banner).filter_by(banner_id=banner_id).first()
        if banner:
            session.delete(banner)
            session.commit()
            return 0
        else:
            return 101


def banner_query(banner_id=None):
    with SessionContext(dberror_handle) as session:
        banner = session.query(Banner).filter_by(banner_id=banner_id).first()
        return banner


def add():
    banner_add(region_code=1,\
               img='http://swindtech-img.oss-ap-southeast-1.aliyuncs.com/e47d0eb4c49a1b0b215306d8a3a1db6b.jpg',\
               start_time=1499069804,end_time=1599069804,\
               type=1,url='www.qotaku.com/?store_id=2')
    banner_add(region_code=1,\
               img='http://swindtech-img.oss-ap-southeast-1.aliyuncs.com/b611ee3bab2cae22b9aa1bac0bc40dc0.jpg',\
               start_time=1499069804,end_time=1599069804,\
               type=1,url='www.qotaku.com/?store_id=1')
    banner_add(region_code=1,\
               img='http://swindtech-img.oss-ap-southeast-1.aliyuncs.com/e53012779b67adcbb6f2d1e3366562ac.jpeg',\
               start_time=1499069804,end_time=1599069804,\
               type=1,url='www.qotaku.com/?store_id=3')


if __name__ == '__main__':
    add()
    # banner_update(banner_id=1,type=1,url='www.qotaku.com/?store_id=1',img='http://pic.90sjimg.com/back_pic/qk/back_origin_pic/00/01/42/6c6cb1412c93e745ea34e187a5be04b1.jpg')


