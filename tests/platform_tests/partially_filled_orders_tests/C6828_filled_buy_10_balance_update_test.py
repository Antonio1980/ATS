import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

"""
    In this test we are testing customer balance update after a trade.
    The trade was performed after "Buy" order was partially filled - 10%.
    Both customers balance was updated accordingly - the buyer's and the seller's.

    Original test flow:

    1. Clear the Order Book for the selected instrument.
    2. Create two customers and save the tokens.
    3. Add balance for both customers used for this test.
    4. Change current reference price to 'price_for_buy'.
    5. Place the 'Buy' order, quantity - 700.
    6. Place the 'Sell' order, quantity - 70.
    7. Verify balance update after the trade - seller.
    8. Verify balance update after the trade - buyer.
"""

test_case = "6828"

# In this test we are testing customer balance update after a trade.
# The trade was performed after an order was partially filled - 10%.
# Both customers balance was updated accordingly - the buyer's and the seller's.


# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
quoted_currency = Instruments.get_currency_by_instrument(instrument_id)[1]
base_currency = Instruments.get_currency_by_instrument(instrument_id)[0]
price_for_buy = 5.0
price_for_sell = price_for_buy
quantity_buy = 700.00

# The parameters below are mandatory to sustain test conditions.
quantity_sell = quantity_buy / 10  # For this test "quantity_sell" must be 10% of "quantity_buy".

WAIT_FOR_TRADE_DELAY = 5


@allure.feature("Order is 10% filled - customer's balance update verified.")
@allure.story("Partially filled orders - customer's balance update.")
@allure.title("Order is 10% filled - customer's balance update verified.")
@allure.description("""
     
    1. Verify balance update after the trade - seller.
    2. Verify balance update after the trade - buyer.
    
       """)
@pytest.mark.incremental
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/partially_filled_orders_tests/C6828_filled_10_balance_update_test.py",
                 "TestBalanceUpdated_10")
@pytest.mark.usefixtures("r_customer")
class TestTenFilled(object):
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

        TestTenFilled.buyer = make_customer[0]
        TestTenFilled.buyer_token = make_customer[0].static_token

        TestTenFilled.seller = make_customer[1]
        TestTenFilled.seller_token = make_customer[1].static_token

        seller_balance = TestTenFilled.seller.postman.get_static_postman(TestTenFilled.seller_token). \
            balance_service.get_all_currencies_balance(TestTenFilled.seller.customer_id)

        logger.logger.info(f"Seller's balance: {seller_balance['result'][base_currency - 1]['balance']}")
        print(seller_balance['result'][base_currency - 1]['balance'])

        # After the trade was created the amount of EUR that was received following the trade is added to Seller's
        # total and available balance. Amount of EUR received : 70 x 5 => quantity_sell * price_for_buy

        # Seller - EUR
        assert float(seller_balance['result'][quoted_currency - 1]['balance']['total']) == quantity_sell * price_for_buy
        assert float(
            seller_balance['result'][quoted_currency - 1]['balance']['available']) == quantity_sell * price_for_buy

        # After the trade was created the amount of XRP that was sold is deducted from Seller's available and total
        # balance. The amount of XRP that is removed from Seller's balance equals to the amount of XRP that was sold
        # - 70, quantity_sell

        # Seller - XRP
        assert float(seller_balance['result'][base_currency - 1]['balance']['total']) == 10000 - quantity_sell
        assert float(seller_balance['result'][base_currency - 1]['balance']['available']) == 10000 - quantity_sell

    @allure.step("Verify balance update after the trade - buyer.")
    @automation_logger(logger)
    def test_verify_buyer_balance(self):
        buyer_balance = TestTenFilled.buyer.postman.get_static_postman(TestTenFilled.buyer_token). \
            balance_service.get_all_currencies_balance(TestTenFilled.buyer.customer_id)

        # After the trade was created the "Buy" order is 90% filled, as a result 90% of Buyer's balance in EUR that
        # was frozen remains frozen: quantity_buy * price_for_buy * 0.9 = > 700 x 5 x 0.9 = 3150 Since Buyer has
        # managed to buy 70 XRP after all, their price is reduced from "total" : 10000 - 70 x 5 =  9650

        # Buyer - EUR
        assert float(
            buyer_balance['result'][quoted_currency - 1]['balance']['frozen']) == quantity_buy * price_for_buy * 0.9
        assert float(
            buyer_balance['result'][quoted_currency - 1]['balance']['total']) == 10000 - quantity_sell * price_for_buy
        assert float(buyer_balance['result'][quoted_currency - 1]['balance'][
                         'available']) == 10000 - quantity_sell * price_for_buy - quantity_buy * price_for_buy * 0.9

        # After the trade was created the amount of XRP that were bough are added to Buyer's "available" and "total"
        # balance.

        # Buyer - XRP
        assert float(buyer_balance['result'][base_currency - 1]['balance']['frozen']) == 0
        assert float(buyer_balance['result'][base_currency - 1]['balance']['available']) == quantity_sell
        assert float(buyer_balance['result'][base_currency - 1]['balance']['total']) == quantity_sell

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
