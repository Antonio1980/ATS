from src.base import logger
from src.base.log_decorator import automation_logger


class AutomationError(BaseException):
    
    def __init__(self, *args, **kwargs):
        super(BaseException, self).__init__(*args)
        AutomationError.__init__(self, *args, **kwargs)

    @automation_logger(logger)
    def __str__(self):
        return "Automation error is occurred: {0}".format(self.args)

    @automation_logger(logger)
    def __repr__(self):
        return "Automation error is occurred: {0}".format(self.__str__())
