import json
import time
import requests
from datetime import date
from src.base import logger
from src.base.log_decorator import automation_logger
from src.base.services.service_route import ServiceRoute
from src.base.services.svc_requests.order_requests import OrderServiceRequest


class OrderService(ServiceRoute):
    def __init__(self, auth_token=None):
        super(OrderService, self).__init__()
        self.headers.update({'Authorization': auth_token})

    @automation_logger(logger)
    def create_order(self, order) -> json:
        """
        Sends HTTP POST request to OrderService to create Market or Limit order.
        :param order: Order object.
        :return: Response body as a json.
        """
        payload = OrderServiceRequest().create_order(order)
        try:
            _response = requests.post(
                self.api_url, data=payload, headers=self.headers, stream=True, verify=False, timeout=10)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            order.date_created = str(date.today()) + " - " + str(time.perf_counter())
            result = body['result']
            if result:
                if 'externalOrderId' in result.keys():
                    order.external_id = result['externalOrderId']
                logger.logger.info(F"{order.type}, {order.external_id}, {order.direction}, {order.date_created}")
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} create_order failed with error: {e}")
            raise e

    @automation_logger(logger)
    def create_order_sync(self, order) -> json:
        """
        Sends HTTP POST Synchronously request to OrderService to create Market or Limit order.
        :param order: Order object.
        :return: Response body as a json.
        """
        payload = OrderServiceRequest().create_order_sync(order)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            order.date_created = str(date.today()) + " - " + str(time.perf_counter())
            result = body['result']
            if result:
                if 'externalOrderId' in result.keys():
                    order.external_id = result['externalOrderId']
                if 'orderId' in result.keys():
                    order.internal_id = result['orderId']
                logger.logger.info(
                    "{0}, {1}, {2}, {3}, {4}".format(order.type, order.external_id, order.internal_id, order.direction,
                                                     order.date_created))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} create_order_sync failed with error: {e}")
            raise e

    @automation_logger(logger)
    def cancel_order(self, order_id) -> json:
        """
        Sends HTTP POST request to OrderService to cancel order by ID.
        :param order_id: If String it will be sent as External ID , in case of Integer will be used internal ID.
        :return: Response body as a json.
        """
        payload = OrderServiceRequest().cancel_order(order_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} cancel_order failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_order_history(self, direction=None, product_id=None, instrument_id=None, *args) -> json:
        """
        Sends HTTP POST request to OrderService to receive all created orders.
        :param direction: Sell/Buy as string.
        :param product_id: Product ID- int.
        :param instrument_id: 
        :return: Response body as a json.
        """
        payload = OrderServiceRequest().order_history(direction, product_id, instrument_id, args)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_order_history failed with error: {e}")
            raise e

    @automation_logger(logger)
    def export_order_history(self, direction, product_id=None, instrument_id=None) -> json:
        """
        Sends HTTP POST request to OrderService to receive all created orders.
        :param direction: Sell/Buy as string.
        :param product_id: Product ID- int.
        :param instrument_id: Instrument ID- int.
        :return: Response body as a json.
        """
        payload = OrderServiceRequest().export_order_history(direction, product_id, instrument_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} export_order_history failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_trades_history(self, direction=None, product_id=None, instrument_id=None, *args) -> json:
        """
        Sends HTTP POST request to OrderService to receive all created trades.
        :param direction: Sell/Buy as string.
        :param product_id: Product ID- int.
        :param instrument_id: Instrument ID- int.
        :return: Response body as a json.
        """
        payload = OrderServiceRequest().trades_history(direction, product_id, instrument_id, args)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_trades_history failed with error: {e}")
            raise e

    @automation_logger(logger)
    def export_trades_history(self, direction, product_id=None, instrument_id=None) -> json:
        """
        Sends HTTP POST request to OrderService to receive all created trades.
        :param direction: Sell or Buy as a string.
        :param product_id: Product ID- int.
        :param instrument_id: Instrument ID- int.
        :return: Response body as a json.
        """
        payload = OrderServiceRequest().export_trade_history(direction, product_id, instrument_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} export_trades_history failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_open_orders(self, product_id=None) -> json:
        """
        Sends HTTP POST request to OrderService to receive all opened orders.
        :param product_id: Product ID- int.
        :return: Response body as a json.
        """
        payload = OrderServiceRequest().open_orders(product_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_open_orders failed with error: {e}")
            raise e

    @automation_logger(logger)
    def export_open_orders(self, product_id=None) -> json:
        """
        Sends HTTP POST request to OrderService to receive all created trades.
        :param product_id: Product ID- int.
        :return: Response body as a json.
        """
        payload = OrderServiceRequest().export_open_orders(product_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} export_open_orders failed with error: {e}")
            raise e

    @automation_logger(logger)
    def get_order_book(self, instrument_id=None) -> json:
        """
        Sends HTTP POST request to OrderService to receive all created trades.
        :param instrument_id: Instrument ID- int.
        :return: Response body as a json.
        """
        payload = OrderServiceRequest().get_order_book(instrument_id)
        try:
            _response = requests.post(self.api_url, data=payload, headers=self.headers)
            body = json.loads(_response.text)
            logger.logger.info("Service Response: {0}".format(body))
            return body
        except Exception as e:
            logger.logger.exception(F"{e.__class__.__name__} get_order_book failed with error: {e}")
            raise e
