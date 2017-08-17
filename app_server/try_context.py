
from super_models.database import Session
from app_server.models.user_model import User


def handel_error(exec_val):
    print 'enter the handel error'
    return 'i have handle this error'


class SessionContext():

    def __init__(self,exception_handle=None):
        self.exception_handle = exception_handle

    def __enter__(self):
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        if exc_tb:
            print 'db_error:',exc_val
            self.session.rollback()
            self.session.result = 'this is db error'
            if self.exception_handle:
                self.exception_handle(exc_val)
        self.session.close()
        return True





def try_one():
    with SessionContext(handel_error) as session:
        user = session.query(User).filter_by(user_id=1).first()
        session.result = user.name
        print 'contine to'
        # return user.name

    print 'session:',session

    return session.result



if __name__ == '__main__':
    name =  try_one()
    print name
