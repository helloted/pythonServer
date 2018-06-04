#coding=utf-8
import sys, os; sys.path.append(os.path.join(os.path.dirname(__file__), os.pardir))
from models.database import SessionContext
from models.QRmodel import QRModel
import time
from sqlalchemy import func

def read_txt():
    with open('code20180404.txt','r') as file:
        sn_list = []
        url_list = []
        while True:
            line = file.readline()
            if line:
                sn,url = line.split(',')
                url = url.strip('\n')
                code_value = url.split('com/')[1]
                sn_list.append(int(sn))
                url_list.append(code_value)
            else:
                break
        print len(sn_list)
        sql_list = []
        temp = 0
        for i in xrange(len(sn_list)):
            if temp < 1000:
                temp += 1
            else:
                insert_model(sql_list)
                temp = 1
                sql_list = []
            sql = {'sn':sn_list[i],'code':url_list[i],'history_sn':1}
            sql_list.append(sql)

        insert_model(sql_list)
    print 'finish===='


def insert_model(sql_list):
    with SessionContext() as session:
        session.execute(QRModel.__table__.insert(), sql_list)
        session.commit()



def update():
    with SessionContext() as session:
        session.execute(
            QRModel.__table__.update().where(QRModel.sn<10000).values(code='www.clubori.com')
        )
        session.commit()
    print 'finish update'


    # # 分配时间
    # dispatch_1_time = Column(BigInteger,default=0)
    #
    # # 分配给了谁
    # dispatch_1_uid = Column(Integer)
    #
    # # 这一层分配到的类别
    # dispatch_1_name = Column(String(64))

def dispatch():
    dis_time = int(time.time())
    start = 10000021
    end = 10000030
    with SessionContext() as session:
        session.execute(
            QRModel.__table__.update().where(QRModel.sn>start).where(QRModel.sn<end).values(dispatch_1_time=dis_time,dispatch_1_uid=1)
        )
        session.commit()
    print 'dispatch_finish'


def insert():
    with SessionContext() as session:
        session.execute(
            QRModel.__table__.insert(),[{'name': 'hello', 'age': 10} for i in xrange(10000)]
        )


def query():
    with SessionContext() as session:
        res = session.query(QRModel,func.count(QRModel.sn)).filter(QRModel.dispatch_1_uid==1).group_by(QRModel.dispatch_1_time).all()
        for obj in res:
            start = obj[0].sn
            count = obj[1]
            print start,count


def read_all():
    url_dic = {}
    with open('code20180415.txt','r') as file:
        while True:
            line = file.readline()
            if line:
                sn,url = line.split(',')
                url = url.strip('\n')
                http,res_str = url.split('com/')
                print res_str,len(res_str)
                value = url_dic.get(res_str)
                if value:
                    print sn
                else:
                    url_dic[res_str] = 'all'
            else:
                break


if __name__ == '__main__':
    read_txt()
