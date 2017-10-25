#coding=utf-8
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from super_models.deal_status_model import DealStatus
from super_models.database import Session
import time
from celery import Celery

broker_url = 'redis://localhost:6379/0'
backend_url = 'redis://localhost:6379/1'
client = Celery('send_mail', backend=backend_url, broker=broker_url)


def celery_send_mail(to_list,subject,msg):
    client.send_task('send_mail.send_mail', (to_list, subject, msg))


def check_deals():
    session = Session()

    yestday_24_msec= zero_point_time_msec()
    yestday_0_msec = yestday_24_msec - 60 * 60 * 24 * 1000
    today_24_msec = yestday_24_msec + 60 * 60 * 24 * 1000

    received_count = session.query(DealStatus).filter(DealStatus.receive_time.between(yestday_0_msec,yestday_24_msec)).count()
    convert_success = session.query(DealStatus).filter(
        DealStatus.receive_time.between(yestday_0_msec,yestday_24_msec),DealStatus.status==1).count()
    convert_failed = session.query(DealStatus).filter(
        DealStatus.receive_time.between(yestday_0_msec,yestday_24_msec),DealStatus.status==2).count()
    did_not = received_count - convert_success - convert_failed
    order = session.query(DealStatus).filter(
        DealStatus.receive_time.between(yestday_0_msec,yestday_24_msec),DealStatus.deal_type==1).count()


    time_0 = int(yestday_0_msec/1000)
    str_0 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_0))

    time_24 = int(yestday_24_msec/1000) - 1
    str_24 = time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time_24))

    msg = '从 {start} 至 {end}, 一共接收小票{received}单，其中未解析{did_not}单，解析失败{failed}单，解析成功{success}单，里面有订单共{order}单'\
        .format(start=str_0,end=str_24,received= received_count,did_not=did_not,failed= convert_failed,success=convert_success,order=order)

    to_list = ['caohaozhi@swindtech.com','xiaojing@swindtech.com','wuliangwang@swindtech.com']
    subject = 'Convert_Server 解析统计'
    celery_send_mail(to_list,subject,msg)



def zero_point_time_msec():
    t = time.localtime(time.time())
    time_0 = time.mktime(time.strptime(time.strftime('%Y-%m-%d 00:00:00', t),'%Y-%m-%d %H:%M:%S'))
    time_0_msec = time_0 * 1000

    return int(time_0_msec)


if __name__ == '__main__':
    check_deals()
