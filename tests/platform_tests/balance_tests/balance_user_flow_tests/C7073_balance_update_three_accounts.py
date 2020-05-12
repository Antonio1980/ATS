import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig

test_case = "7073"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)

price = 5.0

quantity_sell = 1000

quantity_buy = 100

initial_sum = 1000.0

ORDER_PROCESS_DELAY = 5.0


@allure.feature("Balance - User Flow")
@allure.story("Two trades performed, three accounts are updated.")
@allure.title("Two trades performed, three accounts are updated.")
@allure.description("""
    Functional tests.

    1. Adding balance to seller and both buyers.
    2. Placing orders.
    3. Verifying seller's balance after trade.
    4. Verifying the balance of both buyers after trade.
 
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_user_flow_tests/C7073_balance_update_three_accounts.py ",
                 "Balance update - three accounts")
@pytest.mark.usefixtures("r_customer")
class TestThreeAccounts(object):
    """
    This test comes to verify comes to verify balance update for three accounts.
    Customer named Sue is selling 1000 XRP for 5 EUR each.
    Customers Bill and Barney are buying 100 XRP, each one of them.
    As a result 2 trades are created, Sue acquires 1000 EUR for 200 XRP, 800 XRP remain frozen.
    Bill and Barney acquire 100 XRP each, 500 EUR were paid.

    """

    # Sue
    seller = None

    # Bill
    buyer_1 = None

    # Barney
    buyer_2 = None

    sell_order = Order().set_order(2, instrument_id, quantity_sell, price)

    buy_order_1 = Order().set_order(1, instrument_id, quantity_buy, price)

    buy_order_2 = Order().set_order(1, instrument_id, quantity_buy, price)

    @pytest.mark.parametrize('make_two_customers', [[instrument_id]], indirect=True)
    @allure.step("Adding balance to seller and both buyers.")
    @automation_logger(logger)
    def test_add_balance(self, make_two_customers, r_customer_sql):
        # Seller, Sue
        TestThreeAccounts.seller = r_customer_sql

        # Buyer 1, Bill
        TestThreeAccounts.buyer_1 = make_two_customers[0]

        # Buyer 1, Barney
        TestThreeAccounts.buyer_2 = make_two_customers[1]

        # Adding balance - Seller
        response = TestThreeAccounts.seller.postman.balance_service.add_balance(
            TestThreeAccounts.seller.customer_id, base_currency, initial_sum)
        assert response

        # Adding balance - Bill
        response = TestThreeAccounts.buyer_1.postman.get_static_postman(
            TestThreeAccounts.buyer_1.static_token). \
            balance_service.add_balance(TestThreeAccounts.buyer_1.customer_id, quoted_currency, quantity_buy * price)
        assert response

        # Adding balance - Barney
        response = TestThreeAccounts.buyer_2.postman.get_static_postman(
            TestThreeAccounts.buyer_2.static_token). \
            balance_service.add_balance(TestThreeAccounts.buyer_2.customer_id, quoted_currency, quantity_buy * price)
        assert response

    @allure.step("Placing orders.")
    @automation_logger(logger)
    def test_place_all_orders(self):
        # Placing the "Sell" order
        order_response = TestThreeAccounts.seller.postman.get_static_postman(TestThreeAccounts.seller.auth_token) \
            .order_service.create_order_sync(TestThreeAccounts.sell_order)

        assert order_response['error'] is None

        # Placing the first "Buy" order - Bill
        order_response = TestThreeAccounts.buyer_1.postman.get_static_postman(
            TestThreeAccounts.buyer_1.static_token).order_service.create_order_sync(TestThreeAccounts.buy_order_1)

        print(f"Buyer 1 , Bill, CID: {TestThreeAccounts.buyer_1.customer_id}")

        assert order_response['error'] is None

        # Placing the second "Buy" order - Barney
        order_response = TestThreeAccounts.buyer_2.postman.get_static_postman(
            TestThreeAccounts.buyer_2.static_token).order_service.create_order_sync(TestThreeAccounts.buy_order_2)

        assert order_response['error'] is None

    @allure.step("Verifying seller's balance after trade.")
    @automation_logger(logger)
    def test_seller_balance(self):
        time.sleep(ORDER_PROCESS_DELAY)

        # Sue's balance
        seller_balance = TestThreeAccounts.seller.postman.get_static_postman(
            TestThreeAccounts.seller.auth_token) \
            .balance_service.get_all_currencies_balance(TestThreeAccounts.seller.customer_id)

        logger.logger.info(f"Seller balance: {seller_balance}")
        print(f"Seller balance: {seller_balance}")

        # Seller's balance, EUR:
        assert float(seller_balance['result'][quoted_currency - 1]['balance']['available']) == 2 * quantity_buy * price
        # Seller's balance, XRP:
        assert float(seller_balance['result'][base_currency - 1]['balance']['frozen']) == initial_sum - 2 * quantity_buy

    @allure.step("Verifying the balance of both buyers after trade.")
    @automation_logger(logger)
    def test_verify_buyers_balance(self):
        # Bill's balance
        first_buyer_balance = TestThreeAccounts.seller.postman.get_static_postman(
            TestThreeAccounts.buyer_1.static_token) \
            .balance_service.get_all_currencies_balance(TestThreeAccounts.buyer_1.customer_id)

        logger.logger.info(f"Bill's balance: {first_buyer_balance}")
        print(f"Bill's balance: {first_buyer_balance}")

        # Bill's balance, EUR:
        assert float(first_buyer_balance['result'][quoted_currency - 1]['balance']['available']) == 0
        # Bill's balance, XRP:
        assert float(first_buyer_balance['result'][base_currency - 1]['balance']['available']) == quantity_buy

        # Barney's balance
        second_buyer_balance = TestThreeAccounts.seller.postman.get_static_postman(
            TestThreeAccounts.buyer_2.static_token) \
            .balance_service.get_all_currencies_balance(TestThreeAccounts.buyer_2.customer_id)

        logger.logger.info(f"Barney's balance: {second_buyer_balance}")
        print(f"Barney's balance: {second_buyer_balance}")

        # Barney's balance, EUR:
        assert float(second_buyer_balance['result'][quoted_currency - 1]['balance']['available']) == 0
        # Barney's balance, XRP:
        assert float(second_buyer_balance['result'][base_currency - 1]['balance']['available']) == quantity_buy

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
