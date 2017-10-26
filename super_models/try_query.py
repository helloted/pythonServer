
from super_models.database import Session
from super_models.store_model import Store
from super_models.device_model import Device
from super_models.order_model import Order


def query():
    session = Session()

    result = session.query(Device).filter(Store.name=='KFC',Device.store_id==Store.store_id).all()
    print result


def order_at():
    session = Session()
    all = session.query(Order).all()
    for order in all:
        print order.device_sn
    # order = Order()
    # order.device_sn = 'test_sn'
    # session = Session()
    # try:
    #     session.add(order)
    #     session.commit()
    # except Exception,e:
    #     print e
    # else:
    #     print 'finish'

if __name__ == '__main__':
    order_at()