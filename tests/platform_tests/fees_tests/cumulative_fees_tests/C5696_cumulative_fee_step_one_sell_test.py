import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger

test_case = "5696"
quoted_currency_id = 2
base_currency_id = 3
instrument_id = 1012


@allure.feature('Fee')
@allure.description("""
    Cumulative Fee Step One, Sell trade, API test
    Pre-condition:
    1)Set Cumulative Fee parameter in DB (Fee = 0.05)
    2)Restart Cumulative Pods in Kubernetes
    3)Add first deposit.
    4)Add Balance (Base Currency)
    5)Generate Sell Trade
    Test:
    1)Calculate Cumulative Fee. Calculation: (price*amount)- Fee
    2)Get feeAmount from DB 
    3)Verify that Cumulative Fee calculation is equal feeAmount from DB
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Cumulative Fee - Step One, Sell')
@allure.testcase(
    BaseConfig.GITLAB_URL + "/fees_tests/cumulative_fees_tests/C5696_cumulative_fee_step_one_sell_test.py",
    "TestCumulativeFeeStepOneSellTest")
@pytest.mark.fee
@pytest.mark.cumulative_fee
@pytest.mark.usefixtures("r_time_count", "r_customer_sql", "set_cumulative_fee_first_step",)
class TestCumulativeFeeStepOneSellTest(object):

    @allure.step("Starting with: test_cumulative_fee_step_one_sell_test")
    @automation_logger(logger)
    @pytest.mark.parametrize("precondition_cumulative", [[quoted_currency_id, base_currency_id, instrument_id]],
                             indirect=True)
    def test_cumulative_fee_step_one_sell_test(self, r_customer_sql, precondition_cumulative):
        order_id_sell = precondition_cumulative['order_id']['order_id_sell']
        trade_id = Instruments.get_id_trade_by_order_id(order_id_sell)
        fee_amount_db = Instruments.get_fee_amount_by_trade(trade_id)
        amount = precondition_cumulative['amount']
        price = precondition_cumulative['price']
        assert fee_amount_db == (price * amount) - 0.05
        logger.logger.info(f"================== TEST CASE IS PASSED: {test_case}===================")
