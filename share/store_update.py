from super_models.database import Session, SessionContext
from super_models.store_model import Store
import time

# district = Column(String(64))
# icon = Column(String(128))
#
# name = Column(String(50))
# phone = Column(String(16))
#
# lng = Column(DECIMAL(13, 10), default=0)
#
# lat = Column(DECIMAL(13, 10), default=0)
#
# score = Column(Float, default=4.0)
# per = Column(Integer, default=0)
#
# comment_amount = Column(Integer, default=0)
#
# favorites_amount = Column(Integer, default=0)
#
# location = Column(String(256))
#
# category = Column(String(64))
#
# open_time = Column(Integer, default=0)
#
# close_time = Column(Integer, default=0)
#
# set_up = Column(BigInteger, default=0)
#
# banners_list = Column(JSON)
#
# menus_list = Column(JSON)
#
# services = Column(String(512))
#
# cuisines = Column(String(256))

def update_store():
    with SessionContext() as session:
        store = session.query(Store).filter_by(store_id=3).first()
        if store:
            store.phone = '400 800 8820'
            store.region_code = 1
            store.score = 4.5
            store.district = 'nanshan'
            store.per = 50000
            store.icon = 'http://img.sj33.cn/uploads/allimg/201402/7-140206204500561.png'
            store.comment_amount = 5
            store.lng = 113.9481981559
            store.lat = 22.5366229689
            session.commit()



if __name__ == '__main__':
    time_now = int(time.time())
    time_local = time.localtime(time_now)
    print time.strftime("%Y%m%d%H%M%S", time_local)

