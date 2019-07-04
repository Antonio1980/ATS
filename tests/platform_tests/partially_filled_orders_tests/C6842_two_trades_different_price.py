import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "6842"

"""
    In this test we are testing customer balance update after a trade.
    The trade was performed after an order was partially filled - 10%.
    Both customers balance was updated accordingly - the buyer's and the seller's.
"""

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]
price_for_buy = 6
price_for_sell_1 = 5
price_for_sell_2 = 4

quantity_buy = 700

quantity_sell = quantity_buy / 2

WAIT_FOR_TRADE_DELAY = 5


@pytest.mark.incremental
@allure.feature("Two trades on one order with different prices - balance is updating accordingly. ")
@allure.story("Trading and Balance - end to end testing. ")
@allure.title("Two trades on one order with different prices - balance is updating accordingly.  ")
@allure.description("""
    Functional tests.
    1. Clear the Order Book for the selected instrument.
    2. Create two customers and save the tokens.
    3. Add balance for both customers used for this test.
    4. Change current reference price to 'price_for_buy'.
    5. Place two 'Sell' orders, each with quantity - 350.
    6. Place the 'Buy' order, quantity - 700.
    7. Verify balance update after the trade - seller.
    8. Verify balance update after the trade - buyer.
    9. Restore the original reference price.
       """)
@pytest.mark.incremental
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/partially_filled_orders_tests/C6842_two_trades_different_price.py",
                 "TestTwoTradesDifferentPrice")
