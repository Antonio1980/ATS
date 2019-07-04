import csv
from src.base import logger
from src.base.utils.utils import Utils
from src.base.utils.k8s import Kubernetes
from config_definitions import BaseConfig
from src.base.utils.mailgun import MailGun
from src.base.utils.testrail import TestRail
from src.base.data_bases.sql_db import SqlDb
from src.base.data_bases.redis_db import RedisDb
from src.base.utils.calculator import Calculator
from src.base.utils.me_ssh import ParamicoConnector
from src.base.log_decorator import automation_logger


class Instruments(RedisDb, SqlDb, TestRail, Calculator, Utils, MailGun, Kubernetes, ParamicoConnector):

    @classmethod
    @automation_logger(logger)
    def get_safe_price(cls, instrument_id):
        """
        Returns a price that can be used to place an order that won't match
        with any other order in Order Book.
        The method checks the price of the most generous "Buy" order
        and the price of the cheapest "Sell" order and returns a price that is halfway between them.

        :param instrument_id:
        :return: special price
        """
        buy_order_book = cls.get_orders_best_price_and_quantity(instrument_id, "sell", 2)
        sell_order_book = cls.get_orders_best_price_and_quantity(instrument_id, "buy", 2)

        if buy_order_book and sell_order_book:
            best_price_sell = sell_order_book[0][0]
            best_price_buy = buy_order_book[0][0]

        elif buy_order_book:
            best_price_buy = buy_order_book[0][0]
            return best_price_buy + 1

        elif sell_order_book:
            best_price_sell = sell_order_book[0][0]
            return best_price_sell - 1

        else:
            logger.logger.error("NO ORDER BOOK")
            return 100.0

        price_tail_digits = Instruments.get_price_tail_digits(instrument_id)
        safe_price = best_price_buy + (best_price_sell - best_price_buy) / 2

        safe_price_rounded = round(safe_price, price_tail_digits)

        return safe_price_rounded

    @staticmethod
    @automation_logger(logger)
    def get_production_prices(instrument_ids):
        """

        :param instrument_ids: The method receives one or several instrument ID's and provides a list of pairs of
        Instrument ID and price taken from Production and stored in CSV file.
        :return:
        """
        with open(BaseConfig.INSTRUMENT_PRICES_PROD) as instruments_file:
            csv_reader = csv.reader(instruments_file)
            instrument_price = [x for x in csv_reader if x[0] != 'id']

            result = [pair for pair in instrument_price if pair[0] in instrument_ids]
            return result

    @staticmethod
    @automation_logger(logger)
    def create_two_customers(flag=None):
        """
        The method is used to create two new customers.
        Customer ID's are assigned to "Customer" objects, customer status is set to "Pending".
        :return: Two pairs of customer object and authorization tokens .
        """
        from src.base.customer.customer import Customer

        boris = Customer()
        auth_response1 = boris.postman.authorization_service.sign_up_step_1(boris)
        assert auth_response1['error'] is None
        boris_token = auth_response1['result']['token']
        boris.customer_id = auth_response1['result']['customerId']

        boris.set_customer_status(2)

        boris_data = boris.postman.get_static_postman(boris_token).trade_service.customer_data()
        assert boris_data['error'] is None
        assert boris_data['result']['customer']['status'] == 2

        if flag: return [(boris, boris_token)]

        if not flag:
            stas = Customer()
            auth_response2 = stas.postman.authorization_service.sign_up_step_1(stas)
            assert auth_response2['error'] is None
            stas_token = auth_response2['result']['token']
            stas.customer_id = auth_response2['result']['customerId']

            stas.set_customer_status(2)

            stas_data = stas.postman.get_static_postman(stas_token).trade_service.customer_data()
            assert stas_data['error'] is None
            assert stas_data['result']['customer']['status'] == 2

            return [(boris, boris_token), (stas, stas_token)]


# if __name__ == "__main__":
#     print([l for l in Instruments.execute_ssh_command("ls -l")])
#     x = Instruments.create_two_customers()
#     pass
