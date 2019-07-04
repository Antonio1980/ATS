import time
import allure
import pytest
import unittest
from src.base import logger
from src.base.customer.customer import Customer
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger


@pytest.mark.skip(reason="market is not available on WTP")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TRADING SANITY TEST TS- 5")
@allure.description("""
    Verify that customer balance (base/quoted) updated after trade.
    """)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_sanity_tests/market_buy_balance_is_updated_test.py",
                 "TestMarketBuyUnfrozenAndBalanceUpdated")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
@pytest.mark.functional
@pytest.mark.trading_sanity
class TestMarketBuyUnfrozenAndBalanceUpdated(unittest.TestCase):
    test_case = "TS- 5"

    @allure.step("SetUp: calling registered customer and adding USD to balance.")
    def setUp(self):
        self.customer = Customer()
        self.customer.customer_registration()
        self.currency_id = 1
        self.customer.postman.balance_service.add_balance(self.customer.customer_id, 1, 10000.0)
        self.instrument_id = 1022
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_market_buy_unfrozen_and_balance_updated")
    @automation_logger(logger)
    def test_market_buy_unfrozen_and_balance_updated(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(self.test_case))
        logger.logger.info("method test_market_buy_unfrozen_and_balance_updated ")
        result = 0
        try:
            order_quantity = float(Instruments.run_mysql_query(
                "SELECT minOrderQuantity FROM instruments WHERE id=" + str(self.instrument_id) + ";")[0][0])

            balance_quoted_before = self.customer.postman.balance_service.get_currency_balance(
                self.customer.customer_id, 1)
            frozen_balance_before = balance_quoted_before['result']['balance']['frozen']
            available_quoted_before = balance_quoted_before['result']['balance']['available']
            total_quoted_before = balance_quoted_before['result']['balance']['total']

            order_market_buy = Order().set_order(1, self.instrument_id, order_quantity)
            order_response = self.customer.postman.order_service.create_order_sync(order_market_buy)
            order_id = order_response['result']['orderId']
            time.sleep(2)

            price_for_order = Instruments.run_mysql_query(
                "SELECT price*quantity FROM trades_crypto WHERE trades_crypto.orderId=" + str(order_id) + ";")[0][0]

            quantity_base_currency = (Instruments.run_mysql_query(
                "SELECT SUM(quantity) FROM trades_crypto WHERE trades_crypto.orderId=" + str(order_id) + ";"))

            balance_after = self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 1)

            frozen_balance_after = balance_after['result']['balance']['frozen']
            time_ = time.time() + 200
            while frozen_balance_after != frozen_balance_before and time_ > time.time():
                frozen_balance_after = \
                    self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, 1)['result'][
                        'balance']['frozen']
            assert frozen_balance_after == frozen_balance_before

            available_quoted_after = balance_after['result']['balance']['available']
            total_base_after = balance_after['result']['balance']['total']

            assert available_quoted_after == available_quoted_before - float(price_for_order)
            assert total_quoted_before + quantity_base_currency == total_base_after

            logger.logger.info("Test {0}, with CustomerID {1}".format(self.test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, self.test_case, result)