@pytest.mark.usefixtures("r_customer")
class TestTwoTradesDifferentPrice(object):
    original_last_trade_price = ""
    original_ticker_last = ""

    order_buy = Order()
    order_buy.set_order(1, instrument_id, quantity_buy, price_for_buy)

    order_sell_1 = Order()
    order_sell_1.set_order(2, instrument_id, quantity_sell, price_for_sell_1)

    order_sell_2 = Order()
    order_sell_2.set_order(2, instrument_id, quantity_sell, price_for_sell_2)

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
        TestTwoTradesDifferentPrice.original_last_trade_price = Instruments.get_price_last_trade(instrument_id)
        TestTwoTradesDifferentPrice.original_ticker_last = Instruments.get_ticker_last_price(instrument_id)

        r_customer.clean_instrument(instrument_id)

    @allure.step("Create two customers and save the tokens")
    @automation_logger(logger)
    def test_create_customers(self, r_customer):
        # Creating two new customers
        test_customers = Instruments.create_two_customers()

        # Saving the customers and their authorization tokens to class variables.
        TestTwoTradesDifferentPrice.buyer = test_customers[0][0]
        TestTwoTradesDifferentPrice.seller = test_customers[1][0]

        TestTwoTradesDifferentPrice.buyer_token = test_customers[0][1]
        TestTwoTradesDifferentPrice.seller_token = test_customers[1][1]

    @allure.step("Add balance for both customers used for this test.")
    @automation_logger(logger)
    def test_add_balance(self):
        print(F"Test {TestTwoTradesDifferentPrice.buyer}")
        balance_response_buyer = TestTwoTradesDifferentPrice.buyer.postman.get_static_postman(
            TestTwoTradesDifferentPrice.buyer_token). \
            balance_service.add_balance(TestTwoTradesDifferentPrice.buyer.customer_id, quoted_currency, 10000)

        # "Buyer" receives 10000 EUR, "Seller" receives 10000 XRP.

        assert float(balance_response_buyer['result']['balance']['available']) == 10000
        assert float(balance_response_buyer['result']['balance']['total']) == 10000

        balance_response_seller = TestTwoTradesDifferentPrice.seller.postman.get_static_postman(
            TestTwoTradesDifferentPrice.seller_token). \
            balance_service.add_balance(TestTwoTradesDifferentPrice.seller.customer_id, base_currency, 10000)

        assert float(balance_response_seller['result']['balance']['available']) == 10000
        assert float(balance_response_seller['result']['balance']['total']) == 10000

    @allure.step("Change current reference price to 'price_for_buy'.")
    @automation_logger(logger)
    def test_change_reference_price(self, r_customer):
        Instruments.set_price_last_trade(instrument_id, price_for_buy)
        assert int(Instruments.get_price_last_trade(instrument_id)) == price_for_buy

        Instruments.set_ticker_last_price(instrument_id, price_for_buy)
        assert int(Instruments.get_ticker_last_price(instrument_id)) == price_for_buy

    @allure.step("Place two 'Sell' orders, each with quantity - 350.")
    @automation_logger(logger)
    def test_place_sell_order(self):
        order_response = TestTwoTradesDifferentPrice.seller.postman.get_static_postman(
            TestTwoTradesDifferentPrice.seller_token). \
            order_service.create_order_sync(TestTwoTradesDifferentPrice.order_sell_1)
        assert order_response['error'] is None

        order_response = TestTwoTradesDifferentPrice.seller.postman.get_static_postman(
            TestTwoTradesDifferentPrice.seller_token). \
            order_service.create_order_sync(TestTwoTradesDifferentPrice.order_sell_2)
        assert order_response['error'] is None

    @allure.step("Place the 'Buy' order, quantity - 700.")
    @automation_logger(logger)
    def test_place_buy_order(self):
        order_response = TestTwoTradesDifferentPrice.buyer.postman.get_static_postman(
            TestTwoTradesDifferentPrice.buyer_token). \
            order_service.create_order_sync(TestTwoTradesDifferentPrice.order_buy)
        assert order_response['error'] is None

    @allure.step("Verify balance update after the trade - seller.")
    @automation_logger(logger)
    def test_verify_seller_balance(self):
        time.sleep(WAIT_FOR_TRADE_DELAY)

        seller_balance = TestTwoTradesDifferentPrice.seller.postman.get_static_postman(
            TestTwoTradesDifferentPrice.seller_token). \
            balance_service.get_all_currencies_balance(TestTwoTradesDifferentPrice.seller.customer_id)

        print(seller_balance['result'][base_currency - 1]['balance'])

        # Seller gives away 700 XRP . Half of them are sold for 4 EUR each, and the other half - for 5 EUR each.
        # As a result he acquires 350 x 4 + 350 x 5 = 3150 EUR

        # Seller - EUR
        assert float(seller_balance['result'][quoted_currency - 1]['balance']['total']) == (
                    quantity_sell * price_for_sell_1) + (quantity_sell * price_for_sell_2)
        assert float(seller_balance['result'][quoted_currency - 1]['balance']['available']) == (
                    quantity_sell * price_for_sell_1) + (quantity_sell * price_for_sell_2)

        # After the trade was created the amount of XRP that was sold is deducted from Seller's available and t
        # otal balance. The amount of XRP that is removed from Seller's balance equals to the amount of XRP
        # that was sold - 700, quantity_sell x 2  since 2 "Sell" orders were placed, 350 XRP each

        # Seller - XRP
        assert float(seller_balance['result'][base_currency - 1]['balance']['total']) == 10000 - quantity_sell * 2
        assert float(seller_balance['result'][base_currency - 1]['balance']['available']) == 10000 - quantity_sell * 2

    @allure.step("Verify balance update after the trade - buyer.")
    @automation_logger(logger)
    def test_verify_buyer_balance(self):
        buyer_balance = TestTwoTradesDifferentPrice.buyer.postman.get_static_postman(
            TestTwoTradesDifferentPrice.buyer_token). \
            balance_service.get_all_currencies_balance(TestTwoTradesDifferentPrice.buyer.customer_id)

        # After the trade was created the "Buy" order is filled, Buyer aquires 700 XRP.
        # Since one order matches with two other with different prices two different trades with
        # different prices are created.
        # As a result the following sum is deducted from his account:  350 x 4 + 350 x 5 = 3150 EUR

        # Buyer - EUR
        assert float(buyer_balance['result'][quoted_currency - 1]['balance']['frozen']) == 0
        assert float(buyer_balance['result'][quoted_currency - 1]['balance']['available']) == 10000 - (
                    quantity_sell * price_for_sell_1) - (quantity_sell * price_for_sell_2)

        # After the trade was created the amount of XRP that were bough, 700, are added to Buyer's "available"
        # and "total" balance.

        # Buyer - XRP
        assert float(buyer_balance['result'][base_currency - 1]['balance']['frozen']) == 0
        assert float(buyer_balance['result'][base_currency - 1]['balance']['available']) == quantity_buy

    @allure.step("Restore the original reference price.")
    @automation_logger(logger)
    def test_restore_original_price(self):
        Instruments.set_price_last_trade(instrument_id, TestTwoTradesDifferentPrice.original_last_trade_price)
        Instruments.set_ticker_last_price(instrument_id, TestTwoTradesDifferentPrice.original_ticker_last)

    logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
    print(f"================== TEST CASE PASSED: {test_case}===================")

