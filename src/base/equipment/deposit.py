from src.base import logger
from src.base.log_decorator import automation_logger


class Deposit(object):

    def __init__(self, _id=0):
        self.id = _id
        self.customer_id = 0
        self.guid = ""
        self.currency_id = 0
        self.amount = 0

    def __repr__(self):
        return "Deposit ID: %d, Customer ID: %d, GUID: %s" % (int(self.id), int(self.customer_id), self.guid)

    @automation_logger(logger)
    def set_deposit(self, currency_id, amount):
        if self.customer_id != 0:
            self.currency_id = currency_id
            self.amount = amount
