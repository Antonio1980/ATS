import time
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.equipment.trade import Trade
from src.base.instruments import Instruments
from src.base.utils.calculator import Calculator
from src.base.log_decorator import automation_logger

test_case = "trade_verification_hurl_test"

# In this test we are placing two orders: Buy and Sell.
# Sell order quantity is half of Buy order quantity.
# Price is the same price.
# After both orders are placed Buy order is partially filled, Sell order is fully filled,
# and a TRADE is created and splitted to "Buy" and "Sell" trades.
# Trade parameters that are saved in DB are verified.


# Original test flow:
# """
#     Functional tests.
#     1. Clear the balance of the customer used for this test, cancel all orders.
#     2. Add funds to customer's available balance and verify.
#     3. Change the current reference price to the BUY_PRICE
#     4. Place the Buy order.
#     5. Place the Sell order.
#     6. Restore the original last trade  price and ticker last.
#     7. Verify the 'Buy' trade and it's parameters.
#     8. Verify the 'Sell' trade and it's parameters.
#     """

# The parameters below are used for test configuration
instrument_id = 1014
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]
price_for_buy = 5.0
quantity_buy = 144.0
quantity_sell = quantity_buy * 0.5


@pytest.mark.incremental
@allure.feature("Trade Parameters Verification - end to end test.")
@allure.story("Trade is created when two orders are matched and saved in MySQL DB")
@allure.title("End-to-End flow verification")
@allure.description("""
    Functional tests.
    1. Verify the 'Buy' trade and it's parameters.
    2. Verify the 'Sell' trade and it's parameters.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.testcase(BaseConfig.GITLAB_URL + "/hurl_tests/trade_verification_hurl_test.py",
                 "TestFullFlow_trade_verification")
@pytest.mark.usefixtures("r_customer")
class TestTradeVerification(object):

    @allure.step("Verify the 'Buy' trade and it's parameters.")
    @automation_logger(logger)
    @pytest.mark.parametrize('filled_quantity_hurl_order_buy', [[instrument_id, quantity_buy, price_for_buy]],
                             indirect=True)
    @pytest.mark.parametrize('filled_quantity_hurl_order_sell', [[instrument_id, quantity_sell, price_for_buy]],
                             indirect=True)
    def test_verify_buy_trade(self, r_customer, create_customer, filled_quantity_hurl_order_buy,
                              filled_quantity_hurl_order_sell):
        # Wait for the orders to be processed and saved in DB.
        time.sleep(5)

        buy_trade = Trade.trades_data_converter(
            Instruments.get_trade_by_order_id(filled_quantity_hurl_order_buy.internal_id))

        assert len(buy_trade) == 1

        assert buy_trade[0].direction == "buy"
        assert buy_trade[0].customer_id == r_customer.customer_id
        assert buy_trade[0].instrument_id == instrument_id

        assert str(buy_trade[0].orderId) == str(filled_quantity_hurl_order_buy.internal_id)

        assert buy_trade[0].price == price_for_buy
        assert buy_trade[0].quantity == quantity_sell
        assert buy_trade[0].status_id == 1

        # Taking rates from Obligation Service to verify "Rate USD Base" field.
        rate = r_customer.postman.obligation_service.convert_rate(base_currency, 1)
        assert buy_trade[0].rate_usd_base == Calculator.value_decimal(rate['result']['rates'][str(base_currency)])

        # Taking rates from Obligation Service to verify "Rate DXEX Base" field.
        rate = r_customer.postman.obligation_service.convert_rate(base_currency, 8)
        assert float(buy_trade[0].rate_dxex_base) == float(
            Calculator.value_decimal(rate['result']['rates'][str(base_currency)]))

    @allure.step("Verify the 'Sell' trade and it's parameters.")
    @automation_logger(logger)
    def test_verify_sell_trade(self, r_customer, filled_quantity_hurl_order_buy, filled_quantity_hurl_order_sell):
        sell_trade = Trade.trades_data_converter(
            Instruments.get_trade_by_order_id(filled_quantity_hurl_order_sell.internal_id))

        assert len(sell_trade) == 1

        assert sell_trade[0].direction == "sell"
        assert sell_trade[0].customer_id == r_customer.customer_id
        assert sell_trade[0].instrument_id == instrument_id

        assert str(sell_trade[0].orderId) == str(filled_quantity_hurl_order_sell.internal_id)

        assert sell_trade[0].price == price_for_buy
        assert sell_trade[0].quantity == quantity_sell
        assert sell_trade[0].status_id == 1

        # Taking rates from Obligation Service to verify "Rate USD Base" field.
        rate = r_customer.postman.obligation_service.convert_rate(base_currency, 1)
        assert sell_trade[0].rate_usd_base == Calculator.value_decimal(rate['result']['rates'][str(base_currency)])

        # Taking rates from Obligation Service to verify "Rate DXEX Base" field.
        rate = r_customer.postman.obligation_service.convert_rate(base_currency, 8)
        assert float(sell_trade[0].rate_dxex_base) == float(
            Calculator.value_decimal(rate['result']['rates'][str(base_currency)]))

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
