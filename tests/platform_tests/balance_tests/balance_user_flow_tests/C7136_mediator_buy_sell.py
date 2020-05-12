import time
import json
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "7073"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)

cheap_price = 5
expensive_price = 6

quantity_sell = 100

initial_sum_xrp = 100

ORDER_PROCESS_DELAY = 5


@allure.feature("Balance - User Flow")
@allure.story(" Balance is updated after several trades.")
@allure.title(" Two trades with mediator .")
@allure.description("""
    Functional tests.

    1. Adding balance to seller and both buyers.
    2. Jack sells to Eugene 100 XRP.
    3. Eugene sells to Suzie 100 XRP.

       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_user_flow_tests/C7136_mediator_buy_sell.py . ",
                 "Trade with mediator.")
class TestThreeAccounts(object):
    """
    In this test a customer named Jack sells 100 XRP to customer named Eugene for 5 EUR each.
    Since Eugene is interested in making a profit, he sells the 100 XRP that he has bough from Jack
    to another customer named Suzie for 6 EUR each. Eugene is a sort of mediator, that sells what he has bough.

    This test comes to verify balance update to all three accounts after two trades were performed, while
    one of the customers is used as a mediator.


    """

    # Jack
    jack = None

    # Eugene
    eugene = None

    # Suzie
    suzie = None

    sell_order_jack = Order().set_order(2, instrument_id, quantity_sell, cheap_price)

    buy_order_eugene = Order().set_order(1, instrument_id, quantity_sell, cheap_price)

    sell_order_eugene = Order().set_order(2, instrument_id, quantity_sell, expensive_price)

    buy_order_suzie = Order().set_order(1, instrument_id, quantity_sell, expensive_price)

    @pytest.mark.parametrize('make_two_customers', [[instrument_id]], indirect=True)
    @allure.step("Adding balance to seller and both buyers.")
    @automation_logger(logger)
    def test_add_balance(self, make_two_customers, r_customer_sql):
        # Jack
        TestThreeAccounts.jack = r_customer_sql

        # Eugene
        TestThreeAccounts.eugene = make_two_customers[0]

        # Suzie
        TestThreeAccounts.suzie = make_two_customers[1]

        # Adding balance - Jack
        response = TestThreeAccounts.jack.postman.balance_service.add_balance(
            TestThreeAccounts.jack.customer_id, base_currency, initial_sum_xrp)
        assert response

        # Adding balance - Eugene
        response = TestThreeAccounts.eugene.postman.get_static_postman(
            TestThreeAccounts.eugene.static_token). \
            balance_service.add_balance(TestThreeAccounts.eugene.customer_id, quoted_currency,
                                        quantity_sell * cheap_price)
        assert response

        # Adding balance - Suzie
        response = TestThreeAccounts.suzie.postman.get_static_postman(
            TestThreeAccounts.suzie.static_token). \
            balance_service.add_balance(TestThreeAccounts.suzie.customer_id, quoted_currency,
                                        quantity_sell * expensive_price)
        assert response

    @allure.step("Jack sells to Eugene 100 XRP.")
    @automation_logger(logger)
    def test_jack_sell_eugene(self):
        # Placing the "Sell" order - Jack
        order_response = TestThreeAccounts.jack.postman.get_static_postman(TestThreeAccounts.jack.auth_token) \
            .order_service.create_order_sync(TestThreeAccounts.sell_order_jack)

        assert order_response['error'] is None

        # Placing the "Buy" order - Eugene
        order_response = TestThreeAccounts.eugene.postman.get_static_postman(
            TestThreeAccounts.eugene.static_token).order_service.create_order_sync(TestThreeAccounts.buy_order_eugene)

        assert order_response['error'] is None
        time.sleep(ORDER_PROCESS_DELAY)

        # Verifying that Eugene has bough the 100 XRP from Jack.
        eugene_xrp_balance = TestThreeAccounts.eugene.postman.get_static_postman(
            TestThreeAccounts.eugene.static_token) \
            .balance_service.get_all_currencies_balance(TestThreeAccounts.eugene.customer_id)

        assert float(eugene_xrp_balance['result'][base_currency - 1]['balance']['available']) == quantity_sell

        logger.logger.info(
            f"Eugene's balance in XRP after the trade:"
            f" {eugene_xrp_balance['result'][base_currency - 1]['balance']['available']}")

    @allure.step("Eugene sells to Suzie 100 XRP.")
    @automation_logger(logger)
    def test_eugene_sell_suzie(self):
        # Placing the "Sell" order - Eugene
        order_response = TestThreeAccounts.eugene.postman.get_static_postman(
            TestThreeAccounts.eugene.static_token).order_service.create_order_sync(TestThreeAccounts.sell_order_eugene)

        assert order_response['error'] is None

        # Placing the "Buy" order - Suzie
        order_response = TestThreeAccounts.suzie.postman.get_static_postman(
            TestThreeAccounts.suzie.static_token).order_service.create_order_sync(TestThreeAccounts.buy_order_suzie)

        assert order_response['error'] is None
        time.sleep(ORDER_PROCESS_DELAY)

        # Verifying that Eugene got 600 EUR from Suzie
        eugene_eur_balance = TestThreeAccounts.eugene.postman.get_static_postman(
            TestThreeAccounts.eugene.static_token) \
            .balance_service.get_all_currencies_balance(TestThreeAccounts.eugene.customer_id)

        assert float(eugene_eur_balance['result'][quoted_currency - 1]['balance']['available']) == \
               quantity_sell * expensive_price

        # Verifying that Suzie  bough 100 XRP from Eugene
        suzie_xrp_balance = TestThreeAccounts.eugene.postman.get_static_postman(
            TestThreeAccounts.suzie.static_token) \
            .balance_service.get_all_currencies_balance(TestThreeAccounts.suzie.customer_id)

        assert float(suzie_xrp_balance['result'][base_currency - 1]['balance']['available']) == \
               quantity_sell

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
