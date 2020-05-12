import allure
import time
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "7711"

# The parameters below are used for test configuration
instrument_id = 1025  # DXCASH/ETH
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)

price_for_sell = 0.02
price_for_buy = 0.02263779

quantity_sell = 15.99
quantity_buy = 15.99

initial_sum = 10000

TRADE_PROCESSING_DELAY = 6


@allure.feature("Balance - User Flow")
@allure.story("Balance is unfrozen after a trade, no rounding issues.")
@allure.title("Balance is unfrozen after a trade, no rounding issues.")
@allure.description("""
    Functional tests.
    1. Place the Buy order.
    2. Place the Sell order with smaller price.
    3. Verify Sell order is filled.
    4. Verify no balance remains frozen.

       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_user_flow_tests/C7711_frozen_balance_rounding_test.py",
                 "No rounding issues that lead to frozen balance .")
class TestTradePriceSmaller(object):
    """
    This test case comes to verify that there are no rounding issues with balance unfreeze.
    A real case from Production is taken including instrument, currencies, prices and quantities.
    The flow reproduced in this script led to frozen balance because incorrect balance unfreeze.

    """

    order_sell = Order().set_order(2, instrument_id, quantity_sell, price_for_sell)
    order_buy = Order().set_order(1, instrument_id, quantity_sell, price_for_buy)

    sell_order_placed_id = None

    @allure.step("Place the Buy order.")
    @automation_logger(logger)
    def test_place_buy_order(self, r_customer_sql):
        r_customer_sql.clean_instrument(instrument_id)
        r_customer_sql.clean_up_customer()

        r_customer_sql.postman.balance_service.add_balance(r_customer_sql.customer_id, quoted_currency, initial_sum)
        r_customer_sql.postman.balance_service.add_balance(r_customer_sql.customer_id, base_currency, initial_sum)

        order_response = r_customer_sql.postman.order_service.create_order_sync(TestTradePriceSmaller.order_buy)
        assert order_response['error'] is None

    @allure.step("Place the Sell order with smaller price.")
    @automation_logger(logger)
    def test_place_sell_order(self, r_customer_sql):
        order_response = r_customer_sql.postman.order_service.create_order_sync(TestTradePriceSmaller.order_sell)
        assert order_response['error'] is None
        TestTradePriceSmaller.sell_order_placed_id = order_response['result']['orderId']

    @allure.step("Verify Sell order is filled.")
    @automation_logger(logger)
    def test_verify_order_filled(self, r_customer_sql):
        time.sleep(TRADE_PROCESSING_DELAY)
        orders_in_db = Instruments.get_order_by_id(TestTradePriceSmaller.sell_order_placed_id)
        orders_list = Order.orders_data_converter(orders_in_db)

        logger.logger.info(f"Orders in DB: {orders_list}")
        print(f"Orders in DB: {orders_list}")
        logger.logger.info(f"Sell order filled quantity: {orders_list[0].filled_quantity}")
        print(f"Sell order filled quantity: {orders_list[0].filled_quantity}")

        assert float(orders_list[0].filled_quantity) == quantity_sell

    @allure.step("Verify no balance remains frozen.")
    @automation_logger(logger)
    def test_verify_no_frozen(self, r_customer_sql):
        # Verifying no balance is frozen - base currency:
        balance_response_dxcash = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id,
                                                                                           base_currency)
        assert float(balance_response_dxcash['result']['balance']['frozen']) == 0

        # Verifying no balance is frozen - quoted currency:
        balance_response_eth = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id,
                                                                                           quoted_currency)
        assert float(balance_response_eth['result']['balance']['frozen']) == 0

        logger.logger.info(f"Available balance : DXCASH  {balance_response_dxcash['result']['balance']['available']}")
        logger.logger.info(f"Available balance : ETH  {balance_response_eth['result']['balance']['available']}")

        assert float(balance_response_dxcash['result']['balance']['available']) == initial_sum
        assert float(balance_response_eth['result']['balance']['available']) == initial_sum

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
