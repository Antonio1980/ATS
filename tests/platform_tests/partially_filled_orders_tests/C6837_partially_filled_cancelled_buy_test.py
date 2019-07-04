import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "6837"

"""
    In this test we are testing the flow of partially filled "Buy" order cancellation.
    Customer places "Buy" order that is 10% filled and cancelled right after.
    We expect customer's balance to be updated after the trade and after Order Cancellation (should be unfrozen).  
    We shall verify that there is no descrepancy between customer's balance in Redis and in Balance Service after order cancellaiton.
"""

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]

price_for_buy = 5
price_for_sell = price_for_buy
quantity_buy = 700.00

# The parameters below are mandatory to sustain test conditions.
quantity_sell = quantity_buy / 10  # For this test "quantity_sell" must be 10% of "quantity_buy".

WAIT_FOR_TRADE_DELAY = 5


@allure.feature("Partially filled order is cancelled - balance is updated accordingly")
@allure.story("Partially filled orders - balance update.")
@allure.title("Partially filled order is cancelled - balance is updated accordingly")
@allure.description("""
    Functional tests.
    1. Clear the Order Book for the selected instrument.
    2. Create two customers and save the tokens.
    3. Add balance for both customers used for this test.
    4. Change current reference price to 'price_for_buy'.
    5. Place the 'Buy' order, quantity - 700.
    6. Place the 'Sell' order, quantity - 70.
    7. Verify 'Buy' order is partially filled.
    8. Cancel the 'Buy' order - partially filled.
    9. Verifying balance in Redis and in Balance Service
       """)
@pytest.mark.incremental
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/partially_filled_orders_tests/C6837_partially_filled_cancelled_buy_test.py",
                 "TestPartiallyFilledCancelled")
