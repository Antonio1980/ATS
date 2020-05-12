import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "6868"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]
price_for_buy = 5
price_for_sell = price_for_buy
quantity_sell = 700.00

# The parameters below are mandatory to sustain test conditions.
quantity_buy = quantity_sell  # For this test "quantity_buy" must be 50% of "quantity_sell".

WAIT_FOR_TRADE_DELAY = 4

@allure.feature("Sell order is fully filled - customer's balance update verified.")
@allure.story("Fully filled 'Sell' orders - customer's balance is updated.")
@allure.title("End-to-End flow verification")
@allure.description("""
    Functional tests.
    1. Clear the Order Book for the selected instrument.
    2. Create two customers and save the tokens.
    3. Add balance for both customers used for this test.
    4. Change current reference price to 'price_for_buy'.
    5. Place the 'Sell' order, quantity - 700 .
    6. Place the 'Buy' order, quantity - 700.
    7. Verify balance update after the trade - buyer.
    8. Verify balance update after the trade - seller.
    9. Restore the original reference price.
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/partially_filled_orders_tests/C6868_filled_sell_100_balance_update_test.py",
                 "TestSellBalanceUpdated_100")
@pytest.mark.usefixtures("r_customer")
class TestSellFullyFilled(object):
    original_last_trade_price = ""
    original_ticker_last = ""

    order_buy = Order()
    order_buy.set_order(1, instrument_id, quantity_buy, price_for_buy)

    order_sell = Order()
    order_sell.set_order(2, instrument_id, quantity_sell, price_for_sell)

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
        TestSellFullyFilled.buyer = test_customers[0][0]
        TestSellFullyFilled.seller = test_customers[1][0]

        TestSellFullyFilled.buyer_token = test_customers[0][1]
        TestSellFullyFilled.seller_token = test_customers[1][1]

    @allure.step("Add balance for both customers used for this test.")
    @automation_logger(logger)
    def test_add_balance(self):
        print(F"Test {TestSellFullyFilled.buyer}")
        balance_response_buyer = TestSellFullyFilled.buyer.postman.get_static_postman(TestSellFullyFilled.buyer_token). \
            balance_service.add_balance(TestSellFullyFilled.buyer.customer_id, quoted_currency, 10000)

        assert float(balance_response_buyer['result']['balance']['available']) == 10000
        assert float(balance_response_buyer['result']['balance']['total']) == 10000

        balance_response_seller = TestSellFullyFilled.seller.postman.get_static_postman(TestSellFullyFilled.seller_token). \
            balance_service.add_balance(TestSellFullyFilled.seller.customer_id, base_currency, 10000)

        assert float(balance_response_seller['result']['balance']['available']) == 10000
        assert float(balance_response_seller['result']['balance']['total']) == 10000

    @allure.step("Change current reference price to 'price_for_buy'.")
    @automation_logger(logger)
    def test_change_reference_price(self, r_customer):
        TestSellFullyFilled.original_last_trade_price = Instruments.get_price_last_trade(instrument_id)
        Instruments.set_price_last_trade(instrument_id, price_for_buy)
        assert int(Instruments.get_price_last_trade(instrument_id)) == price_for_buy

        TestSellFullyFilled.original_ticker_last = Instruments.get_ticker_last_price(instrument_id)
        Instruments.set_ticker_last_price(instrument_id, price_for_buy)
        assert int(Instruments.get_ticker_last_price(instrument_id)) == price_for_buy

    @allure.step("Place the 'Sell' order, quantity - 700 .")
    @automation_logger(logger)
    def test_place_sell_order(self):
        order_response = TestSellFullyFilled.seller.postman.get_static_postman(TestSellFullyFilled.seller_token). \
            order_service.create_order_sync(TestSellFullyFilled.order_sell)
        assert order_response['error'] is None

        seller_balance = TestSellFullyFilled.seller.postman.get_static_postman(TestSellFullyFilled.seller_token). \
            balance_service.get_all_currencies_balance(TestSellFullyFilled.seller.customer_id)

        # Seller balance - XRP
        assert float(seller_balance['result'][base_currency-1]['balance']['available']) == 10000 - quantity_sell
        assert float(seller_balance['result'][base_currency-1]['balance']['frozen']) == quantity_sell

    @allure.step("Place the 'Buy' order, quantity - 700.")
    @automation_logger(logger)
    def test_place_buy_order(self):
        order_response = TestSellFullyFilled.buyer.postman.get_static_postman(TestSellFullyFilled.buyer_token). \
            order_service.create_order_sync(TestSellFullyFilled.order_buy)
        assert order_response['error'] is None

    @allure.step("Verify balance update after the trade - buyer.")
    @automation_logger(logger)
    def test_verify_buyer_balance(self):
        time.sleep(WAIT_FOR_TRADE_DELAY)

        buyer_balance = TestSellFullyFilled.buyer.postman.get_static_postman(TestSellFullyFilled.buyer_token). \
            balance_service.get_all_currencies_balance(TestSellFullyFilled.buyer.customer_id)

        # Buyer - EUR
        assert float(buyer_balance['result'][quoted_currency-1]['balance']['frozen']) == 0
        assert float(buyer_balance['result'][quoted_currency-1]['balance']['total']) == 10000 - quantity_buy * price_for_buy
        assert float(buyer_balance['result'][quoted_currency-1]['balance']['available']) == 10000 - quantity_buy * price_for_buy

        # Buyer - XRP
        assert float(buyer_balance['result'][base_currency-1]['balance']['frozen']) == 0
        assert float(buyer_balance['result'][base_currency-1]['balance']['available']) == quantity_buy
        assert float(buyer_balance['result'][base_currency-1]['balance']['total']) == quantity_buy

    @allure.step("Verify balance update after the trade - seller.")
    @automation_logger(logger)
    def test_verify_seller_balance(self):
        seller_balance = TestSellFullyFilled.seller.postman.get_static_postman(TestSellFullyFilled.seller_token). \
            balance_service.get_all_currencies_balance(TestSellFullyFilled.seller.customer_id)

        # Seller - EUR
        assert float(seller_balance['result'][quoted_currency-1]['balance']['frozen']) == 0
        assert float(seller_balance['result'][quoted_currency-1]['balance']['total']) == quantity_buy * price_for_buy
        assert float(seller_balance['result'][quoted_currency-1]['balance']['available']) == quantity_buy * price_for_buy

        # Seller - XRP
        assert float(seller_balance['result'][base_currency-1]['balance']['frozen']) == quantity_sell - quantity_buy
        assert float(seller_balance['result'][base_currency-1]['balance']['total']) == 10000 - quantity_buy
        assert float(seller_balance['result'][base_currency-1]['balance']['available']) == 10000 - quantity_sell

    @allure.step("Restore the original reference price.")
    @automation_logger(logger)
    def test_restore_original_price(self):
        Instruments.set_price_last_trade(instrument_id, TestSellFullyFilled.original_last_trade_price)
        Instruments.set_ticker_last_price(instrument_id, TestSellFullyFilled.original_ticker_last)

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")

