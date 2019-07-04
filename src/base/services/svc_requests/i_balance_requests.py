from src.base import logger
from src.base.utils.utils import Utils
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.request_constants import *


class IBalanceServiceRequest:
    def __init__(self):
        super(IBalanceServiceRequest, self).__init__()
        self.id = "1"
        self.method = "balance."
        self.params = {}

    def to_json(self):
        return Utils.to_json(self)

    @automation_logger(logger)
    def get(self, customer_id: int, currency_id: int):
        """
        Build request body for IBalanceService.get_currency_balance()
        :param customer_id: ID of a customer.
        :param currency_id: ID of a currency.
        :return: Request body as json dump string.
        """
        self.method += "get"
        self.params[CUSTOMER_ID] = customer_id
        self.params[CURRENCY_ID] = currency_id
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def get_all(self, customer_id: int):
        """
        Build request body for IBalanceService.get_all_currencies_balance()
        :param customer_id: ID of a customer.
        :return: Request body.
        """
        self.method += "getAll"
        self.params[CUSTOMER_ID] = customer_id
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def get_subtract_transactions(self, customer_id: int, currency_id: int):
        """
        Build request body for IBalanceService.get_all_currencies_balance()
        :param customer_id: ID of a customer.
        :param currency_id: ID of a currency.
        :return: Request body as json dump string.
        """
        self.method += "getSubtractTransactions"
        self.params[CUSTOMER_ID] = customer_id
        self.params[CURRENCY_ID] = currency_id
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def add(self, customer_id: int, currency_id: int, deposit_amount: float):
        """
        Build request body for IBalanceService.add_balance()
        :param customer_id: Customer ID
        :param currency_id: Currency ID
        :param deposit_amount: Amount for deposit- float
        :return: Request body as json dump string.
        """
        self.method += "add"
        self.params[CUSTOMER_ID] = customer_id
        self.params[CURRENCY_ID] = currency_id
        self.params[AMOUNT] = deposit_amount
        self.params[METADATA] = {}
        self.params[METADATA][OPERATION_REFERENCE] = "QA-test"
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def subtract(self, customer_id: int, currency_id: int, subtract_amount: float):
        """
        Build request body for IBalanceService.subtract_balance()
        :param customer_id: Customer ID
        :param currency_id: Currency ID
        :param subtract_amount: Amount
        :return: Request body as json dump string.
        """
        self.method += "subtract"
        self.params[CUSTOMER_ID] = customer_id
        self.params[CURRENCY_ID] = currency_id
        self.params[AMOUNT] = subtract_amount
        self.params[METADATA] = {}
        self.params[METADATA][OPERATION_REFERENCE] = "QA-test"
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def subtract_transaction_initialize(self, customer_id: int, currency_id: int, subtract_amount: float):
        """
        Build request body for IBalanceService.subtract_transaction_initialize()
        :param customer_id: Customer ID
        :param currency_id: Currency ID
        :param subtract_amount: Amount
        :return: Request body as json dump string.
        """
        self.method += "subtractTransactionInitialize"
        self.params[CUSTOMER_ID] = customer_id
        self.params[CURRENCY_ID] = currency_id
        self.params[AMOUNT] = subtract_amount
        self.params[METADATA] = {}
        self.params[METADATA][OPERATION_REFERENCE] = "QA-test"
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def subtract_transaction_partial_rollback(self, guid, customer_id, currency_id, amount):
        """
        Build request body for IBalanceService.subtract_transaction_partial_rollback()
        :param args: 1- transaction_link, 2- customer_id, 3- currency_id,  4- subtract_amount
        :return: Request body as json dump string.
        """
        #(transaction_link, customer_id, currency_id, subtract_amount) = args
        self.method += "subtractTransactionPartialRollback"
        self.params[TRANSACTION_GUID] = guid
        self.params[CUSTOMER_ID] = customer_id
        self.params[CURRENCY_ID] = currency_id
        self.params[AMOUNT] = amount
        self.params[METADATA] = {}
        self.params[METADATA][OPERATION_REFERENCE] = "QA-test"
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def subtract_transaction_partial_commit(self, *args):
        """
        Build request body for IBalanceService.subtract_transaction_partial_commit()
        :param args: 1- transaction_link, 2- customer_id, 3- currency_id, 4- subtract_amount
        :return: Request body as json dump string.
        """
        (transaction_link, customer_id, currency_id, subtract_amount) = args
        self.method += "subtractTransactionPartialCommit"
        self.params[TRANSACTION_GUID] = transaction_link
        self.params[CUSTOMER_ID] = customer_id
        self.params[CURRENCY_ID] = currency_id
        self.params[AMOUNT] = subtract_amount
        self.params[METADATA] = {}
        self.params[METADATA][OPERATION_REFERENCE] = "QA-test"
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def subtract_transaction_commit(self, transaction_link: str, customer_id: int, currency_id: int):
        """
        Build request body for IBalanceService.subtract_transaction_commit()
        :param transaction_link:
        :param customer_id: Customer ID
        :param currency_id: Currency ID
        :return: Request body as json dump string.
        """
        self.method += "subtractTransactionCommit"
        self.params[TRANSACTION_GUID] = transaction_link
        self.params[CUSTOMER_ID] = customer_id
        self.params[CURRENCY_ID] = currency_id
        self.params[METADATA] = {}
        self.params[METADATA][OPERATION_REFERENCE] = "QA-test"
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def subtract_transaction_rollback(self, transaction_link: str, customer_id: int, currency_id: int):
        """
        Build request body for IBalanceService.subtract_transaction_rollback()
        :param transaction_link:
        :param customer_id: Customer ID
        :param currency_id: Currency ID
        :return: Request body as json dump string.
        """
        self.method += "subtractTransactionRollback"
        self.params[TRANSACTION_GUID] = transaction_link
        self.params[CUSTOMER_ID] = customer_id
        self.params[CURRENCY_ID] = currency_id
        self.params[METADATA] = {}
        self.params[METADATA][OPERATION_REFERENCE] = "QA-test"
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def subtract_transaction_commit_and_rollback_reminder(self, *args):
        """
        Build request body for IBalanceService.subtract_transaction_commit_and_rollback_reminder()
        :param args: 1- transaction_link, 2- customer_id, 3- currency_id, 4- commit_amount
        :return: Request body as json dump string.
        """
        (transaction_link, customer_id, currency_id, commit_amount) = args
        self.method += "subtractTransactionCommitAmountAndRollbackRemainder"
        self.params[TRANSACTION_GUID] = transaction_link
        self.params[CUSTOMER_ID] = customer_id
        self.params[CURRENCY_ID] = currency_id
        self.params[COMMIT_AMOUNT] = commit_amount
        self.params[METADATA] = {}
        self.params[METADATA][OPERATION_REFERENCE] = "QA-test"
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body

    @automation_logger(logger)
    def ensure_in_redis(self, customer_id: int):
        """
        Build request body for IBalanceService.get_all_currencies_balance()
        :param customer_id: ID of a customer.
        :return: Request body as json dump string.
        """
        self.method += "ensureInRedis"
        self.params[CUSTOMER_ID] = customer_id
        body = self.to_json()
        logger.logger.info(REQUEST_BODY.format(body))
        return body
