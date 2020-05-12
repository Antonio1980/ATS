import time
import allure
import pytest
from src.base import logger
from src.base.instruments import Instruments
from src.base.equipment.order import Order
from src.base.log_decorator import automation_logger
from config_definitions import BaseConfig
from src.base.equipment.trade import Trade

test_case = "7176"

# The parameters below are used for test configuration
instrument_id = 1014  # XRP/EUR
base_currency, quoted_currency = Instruments.get_currency_by_instrument(instrument_id)

alternative_instrument = 1017  # XRP/BTC
alternative_base, alternative_quoted = Instruments.get_currency_by_instrument(alternative_instrument)

quantity_buy = 100
quantity_sell = 100

alternative_buy = 100
alternative_sell = 100

TRADE_PROCESSING_DELAY = 6


@allure.feature("Balance - User Flow")
@allure.story("User performs several actions, balance verified right after ")
@allure.title("Selling BTC for XRP, selling XRP for EUR, withdrawing EUR.")
@allure.description("""
    Functional tests.

    1. Clean the Order Book - alternative instrument.
    2. Fill the Sell Order Book - main instrument.
    3. Fill the Sell Order Book - alternative instrument.
    4. Place  Buy order on alternative instrument, buy XRP for BTC.
    5. XRP acquired - verify customer's balance.
    6. Place Sell order on the main instrument - acquire EUR for XRP.
    7. Verify customer's balance in EUR.
    8. Withdraw half of the EUR the customer has.
    9. Customer's balance final verification.

       """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_user_flow_tests/C7176_sell_buy_withdrawal_test.py",
                 "Sell, Buy and Withdraw.")
