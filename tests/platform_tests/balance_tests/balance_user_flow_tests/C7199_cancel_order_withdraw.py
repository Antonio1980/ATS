import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "7199"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)

quantity_buy = 100

price_buy = Instruments.get_ticker_last_price(instrument_id)

balance_added = quantity_buy * price_buy

TRADE_CANCELLATION_DELAY = 6

BALANCE_UPDATE_DELAY = 5


@allure.feature("Balance - User Flow.")
@allure.story("Balance is unfrozen when the order is cancelled, the sum can be withdrawn.")
@allure.title("Balance is unfrozen when the order is cancelled, the sum can be withdrawn.")
@allure.description("""
    Functional tests.

    1. Place a 'Buy' order.
    2. Cancel the order, verify balance.
    3. Perform a withdrawal.
    
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_user_flow_tests/C7199_cancel_order_withdraw.py",
                 "Place order, cancel and Withdraw.")
class TestPlaceCancelWithdraw(object):
    """

    In this test customer places a "Buy" order, cancels it and withdraws all the quoted currency he possesses.
    This test comes to verify, that the frozen sum is unfrozen when the order is cancelled and that sum
    can be withdrawn.

    """

    buy_order = Order().set_order(1, instrument_id, quantity_buy, price_buy)

    placed_order_id = None

    @allure.step("Update customer balance and place a 'Buy' order.")
    @automation_logger(logger)
    def test_place_order(self, r_customer_sql):
        r_customer_sql.clean_instrument(instrument_id)
        r_customer_sql.clean_up_customer()

        balance_response = r_customer_sql.postman.balance_service.add_balance(r_customer_sql.customer_id,
                                                                              quoted_currency, balance_added)
        order_response = r_customer_sql.postman.order_service.create_order_sync(TestPlaceCancelWithdraw.buy_order)
        assert order_response['error'] is None

        TestPlaceCancelWithdraw.placed_order_id = order_response['result']['orderId']

        logger.logger.info(f"Balance response: {balance_response}")
        logger.logger.info(f"Order response: {order_response}")

    @allure.step("Cancel the order, verify balance.")
    @automation_logger(logger)
    def test_cancel_order(self, r_customer_sql):
        time.sleep(TRADE_CANCELLATION_DELAY)

        cancel_response = r_customer_sql.postman.order_service.cancel_order(TestPlaceCancelWithdraw.placed_order_id)

        time.sleep(BALANCE_UPDATE_DELAY)

        logger.logger.info(f"Order cancellation response: {cancel_response}")
        print(f"Order cancellation response: {cancel_response}")

        balance_response = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id,
                                                                                       quoted_currency)
        assert float(balance_response['result']['balance']['available']) == balance_added
        assert float(balance_response['result']['balance']['frozen']) == 0

    @allure.step("Perform a withdrawal.")
    @automation_logger(logger)
    def test_perform_withdrawal(self, r_customer_sql):
        withdrawal_response = r_customer_sql.postman.payment_service.withdrawal_wire(r_customer_sql.bank,
                                                                                     quoted_currency, balance_added)
        assert withdrawal_response['error'] is None
        withdrawal_token = withdrawal_response['result']['token']

        assert len(withdrawal_token) > 0

        balance_response = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id,
                                                                                       quoted_currency)
        assert float(balance_response['result']['balance']['frozen']) == balance_added
        assert float(balance_response['result']['balance']['available']) == 0

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
