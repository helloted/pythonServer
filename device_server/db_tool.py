from log_util.device_logger import logger
from super_models.database import Session
import traceback

class SessionContext():

    def __enter__(self):
        self.session = Session()
        return self.session

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.session.exc = False
        self.session.close()
        if exc_tb:
            self.session.rollback()
            logger.error(exc_val)
            logger.error(traceback.format_exc())
            self.session.exc = True
            self.session.exc_val = exc_val
        return True