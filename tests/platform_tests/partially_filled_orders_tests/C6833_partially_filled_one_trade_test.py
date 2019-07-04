import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig
from src.base.equipment.trade import Trade

"""
    In this test a Buy order and a Sell order are placed by 2 different customers.
    The orders are match and a trade is created. The trade is splitted to "Buy" and "Sell" trade.
    Buy order quantity is 700, Sell order quantity is 70, Buy order is partially filled.

    Original test flow:

    1. Clear the Order Book for the selected instrument.
    2. Clear the balance of the customer used for this test, cancel all orders.
    3. Add funds to customer's available balance and verify.
    4. Change current reference price to 'price_for_buy' .
    5. Place the "Buy" order - quantity 700.
    6. Place the "Sell" order - quantity 70.
    7. Restore the original last trade  price and ticker last.
    8. Verify the 'Sell' trade and it's parameters.
    9. Verify the 'Buy' trade and it's parameters.
"""

test_case = "6833"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]

price_for_buy = 5
price_for_sell = price_for_buy
quantity_buy = 700.00

# The parameters below are mandatory to sustain test conditions.
quantity_sell = quantity_buy / 10

PROCESSING_ORDERS_DELAY = 6


@allure.feature("Order is 10% filled - one trade is created and splitted to 'Buy' and 'Sell'.")
@allure.story("Trade is created when order is partially filled.")
@allure.title("End-to-End flow verification")
@allure.description("""
    Functional tests.
   
    1. Verify the 'Sell' trade and it's parameters.
    2. Verify the 'Buy' trade and it's parameters.
    
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/partially_filled_orders_tests/C6833_one_trade_created_test.py",
                 "TestPartiallyFilled_TradeCreated")
@pytest.mark.usefixtures("r_customer")
class TestOneTradeCreated(object):
    buyer = None

    seller = None

    @allure.step("Verify the 'Sell' trade and it's parameters.")
    @automation_logger(logger)
    @pytest.mark.parametrize('place_order_buy', [[quantity_buy, price_for_buy]], indirect=True)
    @pytest.mark.parametrize('place_order_sell', [[quantity_sell, price_for_sell]], indirect=True)
    def test_verify_sell_trade_in_db(self, r_customer, make_customer, place_order_buy, place_order_sell):
        time.sleep(PROCESSING_ORDERS_DELAY)

        TestOneTradeCreated.buyer = make_customer[0]

        TestOneTradeCreated.seller = make_customer[1]

        # Bringing trades from MySQL DB.
        sell_trade = Trade.trades_data_converter(Instruments.get_trade_by_order_id(place_order_sell.internal_id))

        # Verifying "Sell" trade quantity  and price.
        assert len(sell_trade) == 1
        assert sell_trade[0].direction == "sell"
        assert sell_trade[0].price == price_for_sell
        assert sell_trade[0].quantity == quantity_sell
        assert str(sell_trade[0].customer_id) == TestOneTradeCreated.seller.customer_id

    @allure.step("Verify the 'Buy' trade and it's parameters.")
    @automation_logger(logger)
    def test_verify_buy_trade_in_db(self, r_customer, make_customer, place_order_buy, place_order_sell):
        # Bringing trades from MySQL DB.
        buy_trade = Trade.trades_data_converter(
            Instruments.get_trade_by_order_id(place_order_buy.internal_id))

        # Verifying "Buy" trade quantity and price.
        assert len(buy_trade) == 1
        assert buy_trade[0].direction == "buy"
        assert buy_trade[0].price == price_for_buy
        assert str(buy_trade[0].customer_id) == TestOneTradeCreated.buyer.customer_id

        # Please note - "Buy" order is only partially filled, 70 XRP out of 700 XRP were bough. Trade quantity - 70 XRP.
        assert buy_trade[0].quantity == quantity_sell

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
