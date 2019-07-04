import allure
import time
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "8136"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)

price_for_sell = Instruments.get_ticker_last_price(instrument_id)
price_for_buy = price_for_sell + 2

quantity_sell = 100.00

initial_sum = 10000

TRADE_PROCESSING_DELAY = 6


@allure.feature("Balance - User Flow")
@allure.story("Trade price smaller than Buy order price - balance is unfrozen.")
@allure.title("Trade price smaller than Buy order price - balance is unfrozen.")
@allure.description("""
    Functional tests.
    1. Place the Buy order.
    2. Place the Sell order with smaller price.
    3. Verify Sell order is filled.
    4. Verify no balance remains frozen.
    
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_user_flow_tests/C8136_trade_price_smaller_test.py",
                 "Trade price smaller than Buy order price - no frozen balance.")
class TestTradePriceSmaller(object):
    """
    Sell order is placed, Buy order is placed with a greater price right after.
    A trade is created. This test comes to verify that no funds remain in frozen balance.

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

        assert orders_list[0].filled_quantity == quantity_sell

    @allure.step("Verify no balance remains frozen.")
    @automation_logger(logger)
    def test_verify_no_frozen(self, r_customer_sql):
        # Verifying no balance is frozen - base currency:
        balance_response_xrp = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id,
                                                                                           base_currency)
        assert float(balance_response_xrp['result']['balance']['frozen']) == 0

        # Verifying no balance is frozen - quoted currency:
        balance_response_eur = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id,
                                                                                           quoted_currency)
        assert float(balance_response_eur['result']['balance']['frozen']) == 0

        logger.logger.info(f"Available balance : XRP  {balance_response_xrp['result']['balance']['available']}")
        logger.logger.info(f"Available balance : EUR  {balance_response_eur['result']['balance']['available']}")

        assert float(balance_response_xrp['result']['balance']['available']) == initial_sum
        assert float(balance_response_eur['result']['balance']['available']) == initial_sum

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
