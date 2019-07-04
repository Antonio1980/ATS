import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "first_orders_itch_test"

"""
This test comes to verify, that new record is created in Order Book when an order is placed with a distinct price.
and that Order Book receives updates from ME and the values in Redis are updated accordingly.

Original test flow:
("
    Functional tests.
    1. Clear the Order Book for the selected instrument.
    2. Clear the balance of the customer used for this test, cancel all orders.
    3. Add funds to customer's available balance and verify.
    4. Set the reference price to the REFERENCE_PRICE.
    5. Place the 'Buy' order.
    6. Place the 'Sell' order.
    7. Verify 'Buy' Order Book is updated accordingly.
    8. Verify 'Sell' Order Book is updated accordingly.
    ")
"""

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]

standart_price = 5
price_for_buy = standart_price - 2
price_for_sell = standart_price + 2
quantity_buy = 80.0
quantity_sell = 70.0

CANCELLING_ORDERS_DELAY = 5


@pytest.mark.incremental
@allure.feature("Order Book update - end to end test.")
@allure.story("Order Book updated when an order is placed - end to end test.")
@allure.title("Order Book update - end to end test.")
@allure.description("""
    Functional tests.
    1. Verify 'Buy' Order Book is updated accordingly.
    2. Verify 'Sell' Order Book is updated accordingly.   
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/itch_tests/first_orders_test.py",
                 "TestOrderBook_update_verification")
@pytest.mark.usefixtures("r_customer")
class TestFirstOrders(object):

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

        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))
        print("================== TEST CASE PASSED ===================".format(test_case))
