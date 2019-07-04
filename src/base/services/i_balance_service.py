import json
import requests
from src.base import logger, balance_svc_url
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.i_balance_requests import IBalanceServiceRequest


class IBalanceService:
    balance_svc_url = balance_svc_url
    balance_svc_headers = {'Content-Type': 'application/json'}

    @automation_logger(logger)
    def get_currency_balance(self, customer_id: int, currency_id: int) -> json:
        """
        Sends HTTP POST request to IBalanceServiceRequest to get balance for provided currency.
        :param customer_id: Customer ID as an int.
        :param currency_id: Currency ID as an int.
        :return: Response body as a json.
        """
        payload = IBalanceServiceRequest().get(customer_id, currency_id)
        try:
            _response = requests.post(self.balance_svc_url, data=payload, headers=self.balance_svc_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_currency_balance failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_all_currencies_balance(self, customer_id: int) -> json:
        """
        Sends HTTP POST request to IBalanceServiceRequest to get balance for all currencies.
        :param customer_id: Customer ID as an int.
        :return: Response body as a json.
        """
        payload = IBalanceServiceRequest().get_all(customer_id)
        try:
            _response = requests.post(self.balance_svc_url, data=payload, headers=self.balance_svc_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_all_currencies_balance failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_subtract_transactions(self, customer_id: int, currency_id: int) -> json:
        """
        Sends HTTP POST request to IBalanceServiceRequest to.
        :param customer_id: Customer ID as an int.
        :param currency_id: ID of currenct - int.
        :return: Response body as a json.
        """
        payload = IBalanceServiceRequest().get_subtract_transactions(customer_id, currency_id)
        try:
            _response = requests.post(self.balance_svc_url, data=payload, headers=self.balance_svc_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_subtract_transactions failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_balance(self, customer_id: int, currency_id: int, deposit_amount: float) -> json:
        """
        Sends HTTP POST request to IBalanceServiceRequest to add some balance for provided customer.
        :param customer_id: Customer ID as an int.
        :param currency_id: Currency ID as an int.
        :param deposit_amount: Amount as an float.
        :return: Response body as a json.
        """
        payload = IBalanceServiceRequest().add(customer_id, currency_id, deposit_amount)
        try:
            _response = requests.post(self.balance_svc_url, data=payload, headers=self.balance_svc_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} add_balance failed with error: {e}")
            raise e
    
    @automation_logger(logger)
    def subtract_balance(self, customer_id: int, currency_id: int, subtract_amount: float) -> json:
        """
        Sends HTTP POST request to IBalanceServiceRequest to subtract some balance for provided customer.
        :param customer_id: Customer ID as an int.
        :param currency_id: Currency ID as an int.
        :param subtract_amount: Amount as an float.
        :return: Response body as a json.
        """
        payload = IBalanceServiceRequest().subtract(customer_id, currency_id, subtract_amount)
        try:
            _response = requests.post(self.balance_svc_url, data=payload, headers=self.balance_svc_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} subtract_balance failed with error: {e}")
            raise e

    @automation_logger(logger)
    def subtract_transaction_initialize(self, customer_id: int, currency_id: int, subtract_amount: float) -> json:
        """
        Sends HTTP POST request to IBalanceServiceRequest to subtract transaction for provided customer.
        :param customer_id: Customer ID as an int.
        :param currency_id: Currency ID as an int.
        :param subtract_amount: Amount as an float.
        :return: Response body as a json.
        """
        payload = IBalanceServiceRequest().subtract_transaction_initialize(customer_id, currency_id, subtract_amount)
        try:
            _response = requests.post(self.balance_svc_url, data=payload, headers=self.balance_svc_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} subtract_transaction_initialize failed with error: {e}")
            raise e

    @automation_logger(logger)
    def subtract_transaction_partial_rollback(self, guid, customer_id, currency_id, amount) -> json:
        """
        Sends HTTP POST request to IBalanceServiceRequest to rollback partial subtract transaction for provided customer.
        :param args: transaction_link- str, customer_id- int, currency_id- int, subtract_amount- float
        :return: Response body as a json.
        """
        payload = IBalanceServiceRequest().subtract_transaction_partial_rollback(guid, customer_id, currency_id, amount)
        try:
            _response = requests.post(self.balance_svc_url, data=payload, headers=self.balance_svc_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} subtract_transaction_partial_rollback failed with error: {e}")
            raise e

    @automation_logger(logger)
    def subtract_transaction_partial_commit(self, *args) -> json:
        """
        Sends HTTP POST request to IBalanceServiceRequest to partial subtract transaction for provided customer.
        :param args: transaction_link- str, customer_id- int, currency_id- int, subtract_amount- float
        :return: Response body as a json.
        """
        payload = IBalanceServiceRequest().subtract_transaction_partial_commit(*args)
        try:
            _response = requests.post(self.balance_svc_url, data=payload, headers=self.balance_svc_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.error(F"{e.__class__.__name__} subtract_transaction_partial_commit failed with error: {e}")
            raise e

    @automation_logger(logger)
    def subtract_transaction_commit(self, transaction_link, customer_id, currency_id) -> json:
        """
        Sends HTTP POST request to IBalanceServiceRequest to  subtract transaction for provided customer.
        :param transaction_link: GUID
        :param customer_id: Customer ID as an int.
        :param currency_id: Currency ID as an int.
        :return: Response body as a json.
        """
        payload = IBalanceServiceRequest().subtract_transaction_commit(transaction_link, customer_id, currency_id)
        try:
            _response = requests.post(self.balance_svc_url, data=payload, headers=self.balance_svc_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} subtract_transaction_commit failed with error: {e}")
            raise e

    @automation_logger(logger)
    def subtract_transaction_rollback(self, transaction_link, customer_id, currency_id) -> json:
        """
        Sends HTTP POST request to IBalanceServiceRequest to rollback subtract transaction for provided customer.
        :param transaction_link: GUID
        :param customer_id: Customer ID as an int.
        :param currency_id: Currency ID as an int.
        :return: Response body as a json.
        """
        payload = IBalanceServiceRequest().subtract_transaction_rollback(transaction_link, customer_id, currency_id)
        try:
            _response = requests.post(self.balance_svc_url, data=payload, headers=self.balance_svc_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} subtract_transaction_rollback failed with error: {e}")
            raise e

    @automation_logger(logger)
    def subtract_transaction_commit_and_rollback_reminder(self, *args) -> json:
        """
        Sends HTTP POST request to IBalanceServiceRequest to subtract transaction....
        :param args: transaction_link- str, customer_id- int, currency_id- int, commit_amount- float
        :return: Response body as a json.
        """
        payload = IBalanceServiceRequest().subtract_transaction_commit_and_rollback_reminder(*args)
        try:
            _response = requests.post(self.balance_svc_url, data=payload, headers=self.balance_svc_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} subtract_transaction_commit_and_rollback_reminder failed with error: {e}")
            raise e

    @automation_logger(logger)
    def ensure_in_redis(self, customer_id) -> json:
        """
        Sends HTTP POST request to IBalanceServiceRequest to republish current customer balance into Redis.
        :param customer_id: Customer ID as an int.
        :return: Response body as a json.
        """
        payload = IBalanceServiceRequest().ensure_in_redis(customer_id)
        try:
            _response = requests.post(self.balance_svc_url, data=payload, headers=self.balance_svc_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} ensure_in_redis failed with error: {e}")
            raise e