class TestSellBuyWithdraw(object):
    """

    Customer has 0.5 BTC and he sells it for another crypto - XRP.
    The received XRP are sold for EUR, and half of them are withdrawn.
    This test comes to verify customer's balance after the full flow is performed.
    In this test customer isn't charged with fees.
    """

    sell_order_id = ""

    withdrawn_sum = 0

    FIAT_balance = 0

    @allure.step("Clean the Order Book - alternative instrument. ")
    @automation_logger(logger)
    def test_clear_alternative(self, r_customer):
        r_customer.clean_instrument(alternative_instrument)

    @allure.step("Fill the Sell Order Book - main instrument.")
    @automation_logger(logger)
    @pytest.mark.parametrize('make_customer', [[instrument_id]], indirect=True)
    @pytest.mark.parametrize('add_balance_fill',
                             [[quoted_currency, base_currency, alternative_base, alternative_quoted]], indirect=True)
    @pytest.mark.parametrize('fill_order_book_buy', [[quantity_buy, instrument_id]], indirect=True)
    def test_set_precondition_main(self, make_customer, add_balance_fill, fill_order_book_buy):
        logger.logger.info(f"Instrument {instrument_id} - Preconditions were set.")
        print(f"Instrument {instrument_id} - Preconditions were set.")

    @allure.step("Fill the Sell Order Book - alternative instrument.")
    @automation_logger(logger)
    @pytest.mark.parametrize('fill_order_book_sell', [[alternative_sell, alternative_instrument]], indirect=True)
    def test_set_precondition_alternative(self, make_customer, add_balance_fill, fill_order_book_sell):
        logger.logger.info(f"Instrument {alternative_instrument} - Preconditions were set.")
        print(f"Instrument {alternative_instrument} - Preconditions were set.")

    @allure.step("Place  Buy order on alternative instrument, buy XRP for BTC.")
    @automation_logger(logger)
    def test_place_buy_order(self, r_customer_sql):
        logger.logger.info(F"Customer ID: {r_customer_sql.customer_id}*")
        print(F"Customer ID: {r_customer_sql.customer_id}*")

        # The customer initially possesses 10 BTC.
        r_customer_sql.postman.balance_service.add_balance(r_customer_sql.customer_id, alternative_quoted, 10)

        price = Instruments.get_ticker_last_price(alternative_instrument)

        # Buying XRP for BTC.
        order_response = r_customer_sql.postman.order_service.create_order_sync(
            Order().set_order(1, alternative_instrument, quantity_buy, price * 1.1))

        assert order_response['error'] is None
        order_id = order_response['result']['orderId']

        logger.logger.info(F"Buy order placed on the instrument {alternative_instrument}, order ID: {order_id}")
        time.sleep(TRADE_PROCESSING_DELAY)

    @allure.step("XRP aquired - verify customer's balance.")
    @automation_logger(logger)
    def test_verify_balance_update(self, r_customer_sql):
        balance_response_base = r_customer_sql.postman. \
            balance_service.get_currency_balance(r_customer_sql.customer_id, alternative_base)

        assert float(balance_response_base['result']['balance']['available']) == float(quantity_buy)

        logger.logger.info(f"XRP balance: {balance_response_base}")
        print(f"XRP balance: {balance_response_base}")

    @allure.step("Place Sell order on the main instrument - acquire EUR for XRP.")
    @automation_logger(logger)
    def test_place_sell_order(self, r_customer_sql):
        price = Instruments.get_ticker_last_price(instrument_id)

        # Selling XRP for EUR.
        order_response = r_customer_sql.postman.order_service.create_order_sync(
            Order().set_order(2, instrument_id, quantity_sell, price * 0.9))

        assert order_response['error'] is None

        TestSellBuyWithdraw.sell_order_id = order_response['result']['orderId']

        logger.logger.info("Placed Sell Order ID: {TestSellBuyWithdraw.sell_order_id}")
        print("Placed Sell Order ID: {TestSellBuyWithdraw.sell_order_id}")

        time.sleep(TRADE_PROCESSING_DELAY)

    @allure.step("Verify customer's balance in EUR.")
    @automation_logger(logger)
    def test_verify_fiat_received(self, r_customer_sql):
        # Finding the trade, using it to get the amount of EUR that was acquired as a result of the trade.
        sell_trade = Trade.trades_data_converter(Instruments.get_trade_by_order_id(TestSellBuyWithdraw.sell_order_id))

        logger.logger.info(f"Trade ID: {sell_trade[0].id}")
        print(f"Trade ID: {sell_trade[0].id}")

        balance_response_quoted = r_customer_sql.postman.balance_service.get_currency_balance(
            r_customer_sql.customer_id, quoted_currency)

        available_fiat = float(balance_response_quoted['result']['balance']['available'])

        # Available balance in EUR after the trade should be: Trade_quantity x Trade_price
        assert float(sell_trade[0].quantity * sell_trade[0].price) == available_fiat

        logger.logger.info(f"FIAT balance before withdrawal: {available_fiat} {base_currency}")
        print(f"FIAT balance before withdrawal: {available_fiat} {base_currency}")

        # Sum that is to be withdrawn
        TestSellBuyWithdraw.withdrawn_sum = round(available_fiat, 2)

        # Current customer's available balance in EUR.
        TestSellBuyWithdraw.FIAT_balance = available_fiat

    @allure.step("Withdraw half of the EUR the customer has.")
    @automation_logger(logger)
    def test_performing_withdrawal(self, r_customer_sql):
        withdrawal_response = r_customer_sql. \
            postman.payment_service.withdrawal_wire(
              r_customer_sql.bank, quoted_currency, TestSellBuyWithdraw.withdrawn_sum)

        assert withdrawal_response['error'] is None

        logger.logger.info(f"Withdrawal response: {withdrawal_response}")
        print(f"Withdrawal response: {withdrawal_response}")

    @allure.step("Customer's balance final verification.")
    @automation_logger(logger)
    def test_verify_final_balance(self, r_customer_sql):
        balance_response_quoted = r_customer_sql.postman.balance_service.get_currency_balance(
            r_customer_sql.customer_id, quoted_currency)

        logger.logger.info(f"Balance after withdrawal: {balance_response_quoted}")
        print(f"Balance after withdrawal: {balance_response_quoted}")

        # Available balance in EUR after the trade should be: Trade_quantity x Trade_price - Withdrawn Sum
        assert float(balance_response_quoted['result']['balance']['available']) == round(
            (TestSellBuyWithdraw.FIAT_balance - TestSellBuyWithdraw.withdrawn_sum), 2)

        logger.logger.info(f"================== TEST CASE PASSED: {test_case}===================")
        print(f"================== TEST CASE PASSED: {test_case}===================")