@pytest.mark.usefixtures("r_customer")
class TestCancelPartiallyFilled(object):
    original_last_trade_price = ""
    original_ticker_last = ""

    order_buy = Order()
    order_buy.set_order(1, instrument_id, quantity_buy, price_for_buy)

    order_sell = Order()
    order_sell.set_order(2, instrument_id, quantity_sell, price_for_sell)

    # Those class variables are used to save placed orders ID's.
    placed_buy_order_id = ""
    placed_sell_order_id = ""

    buyer = None
    seller = None

    buyer_token = ""
    seller_token = ""


    @allure.step("Clear the Order Book for the selected instrument.")
    @automation_logger(logger)
    def test_janitor(self, r_customer):
        r_customer.clean_instrument(instrument_id, base_currency, quoted_currency)

    @automation_logger(logger)
    @allure.step("Create two customers and save the tokens")
    def test_create_customers(self, r_customer):
        # Creating two new customers
        test_customers = Instruments.create_two_customers()

        # Saving the customers and their authorization tokens to class variables.
        TestCancelPartiallyFilled.buyer = test_customers[0][0]
        TestCancelPartiallyFilled.seller = test_customers[1][0]

        TestCancelPartiallyFilled.buyer_token = test_customers[0][1]
        TestCancelPartiallyFilled.seller_token = test_customers[1][1]

    @allure.step("Add balance for both customers used for this test.")
    @automation_logger(logger)
    def test_add_balance(self):
        print(F"Test {TestCancelPartiallyFilled.buyer}")
        balance_response_buyer = TestCancelPartiallyFilled.buyer.postman.get_static_postman(
            TestCancelPartiallyFilled.buyer_token). \
            balance_service.add_balance(TestCancelPartiallyFilled.buyer.customer_id, quoted_currency, 10000)

        assert float(balance_response_buyer['result']['balance']['available']) == 10000
        assert float(balance_response_buyer['result']['balance']['total']) == 10000

        balance_response_seller = TestCancelPartiallyFilled.seller.postman.get_static_postman(
            TestCancelPartiallyFilled.seller_token). \
            balance_service.add_balance(TestCancelPartiallyFilled.seller.customer_id, base_currency, 10000)

        assert float(balance_response_seller['result']['balance']['available']) == 10000
        assert float(balance_response_seller['result']['balance']['total']) == 10000

    @allure.step("Change current reference price to 'price_for_buy'.")
    @automation_logger(logger)
    def test_change_reference_price(self, r_customer):
        TestCancelPartiallyFilled.original_last_trade_price = Instruments.get_price_last_trade(instrument_id)
        Instruments.set_price_last_trade(instrument_id, price_for_buy)
        assert int(Instruments.get_price_last_trade(instrument_id)) == price_for_buy

        TestCancelPartiallyFilled.original_ticker_last = Instruments.get_ticker_last_price(instrument_id)
        Instruments.set_ticker_last_price(instrument_id, price_for_buy)
        assert int(Instruments.get_ticker_last_price(instrument_id)) == price_for_buy

    @allure.step("Place the 'Buy' order, quantity - 700.")
    @automation_logger(logger)
    def test_place_buy_order(self):
        order_response = TestCancelPartiallyFilled.buyer.postman.get_static_postman(
            TestCancelPartiallyFilled.buyer_token). \
            order_service.create_order_sync(TestCancelPartiallyFilled.order_buy)
        assert order_response['error'] is None

        TestCancelPartiallyFilled.placed_buy_order_id = order_response['result']['orderId']

    @allure.step("Place the 'Sell' order, quantity - 70.")
    @automation_logger(logger)
    def test_place_sell_order(self):
        order_response = TestCancelPartiallyFilled.seller.postman.get_static_postman(
            TestCancelPartiallyFilled.seller_token). \
            order_service.create_order_sync(TestCancelPartiallyFilled.order_sell)
        assert order_response['error'] is None

    @allure.step("Verify 'Buy' order is partially filled")
    @automation_logger(logger)
    def test_verify_partially_filled(self):
        # Waiting for trade to be processed.
        time.sleep(WAIT_FOR_TRADE_DELAY)

        # "Buy" order, partially filled.
        buy_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(TestCancelPartiallyFilled.placed_buy_order_id))
        print(F"Buy Order In DB: {buy_order_in_db}")
        assert len(buy_order_in_db) == 1
        assert buy_order_in_db[0].quantity == TestCancelPartiallyFilled.order_buy.quantity
        assert buy_order_in_db[0].filled_quantity == TestCancelPartiallyFilled.order_sell.quantity

    @allure.step("Cancel the 'Buy' order - partially filled")
    @automation_logger(logger)
    def test_cancel_buy_order(self):
        response = TestCancelPartiallyFilled.buyer.postman.get_static_postman(TestCancelPartiallyFilled.buyer_token). \
            order_service.cancel_order(TestCancelPartiallyFilled.placed_buy_order_id)
        assert response['error'] is None
        print(
            f"Cancelled Order ID: {TestCancelPartiallyFilled.placed_buy_order_id}, Order cancellation response: {response}")

    @allure.step("Verifying balance in Redis and in Balance Service")
    @automation_logger(logger)
    def test_verify_buyer_balance(self):
        # Waiting for balance to be updated after order cancellation.
        time.sleep(WAIT_FOR_TRADE_DELAY - 2)

        # Verifying balance in Balance Service after order cancellation
        buyer_balance = TestCancelPartiallyFilled.buyer.postman.get_static_postman(
            TestCancelPartiallyFilled.buyer_token). \
            balance_service.get_all_currencies_balance(TestCancelPartiallyFilled.buyer.customer_id)

        # After partially filled "Buy" trade was cancelled the sum that was frozen is returned to Buyer's available balance.
        # The amount of EUR that was paid for 70 XRP that the customer has bough is deducted from his available balance:
        # 10000 - 70 x 5 = 9650

        # Buyer, balance in EUR - Balance Service
        assert float(buyer_balance['result'][quoted_currency - 1]['balance']['frozen']) == 0
        assert float(buyer_balance['result'][quoted_currency - 1]['balance']['available']) == 10000 - quantity_sell * price_for_buy

        # Buyer, available balance in EUR - Redis
        assert Instruments.get_customer_balance_redis(TestCancelPartiallyFilled.buyer.customer_id, quoted_currency)[0] == 10000 - quantity_sell * price_for_buy
        # Buyer, frozen balance in EUR - Redis
        assert Instruments.get_customer_balance_redis(TestCancelPartiallyFilled.buyer.customer_id, quoted_currency)[1] == 0

        # After the order was partially filled and a trade was created 70 XRP that were bough are added to customer's balance.
        # Order cancellation has no effect

        # Buyer, balance in XRP - Balance Service
        assert float(buyer_balance['result'][base_currency - 1]['balance']['frozen']) == 0
        assert float(buyer_balance['result'][base_currency - 1]['balance']['available']) == quantity_sell

        # Buyer, available balance in XRP - Redis
        assert Instruments.get_customer_balance_redis(TestCancelPartiallyFilled.buyer.customer_id, base_currency)[
                   0] == quantity_sell
        # Buyer, frozen balance in XRP - Redis
        assert Instruments.get_customer_balance_redis(TestCancelPartiallyFilled.buyer.customer_id, base_currency)[
                   1] == 0

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")

