import time
import unittest
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.order import Order
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer


@pytest.mark.skip(reason="market is not available on WTP")
@allure.severity(allure.severity_level.CRITICAL)
@allure.title("TRADING SANITY TEST 'TS- 7'")
@allure.description("""
    Verify that customer balance unfrozen when market sell order placed.
    """)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_sanity_tests/market_sell_and_balance_unfrozen_test.py",
                 "TestMarketSellUnfrozenAndBalanceUpdated")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
@pytest.mark.functional
@pytest.mark.trading_sanity
class TestMarketSellUnfrozenAndBalanceUpdated(unittest.TestCase):
    test_case = "TS- 7"

    @allure.step("SetUp: calling registered customer and increase him balance.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.currency_id = 8
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), self.currency_id, 10000)
        self.instrument_id = 1022
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_market_buy_unfrozen_and_balance_updated")
    @automation_logger(logger)
    def test_market_buy_unfrozen_and_balance_updated(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(self.test_case))
        logger.logger.info("method test_market_buy_unfrozen_and_balance_updated =['trading_sanity', ]), ")
        result = 0
        try:
            order_quantity = float(Instruments.run_mysql_query(
                "SELECT minOrderQuantity FROM instruments WHERE id=" + str(self.instrument_id) + ";")[0][0])
            frozen_balance_before = \
                self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id,
                                                                           self.currency_id)['result'][
                    'balance']['frozen']
            for i in range(30):
                time_ = time.time() + 250
                order_market_buy = Order().set_order(2, self.instrument_id, order_quantity)
                order_response = self.customer.postman.order_service.create_order(order_market_buy)
                order_status = order_response['result']['status']
                assert order_status is True
                time.sleep(3)
                frozen_balance_after = \
                    self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id,
                                                                               self.currency_id)['result']['balance'][
                        'frozen']
                while float(frozen_balance_before) != float(frozen_balance_after) and time_ > time.time():
                    frozen_balance_after = \
                        self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id,
                                                                                   self.currency_id)['result'][
                            'balance']['frozen']
                assert float(frozen_balance_before) == float(frozen_balance_after)

            logger.logger.info("Test {0}, with CustomerID {1}".format(self.test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, self.test_case, result)
