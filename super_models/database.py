#coding=utf-8

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from contextlib import contextmanager

user = 'root'
password = 'sql$HeF#pass'
port = '3306'
database_name = 'server'
char = 'utf8'

data_url = 'mysql+pymysql://{user}:{password}@localhost:{port}/{database_name}'.format(**locals())

# 最大连接处
engine = create_engine(data_url,max_overflow=10,connect_args={'charset':'utf8'},echo=False)

Base = declarative_base()

Session = sessionmaker(bind=engine)


class SessionContext():
    def __init__(self,exception_handle=None):
        self.exception_handle = exception_handle

    def __enter__(self):
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        if exc_tb:
            print 'error',exc_val
            self.session.rollback()
            if self.exception_handle:
                self.exception_handle(exc_val)
        return False


@contextmanager
def session_scope():
    session = Session()
    try:
        yield session
        session.commit()
    except:
        session.rollback()
        raise
    finally:
        session.close()