from src.base import logger
from src.base.log_decorator import automation_logger


class Transaction(object):

    def __init__(self):
        self.type_id = 0
        self.customer_id = 0
        self.currency_id = 0
        self.amount = 0.0
        self.guid = ""
        self.operation_reference = None

    def __repr__(self):
        return "Transaction type: %d, customer_id: %d, currency_id: %d, amount: %d, guid: %s, reference: %s" % \
               (self.type_id, self.customer_id, self.currency_id, self.amount, self.guid, self.operation_reference)

    @automation_logger(logger)
    def set_transaction(self, type_id, customer_id, currency_id, amount, guid, operation_reference):
        self.type_id = type_id
        self.customer_id = customer_id
        self.currency_id = currency_id
        self.amount = amount
        self.guid = guid
        self.operation_reference = operation_reference
        return self
