import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

"""
    In this test we are testing customer balance update after a trade.
    Buy order was placed, sell order was placed right after, both orders are 100% filled.
    Both customers balance was updated accordingly - the buyer's and the seller's.

    Original test flow:

    1. Clear the Order Book for the selected instrument.
    2. Create two customers and save the tokens.
    3. Add balance for both customers used for this test.
    4. Change current reference price to 'price_for_buy'.
    5. Place the 'Buy' order, quantity - 700.
    6. Place the 'Sell' order, quantity - 700.
    7. Verify balance update after the trade - seller.
    8. Verify balance update after the trade - buyer.
    9. Restore the original reference price.
"""

test_case = "6830"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]
price_for_buy = 5
price_for_sell = price_for_buy
quantity_buy = 700.00

# The parameters below are mandatory to sustain test conditions.
quantity_sell = quantity_buy  # For this test "quantity_sell" must be 100% of "quantity_buy".

WAIT_FOR_TRADE_DELAY = 4


@allure.feature("Order is fully filled - customer's balance update verified.")
@allure.story("Fully filled 'Buy' orders - customer's balance is updated.")
@allure.title("Order is fully filled - customer's balance update verified.")
@allure.description("""
    
    Functional tests.
    1. Verify balance update after the trade - seller.
    2. Verify balance update after the trade - buyer.
    3. Restore the original reference price.
    
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/partially_filled_orders_tests/C6830_filled_buy_100_balance_update_test.py",
                 "TestBuyBalanceUpdated_100")
@pytest.mark.usefixtures("r_customer")
class TestFullyFilled(object):
    # Those class variables are used to save placed orders ID's.
    placed_buy_order_id = ""
    placed_sell_order_id = ""

    buyer = None
    seller = None

    buyer_token = ""
    seller_token = ""

    @allure.step("Verify balance update after the trade - seller.")
    @automation_logger(logger)
    @pytest.mark.parametrize('place_order_buy', [[quantity_buy, price_for_buy]], indirect=True)
    @pytest.mark.parametrize('place_order_sell', [[quantity_sell, price_for_sell]], indirect=True)
    def test_verify_seller_balance(self, r_customer, make_customer, place_order_buy, place_order_sell):
        time.sleep(WAIT_FOR_TRADE_DELAY)

        TestFullyFilled.buyer = make_customer[0]
        TestFullyFilled.buyer_token = make_customer[0].static_token

        TestFullyFilled.seller = make_customer[1]
        TestFullyFilled.seller_token = make_customer[1].static_token

        seller_balance = TestFullyFilled.seller.postman.get_static_postman(TestFullyFilled.seller_token). \
            balance_service.get_all_currencies_balance(TestFullyFilled.seller.customer_id)

        print(seller_balance['result'][base_currency - 1]['balance'])

        # Seller - EUR
        assert float(seller_balance['result'][quoted_currency - 1]['balance']['total']) == quantity_sell * price_for_buy
        assert float(
            seller_balance['result'][quoted_currency - 1]['balance']['available']) == quantity_sell * price_for_buy

        # Seller - XRP
        assert float(seller_balance['result'][base_currency - 1]['balance']['total']) == 10000 - quantity_sell
        assert float(seller_balance['result'][base_currency - 1]['balance']['available']) == 10000 - quantity_sell

    @allure.step("Verify balance update after the trade - buyer.")
    @automation_logger(logger)
    def test_verify_buyer_balance(self):
        buyer_balance = TestFullyFilled.buyer.postman.get_static_postman(TestFullyFilled.buyer_token). \
            balance_service.get_all_currencies_balance(TestFullyFilled.buyer.customer_id)

        # Buyer - EUR
        assert float(buyer_balance['result'][quoted_currency - 1]['balance']['frozen']) == 0
        assert float(
            buyer_balance['result'][quoted_currency - 1]['balance']['total']) == 10000 - quantity_sell * price_for_buy
        assert float(buyer_balance['result'][quoted_currency - 1]['balance'][
                         'available']) == 10000 - quantity_sell * price_for_buy

        # Buyer - XRP
        assert float(buyer_balance['result'][base_currency - 1]['balance']['frozen']) == 0
        assert float(buyer_balance['result'][base_currency - 1]['balance']['available']) == quantity_sell
        assert float(buyer_balance['result'][base_currency - 1]['balance']['total']) == quantity_sell

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
