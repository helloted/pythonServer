
import banner_model
import user_model
import hot_category_model
import favorite_model
import article_model
import comment_model
from super_models.database import Session
from log_util.app_logger import logger
from app_server.response import failed_resp
from app_server.response.errors import ERROR_DataBase

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
            logger.info(exc_val)
            if self.__back_exc:
                self.session.result = exc_val
            else:
                self.session.result = failed_resp(ERROR_DataBase)
        return True