from log_util.web_demo_logger import logger
from super_models.database import Session
from web_server.utils.response import response_failed
from web_server.utils import errors


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
            self.session.result = response_failed(errors.ERROR_DataBase)
        return True