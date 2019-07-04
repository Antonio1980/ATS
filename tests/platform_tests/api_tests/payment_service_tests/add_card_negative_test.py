import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Payment")
@allure.title("Credit Card Negative Tests")
@allure.description("""
    Negative api tests.
    1. Verify that customer with status - "New" (SQL status=1) unable to upload CC.
    2. Verify that customer with status - "Pending" (SQL status=2) unable to upload CC.
    3. Verify that customer with status - "Declined" (SQL status=4) unable to upload CC.
    4. Verify that customer with status - "Suspended" (SQL status=5) unable to upload CC.
    5. Verify that customer with status - "Blocked" (SQL status=6) unable to upload CC.
    6. Verify that customer with status - "Approved" (SQL status=3) able to upload CC.
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Add Credit Card Negative')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/add_card_negative_test.py",
                 "TestAddCreditCardNegative")
@pytest.mark.usefixtures("r_time_count", "customer_new")
@pytest.mark.payment
@pytest.mark.regression
@pytest.mark.payment_service
class TestAddCreditCardNegative(object):

    @allure.step("Verify that customer with status - 'New' (SQL status=1) unable to upload CC.")
    @automation_logger(logger)
    def test_add_credit_card_for_new_customer(self, customer_new):
        add_response = customer_new.postman.payment_service.add_credit_card(customer_new.credit_card)
        assert add_response['error'] is not None
        assert add_response['error'] == "insufficient permissions to perform the operation"

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Verify that customer with status - 'Pending' (SQL status=2) unable to upload CC.")
    @automation_logger(logger)
    def test_add_credit_card_for_pending_customer(self, customer_new):
        customer_new.set_customer_status(2)

        add_response = customer_new.postman.payment_service.add_credit_card(customer_new.credit_card)
        assert add_response['error'] is not None
        assert add_response['error'] == "insufficient permissions to perform the operation"
        
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Verify that customer with status - 'Declined' (SQL status=4) unable to upload CC.")
    @automation_logger(logger)
    def test_add_credit_card_for_declined_customer(self, customer_new):
        customer_new.set_customer_status(4)

        add_response = customer_new.postman.payment_service.add_credit_card(customer_new.credit_card)
        assert add_response['error'] is not None
        assert add_response['error'] == "insufficient permissions to perform the operation"

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Verify that customer with status - 'Suspended' (SQL status=5) unable to upload CC.")
    @automation_logger(logger)
    def test_add_credit_card_for_suspended_customer(self, customer_new):
        customer_new.set_customer_status(5)

        add_response = customer_new.postman.payment_service.add_credit_card(customer_new.credit_card)
        assert add_response['error'] is not None
        assert add_response['error'] == "insufficient permissions to perform the operation"

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Verify that customer with status - 'Blocked' (SQL status=6) unable to upload CC.")
    @automation_logger(logger)
    def test_add_credit_card_for_blocked_customer(self, customer_new):
        customer_new.set_customer_status(6)

        add_response = customer_new.postman.payment_service.add_credit_card(customer_new.credit_card)
        assert add_response['error'] is not None
        assert add_response['error'] == "insufficient permissions to perform the operation"

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Verify that customer with status - 'Approved' (SQL status=3) able to upload CC.")
    @automation_logger(logger)
    def test_add_credit_card_for_approved_customer(self, customer_new):
        customer_new.set_customer_status(3)

        add_response = customer_new.postman.payment_service.add_credit_card(customer_new.credit_card)
        assert add_response['error'] is None
        assert add_response['result']['card']['status'] == 2

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))