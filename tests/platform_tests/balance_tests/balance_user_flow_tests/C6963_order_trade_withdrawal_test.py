import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig
from src.base.equipment.trade import Trade


test_case = "6963"

# The parameters below are used for test configuration.
instrument_id = 1014  # XRP/EUR
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)

deposited_sum = 1000

quantity_buy = 40
quantity_sell = 30

withdrawn_sum = 50

DEPOSIT_DELAY = 5
TRADE_PROCESSING_DELAY = 6


@allure.feature("Balance - User Flow.")
@allure.story("User performs several actions, balance verified right after . ")
@allure.title("Balance update after deposit, order, trade and withdrawal.")
@allure.description("""
    Functional tests.

    1. Fill the Buy Order Book.
    2. Perform a deposit and verify balance.
    3. Add 10000 XRP to customer's balance.
    4. Place a Sell order.
    5. Calculating the fees the customer was charged with.
    6. Performing a withdrawal.
    7. Verifying customer's balance after withdrawal.

       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_user_flow_tests/C6963_order_trade_withdrawal_test.py",
                 "Deposit, Order, Trade")
class TestOrderTradeWithdrawal(object):
    """
    This test comes to verify balance update after several actions - deposit, order, trade and withdrawal.
    Also this test comes to verify that Membership and Cumulative fees are deducted from customer's balance.
    The deposit is performed in USD only to trigger the Membership Fee and to enable the Cumulative Fee, that
    will be taken after the trade is performed.

    """

    placed_order_id = ""

    membership_fee_paid = 0

    cumulative_fee_paid = 0

    price = 0

    buy_trade = None

    @allure.step("Fill the Buy Order Book.")
    @automation_logger(logger)
    @pytest.mark.parametrize('make_customer', [[instrument_id]], indirect=True)
    @pytest.mark.parametrize('add_balance_fill', [[quoted_currency, base_currency]], indirect=True)
    @pytest.mark.parametrize('fill_order_book_buy', [[quantity_buy, instrument_id]], indirect=True)
    def test_set_precondition(self, make_customer, add_balance_fill, fill_order_book_buy):
        logger.logger.info("Preconditions were set.")
        print("Preconditions were set.")

    @allure.step("Perform a deposit and verify balance.")
    @automation_logger(logger)
    def test_perform_deposit(self, r_customer_sql):
        r_customer_sql.set_customer_status(3)
        r_customer_sql.add_credit_card_and_deposit(deposited_sum, 1)
        assert r_customer_sql.transactions[0].id

        logger.logger.info(F"Deposit requested - Payment Service resopnse: {r_customer_sql.transactions[0].id}")
        print(F"Deposit requested - Payment Service resopnse: {r_customer_sql.transactions[0].id}")

        time.sleep(DEPOSIT_DELAY)

        balance_response = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id, 1)
        assert float(balance_response['result']['balance']['available']) == deposited_sum

        logger.logger.info(F"The ID of the customer used for this test; {r_customer_sql.customer_id}")

    @allure.step("Add 10000 XRP to customer's balance.")
    @automation_logger(logger)
    def test_add_customer_balance(self, r_customer_sql):
        balance_response = r_customer_sql.postman.balance_service.add_balance(r_customer_sql.customer_id, base_currency,
                                                                              10000)

        assert float(balance_response['result']['balance']['available']) == 10000

    @allure.step("Place a Sell order.")
    @automation_logger(logger)
    def test_place_order(self, r_customer_sql):
        TestOrderTradeWithdrawal.price = Instruments.get_ticker_last_price(instrument_id) * 0.8

        response = r_customer_sql.postman.order_service.create_order_sync(
            Order().set_order(2, instrument_id, quantity_sell, TestOrderTradeWithdrawal.price))
        assert response['error'] is None
        TestOrderTradeWithdrawal.placed_order_id = response['result']['orderId']

        logger.logger.info(f"Sell order ID; {TestOrderTradeWithdrawal.placed_order_id}")
        print(f"Sell order ID; {TestOrderTradeWithdrawal.placed_order_id}")

    @allure.step("Calculating the fees the customer was charged with.")
    @automation_logger(logger)
    def test_calculate_fees_paid(self, r_customer_sql):
        # CUMULATIVE

        # Getting the trade from DB and getting the Cumulative Fee size by Trade ID.
        time.sleep(TRADE_PROCESSING_DELAY)

        buy_trade = Trade.trades_data_converter(
            Instruments.get_trade_by_order_id(TestOrderTradeWithdrawal.placed_order_id))

        TestOrderTradeWithdrawal.cumulative_fee_paid = Instruments.get_cumulative_fee_by_trade(buy_trade[0].id)

        TestOrderTradeWithdrawal.price = buy_trade[0].price

        logger.logger.info(F"Cumulative Fee in EUR: {TestOrderTradeWithdrawal.cumulative_fee_paid}")
        print(F"Cumulative Fee in EUR: {TestOrderTradeWithdrawal.cumulative_fee_paid}")

        # MEMBERSHIP

        # On first deposit the customer is charged with discounted membership fee.
        membership_fee_size = float(Instruments.get_membership_fee_size(2, True))

        TestOrderTradeWithdrawal.membership_fee_paid = round(membership_fee_size, 2)

        logger.logger.info(F"Membership Fee in USD: {TestOrderTradeWithdrawal.membership_fee_paid}")
        print(F"Membership Fee in USD: {TestOrderTradeWithdrawal.membership_fee_paid}")

    @allure.step("Performing a withdrawal.")
    @automation_logger(logger)
    def test_performing_withdrawal(self, r_customer_sql):
        withdrawal_response = r_customer_sql.postman.payment_service.withdrawal_wire(r_customer_sql.bank,
                                                                                     quoted_currency, withdrawn_sum)
        assert withdrawal_response['error'] is None

        logger.logger.info(f"Withdrawal response: {withdrawal_response}")
        print(f"Withdrawal response: {withdrawal_response}")

    @allure.step("Verifying customer's balance after withdrawal.")
    @automation_logger(logger)
    def test_balance_after_withdrawal(self, r_customer_sql):
        # Quoted currency - balance verification:
        quoted_balance_response = r_customer_sql.postman.balance_service.get_currency_balance(
            r_customer_sql.customer_id, quoted_currency)
        quoted_currency_amount = float(quoted_balance_response['result']['balance']['available'])

        # QUOTED CURRENCY => The amount of quoted currency received from "Sell" trade - CUMULATIVE_FEE - WITHDRAWN_SUM
        assert round(quoted_currency_amount + 0.01, 1) == round((float(quantity_sell * TestOrderTradeWithdrawal.price) - float(
            TestOrderTradeWithdrawal.cumulative_fee_paid) - float(withdrawn_sum)), 1)

        # Base currency  - balance verification:
        base_balance_response = r_customer_sql.postman.balance_service.get_currency_balance(
            r_customer_sql.customer_id, base_currency)
        base_currency_amount = float(base_balance_response['result']['balance']['available'])


        # BASE CURRENCY => The initial sum, 10,000 , minus the amount of base currency that was sold.
        assert base_currency_amount == 10000 - quantity_sell

        # USD - verifying Membership Fee was charged.
        usd_balance_response = r_customer_sql.postman.balance_service.get_currency_balance(
            r_customer_sql.customer_id, 1)

        assert float(usd_balance_response['result']['balance'][
                         'available']) == deposited_sum - TestOrderTradeWithdrawal.membership_fee_paid

        logger.logger.info(f"Quoted currency balance: {quoted_currency_amount}, "
                           f"Base currency balance: {base_currency_amount}, USD balance: {usd_balance_response}")
        print(f"Quoted currency balance: {quoted_currency_amount},"
              f" Base currency balance: {base_currency_amount}, USD balance: {usd_balance_response}")


        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
