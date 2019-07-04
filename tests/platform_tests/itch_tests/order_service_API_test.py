import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig
from src.base.utils.calculator import Calculator

test_case = "order_service_API_test"

"""
Order Service API has a method that provides all the data that  Order Book contains.
This test comes to verify, that the date provided by Order Service API is identical
to the Order Book received from ME and stored in Redis.
Order Book provided by Order Service API can be taken from ANY source, as long at is identical to
the Order Book stored in Redis.

Original test flow:

    1. Clear the Order Book for the selected instrument.
    2. Clear the balance of the customer used for this test, cancel all orders.
    3. Add funds to customer's available balance and verify.
    4. Set the reference price to the REFERENCE_PRICE.
    5. Place the 'Buy' order.
    6. Place the 'Sell' order.
    7. Verify 'Buy' Order Book is updated accordingly.
    8. Verify 'Sell' Order Book is updated accordingly.
    9. Verifying the information received from Order API.
"""

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]

reference_price = 5
price_for_buy = reference_price - 2
price_for_sell = reference_price + 2
quantity_buy = 80.0
quantity_sell = 70.0

CANCELLING_ORDERS_DELAY = 5


@pytest.mark.incremental
@allure.feature("Order Book provided by Order Service.")
@allure.story("Order Book from Order Service API - end to end test.")
@allure.title("End-to-End flow verification")
@allure.description("""
    Functional tests.
    1. Verify 'Buy' Order Book is updated accordingly.
    2. Verify 'Sell' Order Book is updated accordingly.
    3. Verifying the information received from Order API.
    4. Restore the original last trade  price and ticker last.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/itch_tests/order_service_API_test.py",
                 "TestOrderBook_order_API")
@pytest.mark.usefixtures("r_customer")
class TestOrderAPI(object):

    @automation_logger(logger)
    @allure.step("Verify 'Buy' Order Book is updated accordingly.")
    @pytest.mark.parametrize('itch_order_buy', [[instrument_id, quantity_buy, price_for_buy]], indirect=True)
    @pytest.mark.parametrize('itch_order_sell', [[instrument_id, quantity_sell, price_for_sell]], indirect=True)
    def test_buy_order_book(self, r_customer, create_customer, itch_order_buy, itch_order_sell):
        order_book = Instruments.get_orders_best_price_and_quantity(instrument_id, "sell", 2)
        # Only one record must be added to the Order Book.
        assert len(order_book) == 1

        for record in order_book:
            # Price verification
            assert record[0] == price_for_buy
            # Quantity verification
            assert record[1] == quantity_buy

    @allure.step("Verify 'Sell' Order Book is updated accordingly.")
    @automation_logger(logger)
    def test_sell_order_book(self):
        order_book = Instruments.get_orders_best_price_and_quantity(instrument_id, "buy", 2)
        assert len(order_book) == 1

        for record in order_book:
            assert record[0] == price_for_sell
            assert record[1] == quantity_sell

    @allure.step("Verifying the information received from Order API.")
    @automation_logger(logger)
    def test_get_order_book_api(self, r_customer):
        # Getting the Order Book from Order Service API.
        response = r_customer.postman.order_service.get_order_book(instrument_id)

        # Comparing the date from Order Service to Order Book provided by ITCH integration and stored in Redis.
        sell_price = Calculator.value_decimal(response['result']['buy'][0]['price'])
        assert sell_price == price_for_sell

        sell_quantity = Calculator.value_decimal(response['result']['buy'][0]['qty'])
        assert sell_quantity == quantity_sell

        buy_price = Calculator.value_decimal(response['result']['sell'][0]['price'])
        assert buy_price == price_for_buy

        buy_quantity = Calculator.value_decimal(response['result']['sell'][0]['qty'])
        assert buy_quantity == quantity_buy

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
