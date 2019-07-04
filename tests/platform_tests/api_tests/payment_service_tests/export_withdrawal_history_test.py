import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = ""
currency_id = 2


@allure.feature("Withdrawal")
@allure.title("Export Withdrawal")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
     Functional api test.
    Validation of response after export withdrawal history.
    1)Export withdrawal history for customer that has withdrawal.
    2)Export withdrawal history for customer that has no withdrawal.
    """)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Export Withdrawal History')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/export_withdrawal_history_test.py",
                 "TestExportWithdrawalHistory")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.withdrawal
@pytest.mark.regression
@pytest.mark.payment_service
class TestExportWithdrawalHistory(object):
    
    @pytest.fixture
    @automation_logger(logger)
    def another_new_customer(self):
        customer = Customer()
        customer.insert_customer_sql()
        return customer

    @allure.step("Starting with: test_export_withdrawal_history_customer_has_withdrawal")
    @automation_logger(logger)
    @pytest.mark.parametrize('add_balance', [[currency_id]], indirect=True)
    def test_export_withdrawal_history_customer_has_withdrawal(self, r_customer, add_balance):
        withdrawal_response = r_customer.postman.payment_service.withdrawal_wire(r_customer.bank, currency_id, 250)
        assert withdrawal_response['error'] is None
        withdrawal_token = withdrawal_response['result']['token']
        logger.logger.info(F"Withdrawal wire token: {withdrawal_token}")

        history_response = r_customer.postman.payment_service.export_withdrawal_history()
        assert history_response['error'] is None
        link = history_response['result']['link']
        assert link.find('.csv')!= -1
        assert link.find(str(r_customer.customer_id)) != -1
        assert link.find('withdrawals_history') != -1

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting: test_export_withdrawal_history_customer_has_no_withdrawal")
    @automation_logger(logger)
    def test_export_withdrawal_history_customer_has_no_withdrawal(self, another_new_customer):
        history_response = another_new_customer.postman.payment_service.export_withdrawal_history()
        assert history_response['result']['link']
        assert history_response['error'] is None

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))