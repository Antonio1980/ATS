import json
import requests
from src.base import logger
from config_definitions import BaseConfig
from src.base import coins_marketplace_url
from src.base.log_decorator import automation_logger


class CoinsMarketplace:
    coins_proxy = "/api/vault/accounts"
    coins_marketplace_url = coins_marketplace_url + coins_proxy
    coins_headers = {'Content-Type': 'application/json'}
    coins_headers.update({'Authorization': 'Bearer ' + BaseConfig.BAR_TOKEN})

    @automation_logger(logger)
    def get_cmp_account(self, customer_id: int):
        """
        Sends HTTP POST request to CoinsMarketPlace to return internal (cmp) customer id.
        :param customer_id: Customer ID.
        :return: Response body as json.
        """
        _url = self.coins_marketplace_url + '''?query={"name": "%s"}''' % str(customer_id)
        try:
            _response = requests.get(_url, headers=self.coins_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_cmp_account failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_customer_cmp_balance(self, customer_id: int) -> json:
        """
        Sends HTTP POST request to CoinsMarketPlace to return customer balance.
        :param customer_id: Customer ID.
        :return: Response body as json.
        """
        account_response = self.get_cmp_account(customer_id)
        assert account_response[0]['_id']
        assert account_response[0]['name'] == str(customer_id)
        _id = account_response[0]['_id']
        _url = self.coins_marketplace_url + "/{0}/balances".format(_id)
        try:
            _response = requests.get(_url, headers=self.coins_headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_customer_cmp_balance failed with error: {e}")
            raise e
