import allure
import pytest
from config_definitions import BaseConfig
from src.base import logger
from src.base.log_decorator import automation_logger

test_case = "6141"
quoted_currency_id = 2
base_currency_id = 3
instrument_id = 1012


@allure.feature('Fee')
@allure.description("""
    Cumulative Fee and Balance Updated after Buy trade, API test
    Pre-condition:
    1)Set Cumulative Fee parameter in DB (Fee = 0.05)
    2)Restart Cumulative Pods in Kubernetes
    3)Add first deposit.
    4)Add Balance (Quoted Currency)
    5)Get all balance before trade (Base Currency)
    6)Generate Buy Trade
    Test:
    1)Get all balance after trade (Base Currency)
    2)Verify Cumulative Fee after Trade Buy. Calculation: available_base_before + amount - (amount*Fee)
    3)Verify that Available and Total Balance are equal, Frozen Balance is 0.00
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Cumulative Fee - Balance Update, "Buy".')
@allure.testcase(
    BaseConfig.GITLAB_URL + "/fees_tests/cumulative_fees_tests/C6141_cumulative_fee_balance_update_buy_test.py",
    "TestCumulativeFeeBalanceUpdateBuyTest")
@pytest.mark.fee
@pytest.mark.cumulative_fee
@pytest.mark.usefixtures("r_time_count", "r_customer_sql", "set_cumulative_fee_first_step",)
class TestCumulativeFeeBalanceUpdateTest(object):

    @allure.step("Starting with: test_cumulative_fee_balance_update_buy_test")
    @automation_logger(logger)
    @pytest.mark.parametrize("precondition_cumulative", [[quoted_currency_id, base_currency_id, instrument_id]],
                             indirect=True)
    def test_cumulative_fee_balance_update_buy_test(self, r_customer_sql, precondition_cumulative):
        available_before = precondition_cumulative['balance']['available_base_before']
        balance = r_customer_sql.postman.balance_service.get_currency_balance(r_customer_sql.customer_id,
                                                                              base_currency_id)
        total_after_fee = float(balance['result']['balance']['total'])
        frozen_after_fee = float(balance['result']['balance']['frozen'])
        available_after_fee = float(balance['result']['balance']['available'])
        amount = precondition_cumulative['amount']

        assert total_after_fee == available_before + amount - (amount * 0.05)
        assert available_after_fee == total_after_fee
        assert frozen_after_fee == 0.0
        logger.logger.info(f"================== TEST CASE IS PASSED: {test_case}===================")
