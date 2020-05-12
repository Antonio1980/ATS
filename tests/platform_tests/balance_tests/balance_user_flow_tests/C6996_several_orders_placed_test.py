
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "6996"

# This test comes to verify the flow in which customer places "Sell" orders on a given instrument
# again and again, until all his balance is frozen. The amount of orders that were placed is verified.
# After all orders were placed all customer's balance must be frozen WITHOUT delay .

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)

price_for_sell = 5
quantity_sell = 100.00

initial_sum = 10000


@allure.feature("Balance - User Flow")
@allure.story("User has placed several orders, all his balance is frozen.")
@allure.title("User has placed several orders, all his balance is frozen.")
@allure.description("""
    Functional tests.
    1. Clear the Order Book for the selected instrument.
    2. Clear the balance of the customer used for this test, cancel all orders
    3. Add 10000 and save customer's balance.
    4. Place enough orders to freeze all the balance.
    5. Verify the balance after all orders were placed. 
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_user_flow_tests/C6996_several_orders_placed_test.py",
                 "Placed_Orders_all_frozen")
@pytest.mark.usefixtures("r_customer")
class TestPlacedSeveralOrders(object):
    original_last_trade_price = 0
    original_ticker_last = 0

    test_customer_balance_available = 0
    test_customer_balance_frozen = 0

    order_counter = 0

    sell_order = Order().set_order(2, instrument_id, quantity_sell, price_for_sell)

    @allure.step("Clear the Order Book for the selected instrument.")
    @automation_logger(logger)
    def test_janitor(self, r_customer):
        r_customer.clean_instrument(instrument_id, base_currency, quoted_currency)

    @allure.step("Clear the balance of the customer used for this test, cancel all orders")
    @automation_logger(logger)
    def test_clean_up_customer(self, r_customer):
        r_customer.clean_up_customer()
        cur_orders = r_customer.postman.order_service.get_open_orders()
        assert len(cur_orders['result']['orders']) == 0
        print(F"Clean Customer method - existing orders: {cur_orders['result']['orders']}")

    @allure.step("Add 10000 and save customer's balance.")
    @automation_logger(logger)
    def test_add_save_balance(self, r_customer):
        r_customer.postman.balance_service.add_balance(r_customer.customer_id, base_currency, initial_sum)

        response = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, base_currency)
        assert float(response['result']['balance']['available']) == initial_sum

        TestPlacedSeveralOrders.test_customer_balance_available = \
            float(response['result']['balance']['available'])
        TestPlacedSeveralOrders.test_customer_balance_frozen = \
            float(response['result']['balance']['frozen'])

        logger.logger.info(
            F"Customer's balance available before orders are placed - response: "
            F"{TestPlacedSeveralOrders.test_customer_balance_available}")
        print(
            F"Customer's  available balance before orders are placed - response: "
            F"{TestPlacedSeveralOrders.test_customer_balance_available}")

    @allure.step("Place enough orders to freeze all the balance.")
    @automation_logger(logger)
    def test_place_orders(self, r_customer):
        TestPlacedSeveralOrders.original_last_trade_price = Instruments.get_price_last_trade(instrument_id)
        TestPlacedSeveralOrders.original_ticker_last = Instruments.get_ticker_last_price(instrument_id)

        Instruments.set_price_last_trade(instrument_id, price_for_sell)
        Instruments.set_ticker_last_price(instrument_id, price_for_sell)

        while TestPlacedSeveralOrders.test_customer_balance_available > 0:
            response = r_customer.postman.order_service.create_order(TestPlacedSeveralOrders.sell_order)
            assert response['error'] is None
            # This variable is used to count the amount of orders that were placed .
            TestPlacedSeveralOrders.order_counter += 1

            TestPlacedSeveralOrders.test_customer_balance_available -= quantity_sell

        Instruments.set_price_last_trade(instrument_id, TestPlacedSeveralOrders.original_last_trade_price)
        Instruments.set_ticker_last_price(instrument_id, TestPlacedSeveralOrders.original_ticker_last)

    @allure.step("Verify the balance after all orders were placed. ")
    @automation_logger(logger)
    def test_verify_result(self, r_customer):
        response = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, base_currency)

        TestPlacedSeveralOrders.test_customer_balance_available = \
            float(response['result']['balance']['available'])
        TestPlacedSeveralOrders.test_customer_balance_frozen = \
            float(response['result']['balance']['frozen'])

        logger.logger.info(
            F"Customer's balance available after orders are placed - response: "
            F"{TestPlacedSeveralOrders.test_customer_balance_available}")
        print(
            F"Customer's  available balance after orders are placed - response: "
            F"{TestPlacedSeveralOrders.test_customer_balance_available}")

        # Verifying the amount of orders that was placed.
        assert TestPlacedSeveralOrders.order_counter == initial_sum // quantity_sell

        # Verifying all balance was frozen
        assert TestPlacedSeveralOrders.test_customer_balance_available == 0
        assert TestPlacedSeveralOrders.test_customer_balance_frozen == initial_sum

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
