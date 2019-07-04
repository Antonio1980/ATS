import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "6843"

"""
    In this test we are to verify that balance is updated both in Redis and Balance Service
    after  Order Placement and Trade.
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

WAIT_FOR_TRADE_DELAY = 6


@allure.feature("Balance in Redis is updated after order and trade.")
@allure.story("Partially filled 'Buy' orders - customer's balance is updated in Redis.")
@allure.title("Balance in Redis is updated after order and trade.")
@allure.description("""
    Functional tests.
    1. Clear the Order Book for the selected instrument.
    2. Create two customers and save the tokens.
    3. Add balance for both customers used for this test.
    4. Change current reference price to 'price_for_buy'.
    5. Place the 'Buy' order and verify Redis balance update, quantity - 700.
    6. Place the 'Sell' order, quantity - 70.
    7. Verify balance update in Redis after the trade - seller.
    8. Verify balance update in Redis after the trade - buyer.
    9. Restore the original reference price.
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/partially_filled_orders_tests/C6843_balance_redis_sync_test.py",
                 "TestBalanceUpdatedRedis")
@pytest.mark.usefixtures("r_customer")
class TestTenFilled(object):
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

    @allure.step("Create two customers and save the tokens")
    @automation_logger(logger)
    def test_create_customers(self, r_customer):
        # Creating two new customers
        test_customers = Instruments.create_two_customers()

        # Saving the customers and their authorization tokens to class variables.
        TestTenFilled.buyer = test_customers[0][0]
        TestTenFilled.seller = test_customers[1][0]

        TestTenFilled.buyer_token = test_customers[0][1]
        TestTenFilled.seller_token = test_customers[1][1]

    @allure.step("Add balance for both customers used for this test.")
    @automation_logger(logger)
    def test_add_balance(self):
        print(F"Test {TestTenFilled.buyer}")
        balance_response_buyer = TestTenFilled.buyer.postman.get_static_postman(TestTenFilled.buyer_token). \
            balance_service.add_balance(TestTenFilled.buyer.customer_id, quoted_currency, 10000)

        assert float(balance_response_buyer['result']['balance']['available']) == 10000
        assert float(balance_response_buyer['result']['balance']['total']) == 10000

        balance_response_seller = TestTenFilled.seller.postman.get_static_postman(TestTenFilled.seller_token). \
            balance_service.add_balance(TestTenFilled.seller.customer_id, base_currency, 10000)

        assert float(balance_response_seller['result']['balance']['available']) == 10000
        assert float(balance_response_seller['result']['balance']['total']) == 10000

    @allure.step("Change current reference price to 'price_for_buy'.")
    @automation_logger(logger)
    def test_change_reference_price(self, r_customer):
        TestTenFilled.original_last_trade_price = Instruments.get_price_last_trade(instrument_id)
        Instruments.set_price_last_trade(instrument_id, price_for_buy)
        assert int(Instruments.get_price_last_trade(instrument_id)) == price_for_buy

        TestTenFilled.original_ticker_last = Instruments.get_ticker_last_price(instrument_id)
        Instruments.set_ticker_last_price(instrument_id, price_for_buy)
        assert int(Instruments.get_ticker_last_price(instrument_id)) == price_for_buy

    @allure.step("Place the 'Buy' order and verify Redis balance update, quantity - 700")
    @automation_logger(logger)
    def test_place_buy_order(self):
        order_response = TestTenFilled.buyer.postman.get_static_postman(TestTenFilled.buyer_token). \
            order_service.create_order_sync(TestTenFilled.order_buy)
        assert order_response['error'] is None

        buyer_balance = TestTenFilled.buyer.postman.get_static_postman(TestTenFilled.buyer_token).balance_service. \
            get_currency_balance(TestTenFilled.buyer.customer_id, quoted_currency)

        # Buyer, Balance in Balance Service - EUR
        assert float(buyer_balance['result']['balance']['available']) == 10000 - quantity_buy * price_for_buy
        assert float(buyer_balance['result']['balance']['frozen']) == quantity_buy * price_for_buy

        # Buyer, Available balance in Redis - EUR
        assert Instruments.get_customer_balance_redis(TestTenFilled.buyer.customer_id, quoted_currency)[0] == \
               10000 - quantity_buy * price_for_buy

        # Buyer, Frozen balance in Redis - EUR
        assert Instruments.get_customer_balance_redis(TestTenFilled.buyer.customer_id, quoted_currency)[1] == \
               quantity_buy * price_for_buy

        print(F"Buyer balance: {buyer_balance}")

    @allure.step("Place the 'Sell' order, quantity - 70.")
    @automation_logger(logger)
    def test_place_sell_order(self):
        order_response = TestTenFilled.seller.postman.get_static_postman(TestTenFilled.seller_token). \
            order_service.create_order_sync(TestTenFilled.order_sell)
        assert order_response['error'] is None

    @allure.step("Verify balance update after the trade - seller.")
    @automation_logger(logger)
    def test_verify_seller_balance(self):
        time.sleep(WAIT_FOR_TRADE_DELAY)

        seller_balance = TestTenFilled.seller.postman.get_static_postman(TestTenFilled.seller_token). \
            balance_service.get_all_currencies_balance(TestTenFilled.seller.customer_id)

        print(seller_balance['result'][base_currency - 1]['balance'])

        # Seller, Balance in Balance Service - EUR
        assert float(seller_balance['result'][quoted_currency - 1]['balance']['total']) == quantity_sell * price_for_buy
        assert float(seller_balance['result'][quoted_currency - 1]['balance']['available']) == quantity_sell * price_for_buy

        # Seller, Balance in Balance Service - XRP
        assert float(seller_balance['result'][base_currency - 1]['balance']['total']) == 10000 - quantity_sell
        assert float(seller_balance['result'][base_currency - 1]['balance']['available']) == 10000 - quantity_sell

        # Seller, Available balance in Redis - EUR
        assert Instruments.get_customer_balance_redis(TestTenFilled.seller.customer_id, quoted_currency)[0] == quantity_sell * price_for_buy

        # Seller, Frozen balance in Redis - EUR
        assert Instruments.get_customer_balance_redis(TestTenFilled.seller.customer_id, quoted_currency)[1] == 0

        # Seller, Available balance in Redis - XRP
        assert Instruments.get_customer_balance_redis(TestTenFilled.seller.customer_id, base_currency)[0] == 10000 - quantity_sell

        # Seller, Frozen balance in Redis - XRP
        assert Instruments.get_customer_balance_redis(TestTenFilled.seller.customer_id, base_currency)[1] == 0

    @allure.step("Verify balance update after the trade - buyer.")
    @automation_logger(logger)
    def test_verify_buyer_balance(self):
        buyer_balance = TestTenFilled.buyer.postman.get_static_postman(TestTenFilled.buyer_token). \
            balance_service.get_all_currencies_balance(TestTenFilled.buyer.customer_id)

        # Buyer, Balance in Balance Service - EUR
        assert float(
            buyer_balance['result'][quoted_currency - 1]['balance']['frozen']) == quantity_buy * price_for_buy * 0.9

        assert float(
            buyer_balance['result'][quoted_currency - 1]['balance']['total']) == 10000 - quantity_sell * price_for_buy

        assert float(buyer_balance['result'][quoted_currency - 1]['balance']['available']) == \
               10000 - quantity_sell * price_for_buy - quantity_buy * price_for_buy * 0.9


        # Buyer, Frozen balance in Redis - EUR
        assert Instruments.get_customer_balance_redis(TestTenFilled.buyer.customer_id, quoted_currency)[
                   1] == quantity_buy * price_for_buy * 0.9


        # Buyer, Available balance in Redis - EUR
        assert Instruments.get_customer_balance_redis(TestTenFilled.buyer.customer_id, quoted_currency)[0] == \
               10000 - quantity_sell * price_for_buy - quantity_buy * price_for_buy * 0.9

        # Buyer, Balance in Balance Service - XRP
        assert float(buyer_balance['result'][base_currency - 1]['balance']['frozen']) == 0
        assert float(buyer_balance['result'][base_currency - 1]['balance']['available']) == quantity_sell
        assert float(buyer_balance['result'][base_currency - 1]['balance']['total']) == quantity_sell

        # Buyer, Frozen balance in Redis - XRP
        assert Instruments.get_customer_balance_redis(TestTenFilled.buyer.customer_id, base_currency)[1] == 0
        # Buyer, Available balance in Redis - XRP
        assert Instruments.get_customer_balance_redis(TestTenFilled.buyer.customer_id, base_currency)[0] == quantity_sell

    @allure.step("Restore the original reference price.")
    @automation_logger(logger)
    def test_restore_original_price(self):
        Instruments.set_price_last_trade(instrument_id, TestTenFilled.original_last_trade_price)
        Instruments.set_ticker_last_price(instrument_id, TestTenFilled.original_ticker_last)

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")

