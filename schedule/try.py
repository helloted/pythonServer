import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from super_models.daily_model import StoreDaily
from super_models.database import Session
import datetime,time
from super_models.deal_model import Deal
from sqlalchemy import func
from super_models.history_model import EventsHistroy, OfflineHistroy


def save_daily():
    today = datetime.date.today()
    zero = str(today) + ' 00:00:00'
    st = time.strptime(zero, '%Y-%m-%d %H:%M:%S')
    yesterday_24_time = int(time.mktime(st)) * 1000
    yesterday_zero_time = yesterday_24_time - 1000* 60 * 60 * 24
    today_24_time = yesterday_24_time + 1000* 60 * 60 * 24

    session = Session()
    try:
        results = session.query(
            Deal.store_id,
            Deal.store_name,
            func.count('*'),
            func.sum(Deal.total_price),
            func.sum(Deal.tax)).\
            filter(Deal.time.between(yesterday_zero_time,yesterday_24_time))\
            .group_by(Deal.store_id).all()
    except Exception,e:
        session.rollback()
        print e
    else:
        for res in results:
            print 'store_name',res[0],res[1]
            store_daily = StoreDaily()
            store_daily.time = yesterday_zero_time/1000
            store_daily.datetime = datetime.datetime.fromtimestamp(yesterday_zero_time/1000)
            store_daily.store_id = int(res[0])
            store_daily.store_name = res[1]
            store_daily.total_count = int(res[2])
            store_daily.total_price = int(res[3])
            store_daily.total_tax = int(res[4])
            # session.add(store_daily)
            #
            pass_dates = []
            for i in xrange(4):
                pass_day = yesterday_zero_time/1000 - 60 * 60 * 24 * 7 * (i+1)
                pass_dates.append(pass_day)
            #
            # ave = session.query(func.avg(StoreDaily.total_price)).filter(StoreDaily.time.in_(pass_dates),StoreDaily.store_id==store_daily.store_id).scalar()
            #
            # if not ave:
                ave = session.query(StoreDaily.total_price).filter(StoreDaily.time== yesterday_zero_time/1000 - 60 * 60 * 24,
                                                                       StoreDaily.store_id == store_daily.store_id).scalar()

            print ave
            #
            # if ave:
            #     value = ave - store_daily.total_price
            #     float_value = float(value) / float(ave)
            #     if float_value > 0.1 or float_value < -0.1:
            #         history = EventsHistroy()
            #         history.store_id = store_daily.store_id
            #         history.store_name = store_daily.store_name
            #         history.type = 3
            #         history.status = 0
            #         history.value = value
            #         history.float_value = float_value
            #         history.time = yesterday_zero_time / 1000
            #         session.add(history)

        # session.commit()
    finally:
        session.close()


if __name__ == '__main__':
    save_daily()