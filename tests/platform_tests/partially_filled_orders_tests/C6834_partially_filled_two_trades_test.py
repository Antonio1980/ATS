import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig
from src.base.equipment.trade import Trade

"""
    In this test one Buy order and two Sell orders are placed.
    Buy order quantity - 700; Sell orders quantities - 70 and 420.
    Buy order is partially filled, two trades are created.
    The created trades are splitted, as a result we have 2 Buy and 2 Sell trades.
    Price, quantity and direction are verified for each trade.

    Original test flow:

    1. Clear the Order Book for the selected instrument.
    2. Clear the balance of the customer used for this test, cancel all orders
    3. Add funds to customer's available balance and verify
    4. Change current reference price to 'price_for_buy'.
    5. Place the Buy order, quantity - 700.
    6. Place the Sell_10 order, quantity - 70.
    7. Place the Sell_60 order, quantity - 420.
    8. Restore the original last trade  price and ticker last.
    9. Two 'Sell' trades are created - trade parameters verification.
    10. Two 'Buy' trades are created - trade parameters verification.
    11. Verify 'Buy' order parameters in DB.
"""

test_case = "6834"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]

price_for_buy = 5
price_for_sell = price_for_buy
quantity_buy = 700.00

# The parameters below are mandatory to sustain test conditions.
quantity_sell_10 = quantity_buy * 0.1
quantity_sell_60 = quantity_buy * 0.6

PROCESSING_ORDERS_DELAY = 6


@allure.feature("Order is 70% filled - two trades are created and splitted to 'Buy' and 'Sell'. ")
@allure.story("Trade is created when order is partially filled. ")
@allure.title("Order is 70% filled - two trades are created and splitted to 'Buy' and 'Sell'. ")
@allure.description("""
    Functional tests.
    
    1. Two 'Sell' trades are created - trade parameters verification.
    2. Two 'Buy' trades are created - trade parameters verification.
    3. Verify 'Buy' order parameters in DB. 
    
  """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/partially_filled_orders_tests/C6834_partially_filled_two_trades_test.py",
                 "TestPartiallyFilled_TwoTrades")
@pytest.mark.usefixtures("r_customer")
class TestTwoTradesCreated(object):

    @allure.step("Two 'Sell' trades are created - trade parameters verification")
    @automation_logger(logger)
    @pytest.mark.parametrize('place_order_buy', [[quantity_buy, price_for_buy]], indirect=True)
    @pytest.mark.parametrize(
        'place_two_sell_orders', [[quantity_sell_10, quantity_sell_60, price_for_sell, price_for_sell]], indirect=True)
    def test_verify_sell_trade_in_db(self, r_customer, make_customer, place_order_buy, place_two_sell_orders):
        time.sleep(PROCESSING_ORDERS_DELAY)

        # Bringing "Sell" trade from MySQL DB - 70 XRP were sold.
        sell_trade_10 = Trade.trades_data_converter(
            Instruments.get_trade_by_order_id(place_two_sell_orders[0].internal_id))

        # Verifying "Sell" trade quantity and price.
        assert len(sell_trade_10) == 1
        assert sell_trade_10[0].direction == "sell"
        assert sell_trade_10[0].price == price_for_sell
        assert sell_trade_10[0].quantity == quantity_sell_10

        # Bringing "Sell" trade from MySQL DB - 420 XRP were sold.
        sell_trade_60 = Trade.trades_data_converter(
            Instruments.get_trade_by_order_id(place_two_sell_orders[1].internal_id))

        # Verifying "Sell" trade quantity and price.
        assert len(sell_trade_60) == 1
        assert sell_trade_60[0].direction == "sell"
        assert sell_trade_60[0].price == price_for_sell
        assert sell_trade_60[0].quantity == quantity_sell_60

    @allure.step("Two 'Buy' trades are created - trade parameters verification")
    @automation_logger(logger)
    def test_verify_buy_trade_in_db(self, r_customer, make_customer, place_order_buy, place_two_sell_orders):
        # Bringing trades from MySQL DB.
        buy_trades = Trade.trades_data_converter(
            Instruments.get_trade_by_order_id(place_order_buy.internal_id))

        # Verifying "Buy" trade quantity and price.
        assert len(buy_trades) == 2

        # Verifying the first "Buy" trade - 70 XRP were bough.
        assert buy_trades[0].direction == "buy"
        assert buy_trades[0].price == price_for_buy
        assert buy_trades[0].quantity == quantity_sell_10

        # Verifying the second "Buy" trade - 420 XRP were bough.
        assert buy_trades[1].direction == "buy"
        assert buy_trades[1].price == price_for_buy
        assert buy_trades[1].quantity == quantity_sell_60

    @allure.step("Verify 'Buy' order parameters in DB")
    @automation_logger(logger)
    def test_verify_buy_order_in_db(self, r_customer, make_customer, place_order_buy, place_two_sell_orders):
        buy_order_in_db = Order.orders_data_converter(
            Instruments.get_order_by_id(place_order_buy.internal_id))

        assert len(buy_order_in_db) == 1
        assert buy_order_in_db[0].quantity == place_order_buy.quantity

        # "Buy" order has matched with both "Sell" orders. Filled quantity must be updated accordingly.
        assert buy_order_in_db[0].filled_quantity == quantity_sell_10 + quantity_sell_60

        logger.logger.info(f"================== TEST CASE IS PASSED {test_case} ===================")
        print(f"================== TEST CASE IS PASSED {test_case} ===================")
