import allure
import pytest
from config_definitions import BaseConfig
from src.base import logger
from src.base.log_decorator import automation_logger

test_case = "5705"
quoted_currency_id = 2
base_currency_id = 3
instrument_id = 1012


@allure.feature('Fee')
@allure.description("""
    Cumulative Fee and Balance Updated after Sell trade, API test
    Pre-condition:
    1)Set Cumulative Fee parameter in DB (Fee = 0.05)
    2)Restart Cumulative Pods in Kubernetes
    3)Add first deposit.
    4)Add Balance (Base Currency)
    5)Get all balance before trade (Quoted Currency)
    6)Generate Sell Trade
    Test:
    1)Get all balance after trade (Quoted Currency)
    2)Verify Cumulative Fee after Trade Buy. Calculation: available_quoted_before + (price*amount)- Fee
    3)Verify that Available and Total Balance are equal, Frozen Balance is 0.00
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Cumulative Fee - Balance Update, "Sell".')
@allure.testcase(
    BaseConfig.GITLAB_URL + "/fees_tests/cumulative_fees_tests/C5705_cumulative_fee_balance_update_sell_test.py",
    "TestCumulativeFeeBalanceUpdateSellTest")
@pytest.mark.fee
@pytest.mark.cumulative_fee
@pytest.mark.usefixtures("r_time_count", "r_customer", "set_cumulative_fee_first_step",)
class TestCumulativeFeeBalanceUpdateTest(object):

    @allure.step("Starting with: test_cumulative_fee_balance_update_sell_test")
    @automation_logger(logger)
    @pytest.mark.parametrize("precondition_cumulative", [[quoted_currency_id, base_currency_id, instrument_id]],
                             indirect=True)
    def test_cumulative_fee_balance_update_sell_test(self, r_customer, precondition_cumulative):
        r_customer_sql = r_customer
        available_before = precondition_cumulative['balance']['available_quoted_before']
        balance = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id,
                                                                              quoted_currency_id)
        total_after_fee = float(balance['result']['balance']['total'])
        frozen_after_fee = float(balance['result']['balance']['frozen'])
        available_after_fee = float(balance['result']['balance']['available'])
        amount = precondition_cumulative['amount']
        price = precondition_cumulative['price']
        a = total_after_fee
        b = available_before + (price*amount) - 0.05
        assert total_after_fee == available_before + (price*amount) - 0.05
        assert available_after_fee == total_after_fee
        assert frozen_after_fee == 0.0
        logger.logger.info(f"================== TEST CASE IS PASSED: {test_case}===================")
