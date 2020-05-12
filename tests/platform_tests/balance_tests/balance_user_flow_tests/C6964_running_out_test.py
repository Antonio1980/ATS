import json
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "6964"


# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)

price_for_sell = 5
quantity_sell = 80.00

initial_sum = 180


@allure.feature("Balance testing - user flow.")
@allure.story("Balance is updated according to performed actions.")
@allure.title("Failed to place the third order - not enough availabla balance left.")
@allure.description("""

    Functional tests.
    1. Add funds to customer's balance.
    2. Place two valid orders.
    3. Trying to place the third order - failure expected.
    
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_user_flow_tests/C6964_running_out_test.py",
                 "Running_Out_Of_available_balance")
@pytest.mark.usefixtures("r_customer")
class TestRunningOut(object):
    """
    In this test customer places two orders and tries to place a third order, but doesn't have enough.
    available balance. This test comes to verify that the third order isn't placed and customer's balance
    in "base" currency isn't modified after the failed attempt to place the third order.
    """

    sell_order = Order().set_order(2, instrument_id, quantity_sell, price_for_sell)

    @allure.step("Add funds to customer's balance.")
    @automation_logger(logger)
    def test_add_save_balance(self, r_customer_sql):
        r_customer_sql.postman.balance_service.add_balance(r_customer_sql.customer_id, base_currency, initial_sum)

        response = r_customer_sql.postman.balance_service.\
            get_currency_balance(r_customer_sql.customer_id, base_currency)

        assert float(response['result']['balance']['available']) == initial_sum

        logger.logger.info(
            F"Customer's balance available before orders are placed - response: "
            F"{response['result']['balance']['available']}")
        print(
            F"Customer's  available balance before orders are placed - response: "
            F"{response['result']['balance']['available']}")

    @allure.step("Place two valid orders")
    @automation_logger(logger)
    def test_place_two_valid_orders(self, r_customer_sql):

        order_response = r_customer_sql.postman.order_service.create_order(TestRunningOut.sell_order)
        assert order_response['error'] is None

        order_response = r_customer_sql.postman.order_service.create_order(TestRunningOut.sell_order)
        assert order_response['error'] is None

        response = r_customer_sql.postman.balance_service.\
            get_currency_balance(r_customer_sql.customer_id, base_currency)

        assert float(response['result']['balance']['available']) == initial_sum - quantity_sell * 2

    @allure.step("Trying to place the third order - failure expected.")
    @automation_logger(logger)
    def test_order_placement_fails(self, r_customer_sql):

        order_response = r_customer_sql.postman.order_service.create_order(TestRunningOut.sell_order)
        error_report = json.loads(order_response['error'])
        assert error_report['details'] == 'error freezing balance'

        logger.logger.info(f"Order service response: {order_response}")
        print(f"Order service response: {order_response}")

        balance_response = r_customer_sql.postman.balance_service.\
            get_currency_balance(r_customer_sql.customer_id, base_currency)

        assert float(balance_response['result']['balance']['available']) == initial_sum - quantity_sell * 2

        sell_orders_in_db = Order.\
            orders_data_converter(Instruments.get_orders_by_customer_mysql(r_customer_sql.customer_id, 1, 3))

        logger.logger.info("Orders in DB: {sell_orders_in_db}")
        print(f"Orders in DB: {sell_orders_in_db}")
        assert len(sell_orders_in_db) == 2

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
