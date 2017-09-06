from log_util.web_demo_logger import logger
from super_models.database import Session
from web_server.response.resp import failed_response


class SessionContext():
    def __init__(self,back_exc=False):
        self.__back_exc = back_exc

    def __enter__(self):
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.close()
        if exc_tb:
            self.session.rollback()
            logger.error(exc_val)
            if self.__back_exc:
                self.session.result = exc_val
            else:
                self.session.result = failed_response(1,'data base error')
        return True