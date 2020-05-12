import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Fee")
@allure.title("Export Fee")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
     Functional api test.
    Validation of response after export fee history.
    1)Export fee history for customer that has fee.
    2)Export fee history for customer that has no fee.
    """)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Export Fee History')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/export_fee_history_test.py",
                 "TestExportFeeHistory")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.fee
@pytest.mark.regression
@pytest.mark.payment_service
class TestExportDepositHistory(object):

    @pytest.fixture
    @automation_logger(logger)
    def another_customer(self):
        customer = Customer()
        customer.insert_customer_sql()
        return customer

    @allure.step("Starting with: test_export_fee_history_customer_has_deposit")
    @automation_logger(logger)
    def test_export_fee_history_customer_has_fee(self, r_customer):
        add_response = r_customer.postman.payment_service.add_credit_card(r_customer.credit_card)
        assert add_response['error'] is None
        r_customer.credit_card.id = add_response['result']['card']['id']
        r_customer.set_credit_card_status(r_customer.credit_card.id, 1)

        deposit_response = r_customer.postman.payment_service.add_deposit_credit_card(r_customer.credit_card, 1000.0, 2)
        assert deposit_response['error'] is None
        history_response = r_customer.postman.payment_service.export_fee_history()
        assert history_response['error'] is None
        link = history_response['result']['link']
        assert '.csv' in link
        assert 'fees_history' in link
        assert str(r_customer.customer_id)in link
        logger.logger.info("Test {0} PASSED, with CustomerID {1}".format(test_case, r_customer.customer_id))

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting: test_export_fee_history_customer_has_no_withdrawal")
    @automation_logger(logger)
    def test_export_fee_history_customer_has_no_fee(self, another_customer):
        history_response = another_customer.postman.payment_service.export_fee_history()
        assert history_response['result']['link']
        assert history_response['error'] is None

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
