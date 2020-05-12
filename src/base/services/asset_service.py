import json
import requests
from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.service_route import ServiceRoute
from src.base.services.svc_requests.asset_requests import AssetServiceRequest


class AssetService(ServiceRoute):
    def __init__(self, auth_token=None):
        super(AssetService, self).__init__()
        self.headers.update({'Authorization': auth_token})

    @automation_logger(logger)
    def get_history(self, instrument_id: int = None, type_: str = None) -> json:
        """
        Sends HTTP POST request to AssetService to return all records for provided instrument and given time gap.
        :param instrument_id: ID of instrument- int, not mandatory (without- for all instruments)..
        :param type_: String ("1m", "5m", "1h", "1d")- Tenor (good till date option).
        :return: Service response body as json.
        """
        payload = AssetServiceRequest().history(instrument_id, type_)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_history failed with error: {e}")
            raise e

    @automation_logger(logger)
    def set_favorite_instrument(self, instrument_id: int) -> json:
        """
        Sends HTTP POST request to AssetService to set record for provided instrument.
        :param instrument_id: ID of instrument- int
        :return: Service response body as json.
        """
        payload = AssetServiceRequest().set_favorite_instrument(instrument_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} set_favorite_instrument failed with error: {e}")
            raise e

    @automation_logger(logger)
    def remove_favorite_instrument(self, instrument_id: int) -> json:
        """
        Sends HTTP POST request to AssetService to delete record for provided instrument.
        :param instrument_id: ID of instrument- int
        :return: Service response body as json.
        """
        payload = AssetServiceRequest().remove_favorite_instrument(instrument_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} remove_favorite_instrument failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_instruments(self, symbol: str = None, product_id: int = None) -> json:
        """
        Sends HTTP POST request to AssetService to return all tradeable instruments.
        :param symbol: String as "BTC/EUR, not mandatory.
        :param product_id: ID of product- int, not mandatory.
        If optional parameters not provided will be choosen for all available.
        :return: Service response body as json.
        """
        payload = AssetServiceRequest().get_instruments(symbol, product_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_instruments failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_ticker(self, instrument_id: int, currency_id: int) -> json:
        """
        Sends HTTP POST request to AssetService to return ticker for instrument and currency.
        :param instrument_id: ID of an instrument- int.
        :param currency_id: ID of a currency- int.
        :return: Service response body as json.
        """
        payload = AssetServiceRequest().get_ticker(instrument_id, currency_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_ticker failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_last_trades(self, instrument_id: int) -> json:
        """
        Sends HTTP POST request to AssetService to return last trade info for instrument.
        :param instrument_id: ID of an instrument- int.
        :return: Service response body as json.
        """
        payload = AssetServiceRequest().get_last_trades(instrument_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_last_trades failed with error: {e}")
            raise e
