import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig
from src.base.equipment.trade import Trade
from src.base.utils.calculator import Calculator

test_case = "6962"

# This test comes to verify balance update after several actions - deposit, order and trade.


# The parameters below are used for test configuration.
instrument_id = 1014  # XRP/EUR
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)

deposited_sum = 10000

quantity_buy = 30
quantity_sell = 20

DEPOSIT_DELAY = 5
TRADE_PROCESSING_DELAY = 6


@allure.feature("Balance - User Flow")
@allure.story("User performs several actions, balance verified right after ")
@allure.title("Balance update after deposit, order and trade")
@allure.description("""
    Functional tests.
    
    1. Fill the Sell Order Book.
    2. Perform a deposit and verify balance.
    3. Place a Buy order.
    4. Calculating the fees the customer was charged with.
    5. Verify balance update after trade.
    
       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_user_flow_tests/C6962_deposit_order_trade_test.py",
                 "Deposit, Order, Trade")
class TestDepositOrderTrade(object):
    """
    This test comes to verify balance update after several actions - deposit, order and trade.
    Customer is charged with Membership Fee on his first deposit - verifying balance is updating accordingly.
    If customer is charged with Cumulative Fee this test verifies that his balance is updated.
    """

    placed_order_id = ""

    membership_fee_paid = 0

    cumulative_fee_paid = 0

    @allure.step("Fill the Sell Order Book")
    @automation_logger(logger)
    @pytest.mark.parametrize('make_customer', [[instrument_id]], indirect=True)
    @pytest.mark.parametrize('add_balance_fill', [[quoted_currency, base_currency]], indirect=True)
    @pytest.mark.parametrize('fill_order_book_sell', [[quantity_sell, instrument_id]], indirect=True)
    def test_set_precondition(self,  make_customer, add_balance_fill, fill_order_book_sell):
        logger.logger.info("Preconditions were set.")
        print("Preconditions were set.")

    @allure.step("Perform a deposit and verify balance")
    @automation_logger(logger)
    def test_perform_deposit(self, r_customer_sql):
        r_customer_sql.set_customer_status(3)
        r_customer_sql.add_credit_card_and_deposit(deposited_sum, quoted_currency)
        assert r_customer_sql.transactions[0].id

        logger.logger.info(F"Deposit requested - Payment Service resopnse: {r_customer_sql.transactions[0].id}")
        print(F"Deposit requested - Payment Service resopnse: {r_customer_sql.transactions[0].id}")

        time.sleep(DEPOSIT_DELAY)

        balance_response = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id,
                                                                                       quoted_currency)
        assert float(balance_response['result']['balance']['available']) == deposited_sum

    @allure.step("Place a Buy order.")
    @automation_logger(logger)
    def test_place_order(self, r_customer_sql):
        logger.logger.info(f"Customer ID: {r_customer_sql.customer_id}")
        print(f"Customer ID: {r_customer_sql.customer_id}")

        price = Instruments.get_ticker_last_price(instrument_id) * 1.5

        response = r_customer_sql.postman.order_service.create_order_sync(
            Order().set_order(1, instrument_id, quantity_sell, price))
        assert response['error'] is None
        TestDepositOrderTrade.placed_order_id = response['result']['orderId']

        logger.logger.info(f"Placed order ID: {response['result']['orderId']}")
        print(f"Placed order ID: {response['result']['orderId']}")

    @allure.step("Calculating the fees the customer was charged with")
    @automation_logger(logger)
    def test_calculate_fees_paid(self, r_customer_sql):
        # CUMULATIVE

        # Getting the trade from DB and getting the Cumulative Fee size by Trade ID.
        time.sleep(TRADE_PROCESSING_DELAY)

        buy_trade = Trade.trades_data_converter(
            Instruments.get_trade_by_order_id(TestDepositOrderTrade.placed_order_id))

        TestDepositOrderTrade.cumulative_fee_paid = Instruments.get_cumulative_fee_by_trade(buy_trade[0].id)

        logger.logger.info(F"Cumulative Fee in XRP: {TestDepositOrderTrade.cumulative_fee_paid}")
        print(F"Cumulative Fee in XRP: {TestDepositOrderTrade.cumulative_fee_paid}")

        # MEMBERSHIP

        # On first deposit the customer is charged with discounted membership fee.
        membership_fee_size = float(Instruments.get_membership_fee_size(2, True))
        rate = r_customer_sql.postman.obligation_service.convert_rate(quoted_currency, 1)
        conversion_rate = Calculator.value_decimal(rate['result']['rates'][str(quoted_currency)])
        # Fee is always rounded up in our system
        TestDepositOrderTrade.membership_fee_paid = round((membership_fee_size / conversion_rate) + 0.01, 2)

        logger.logger.info(F"Membership Fee in USD: {TestDepositOrderTrade.membership_fee_paid}")
        print(F"Membership Fee in USD: {TestDepositOrderTrade.membership_fee_paid}")

    @allure.step("Verify balance update after trade.")
    @automation_logger(logger)
    def test_verify_balance_update(self, r_customer_sql):
        buy_trade = Trade.trades_data_converter(
            Instruments.get_trade_by_order_id(TestDepositOrderTrade.placed_order_id))

        balance_response_base = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id,
                                                                                            base_currency)

        # Final customer balance (base currency) is TRADE_QUANTIY - - CUMULATIVE_FEE
        assert float(balance_response_base['result']['balance']['available']) == float(
            buy_trade[0].quantity - TestDepositOrderTrade.cumulative_fee_paid)

        balance_response_quoted = r_customer_sql.postman.balance_service.get_currency_balance(
            r_customer_sql.customer_id, quoted_currency)

        # Final customer balance (quoted currency) is DEPOSITED_SUM - TRADE_QUANTITY x TRADE_PRICE - MEMBERSHIP_FEE

        assert round(float(balance_response_quoted['result']['balance']['available']),1) == round((float(
            deposited_sum - buy_trade[0].quantity * buy_trade[0].price) - TestDepositOrderTrade.membership_fee_paid), 1)

        # Adding 0.01 before rounding because our system rounds up by default.

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
