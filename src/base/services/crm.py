import json

import requests

from config_definitions import BaseConfig
from src.base import logger, crm_base_url
from src.base.log_decorator import automation_logger
from src.base.services.svc_requests.crm_requests import CrmRequest


class Crm:
    crm_proxy = "/dx"
    crm_url = crm_base_url + crm_proxy
    crm_reference_url = crm_url + "/customers/page/"
    crm_ref_url = crm_url + "/customers/page/"
    crm_headers = {'Content-Type': 'application/x-www-form-urlencoded', 'Origin': crm_base_url,
                   'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                                 'Chrome/71.0.3578.80 Safari/537.36', 'DisablePermissionsCache': '1'}

    @automation_logger(logger)
    def log_in_to_crm(self, username=BaseConfig.CRM_USERNAME, password=BaseConfig.CRM_PASSWORD):
        """
        Sends HTTP POST request to log in to CRM and stores session.
        :param username: User credentials.
        :param password: User credentials.
        :return: Response body as a String (contains HTML page).
        """
        url = self.crm_url + "/login"
        payload = CrmRequest().log_in(username, password)
        try:
            _response = requests.post(url, data=payload, headers=self.crm_headers, allow_redirects=True)
            assert _response.ok is True and _response.status_code == 200
            logger.logger.info("Log In to CRM successful.")
            crm_session = _response.request.headers['Cookie'].split(';')[1].strip()
            self.crm_headers.update({'Cookie': crm_session})
            return True
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} log_in_to_crm failed with error: {e}")
            raise e

    @automation_logger(logger)
    def approve_customer(self, customers) -> str:
        """
        Log In to CRM and next HTTP POST request to approve customer by provided ID.
        :param customers: Customer ID as a int.
        :return: Response body as a String (contains text message).
        """
        assert self.log_in_to_crm()

        if not isinstance(customers, list):
            customers = [customers, ]
        try:
            body = None
            for customer_id in customers:
                self.crm_headers.update({'Referer': self.crm_reference_url + str(customer_id)})
                url = self.crm_url + "/customers/page/setKyc/" + str(
                    customer_id) + "?reg=3&risk=Normal&action=3&sendEmail=True"
                _response = requests.get(url, headers=self.crm_headers, allow_redirects=True)
                if "DOCTYPE" in _response.text:
                    body = _response.text
                else:
                    body = json.loads(_response.text)
                    assert "successful" in body['message']
                logger.logger.info("Service Response: {0}".format(body))
                logger.logger.info("Customer {0} successfully approved.".format(customer_id))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} approve_customer failed with error: {e}")
            raise e

    @automation_logger(logger)
    def update_customer_deposit(self, customer_id: int, customer: object, *args) -> str:
        """
        Sends HTTP POST request to update deposit status to "2"- approved.
        :param customer_id: Customer ID as a int.
        :param customer: Customer object.
        :param args: 1- deposit_id, 2- payment_method_id, 3- currency_name, 4- currency_id, 5- deposit_amount
        :return: Response body as a String (contains text message).
        """
        self.crm_headers.update({'Referer': self.crm_reference_url + str(customer_id)})
        url = self.crm_url + "/customers/page/updateCustomerDeposit/" + str(customer_id)
        payload = CrmRequest().approve_customer_deposit(customer_id, customer, args)
        try:
            _response = requests.post(url, data=payload, headers=self.crm_headers, allow_redirects=True)
            logger.logger.info("Service Response: {0}".format(_response.text))
            crm_session = _response.request.headers['Cookie'].strip()
            self.crm_headers.update({'Cookie': crm_session})
            return _response.text
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} update_customer_deposit failed with error: {e}")
            raise e

    @automation_logger(logger)
    def add_new_deposit(self, customer_id: int, customer: object, *args) -> json:
        """
        Sends HTTP POST request to add new deposit for provided customer.
        :param customer_id: Customer ID as a int.
        :param customer: Customer object.
        :param args: 1- payment_method_id, 2- currency_name, 3- currency_id, 4- deposit_amount
        :return: Response body as a String (contains text message).
        """
        self.crm_headers.update({'Referer': self.crm_reference_url + str(customer_id)})
        url = self.crm_url + "/customers/page/addNewDeposit/" + str(customer_id)
        payload = CrmRequest().add_new_deposit(customer, args)
        try:
            _response = requests.post(url, data=payload, headers=self.crm_headers, allow_redirects=True)
            crm_session = _response.request.headers['Cookie'].strip()
            self.crm_headers.update({'Cookie': crm_session})
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} add_new_deposit failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_deposit_by_id(self, customer_id: int, deposit_id: float) -> str:
        """
        Sends HTTP GET request to CRM that selects customer deposit.
        :param customer_id: Customer ID as a int.
        :param deposit_id: Deposit ID as a int.
        :return: Response body as a String (contains text message).
        """
        self.crm_headers.update({'Referer': self.crm_reference_url + str(customer_id)})
        url = self.crm_url + "/customers/page/getDepositById/" + str(deposit_id)
        payload = CrmRequest().get_deposit_by_id(customer_id)
        try:
            _response = requests.post(url, data=payload, headers=self.crm_headers, allow_redirects=True)
            logger.logger.info("Service Response: {0}".format(_response.text))
            crm_session = _response.request.headers['Cookie'].strip()
            self.crm_headers.update({'Cookie': crm_session})
            return _response.text
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_deposit_by_id failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_customer_deposits(self, customer_id: int) -> str:
        """
        Sends HTTP GET request to CRM that selects all customer deposit.
        :param customer_id: Customer ID as a String.
        :return: Response body as a json.
        """
        payload = CrmRequest().get_customer_deposits()
        self.crm_headers.update({'Referer': self.crm_reference_url + str(customer_id)})
        url = self.crm_url + "/customers/page/getCustomerDeposits/" + str(customer_id) + "?s" + payload
        try:
            _response = requests.get(url, headers=self.crm_headers, allow_redirects=True)
            crm_session = _response.request.headers['Cookie'].strip()
            self.crm_headers.update({'Cookie': crm_session})
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_customer_deposits failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_customer_withdrawals(self, customer_id: int) -> json:
        """
        Sends HTTP GET request to CRM that selects all customer withdrawals.
        :param customer_id: Customer ID as a int.
        :return: Response body as a json.
        """
        payload = CrmRequest().get_customer_withdrawals()
        self.crm_headers.update({'Referer': self.crm_reference_url + str(customer_id)})
        url = self.crm_url + "/customers/page/getCustomerWithdrawals/" + str(customer_id) + "?s" + payload
        try:
            _response = requests.get(url, headers=self.crm_headers, allow_redirects=True)
            crm_session = _response.request.headers['Cookie'].strip()
            self.crm_headers.update({'Cookie': crm_session})
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_customer_withdrawals failed with error: {e}")
            raise e

    @automation_logger(logger)
    def update_customer_details(self, customer_id: int, customer: object, phone: str) -> str:
        """
        Sends HTTP GET request to CRM that selects all customer deposit.
        :param customer_id: Customer ID as a int.
        :param customer: Customer object.
        :param phone: Phone number to update as a str without '+' and 13 chars length
        return: Response body as a json.
        """
        payload = CrmRequest().save_customer_information(customer, phone)
        self.crm_headers.update({'Referer': self.crm_reference_url + str(customer_id)})
        url = self.crm_url + "/customers/page/saveCustomerInformation/" + str(customer_id)
        try:
            _response = requests.post(url, data=payload, headers=self.crm_headers, allow_redirects=True)
            crm_session = _response.request.headers['Cookie'].strip()
            self.crm_headers.update({'Cookie': crm_session})
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} update_customer_details failed with error: {e}")
            raise e

    @automation_logger(logger)
    def save_permissions(self):

        assert self.log_in_to_crm()

        querystring = CrmRequest().save_permissions()

        url = self.crm_url + "/permissions/getTable?"
        self.crm_headers.update({'Referer': self.crm_url + "/permissions/"})

        try:
            _response = requests.request("GET", url, headers=self.crm_headers, params=querystring, allow_redirects=True)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} save_permissions failed with error: {e}")
            raise e

    @automation_logger(logger)
    def update_customer_withdrawal(self, customer_id: int, *args, status_id='1') -> str:
        """
        Sends HTTP POST request to update withdrawal status to "2"- approved.
        :param customer_id: Customer ID as a String.
        :param args: 1- withdrawal_id,
                     2- payment_method_id :'2' - for Sepa Withdrawal, '4' - for Wire Withdrawal,
                     3- currency_name,
                     4- currency_id,
                     5- withdrawal_amount
        :param status_id: 1- pending system, 2- approved, 3- declined, 4- cancelled, 5- pending customer.
        :return: Response body as a String (contains text message).
        """
        self.log_in_to_crm()
        self.crm_headers.update({'Referer': self.crm_reference_url + str(customer_id)})
        url = self.crm_url + "/customers/page/updateCustomerWithdrawal/" + str(customer_id)
        payload = CrmRequest().approve_customer_withdrawal(customer_id, status_id, args)
        try:
            _response = requests.post(url, data=payload, headers=self.crm_headers, allow_redirects=True)
            logger.logger.info("Service Response: {0}".format(_response.text))
            crm_session = _response.request.headers['Cookie'].strip()
            self.crm_headers.update({'Cookie': crm_session})
            return _response.text
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} update_customer_withdrawal failed with error: {e}")
            raise e


# if __name__ == '__main__':
#     Crm().update_customer_withdrawal(100001100000023403, 2068, 4, 'USD', 1, 100)
#     pass
