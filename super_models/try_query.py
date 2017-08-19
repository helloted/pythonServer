
from super_models.database import Session
from super_models.store_model import Store
from super_models.device_model import Device


def query():
    session = Session()

    result = session.query(Device).filter(Store.name=='KFC',Device.store_id==Store.store_id).all()
    print result



if __name__ == '__main__':
    query()