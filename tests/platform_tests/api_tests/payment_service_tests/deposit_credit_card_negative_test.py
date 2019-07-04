import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@pytest.mark.incremental
@allure.feature("Payment")
@allure.title("Deposit Credit Card Negative Tests")
@allure.description("""
    Negative api test.
    1. Verify that credit card with status "Unverified" (SQL status=2 given by default) can't be used for deposit. 
    2. Verify that credit card with status "Declined" (SQL status=3) can't be used for deposit. 
    3. Verify that credit card with status "Deleted" (SQL status=4) can't be used for deposit. 
    4. Verify that credit card with status "Expiered" (SQL status=5) can't be used for deposit. 
    5. Verify that credit card with status "Verified" (SQL status=1) can be used for deposit. 
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Deposit Credit Card Negative')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/deposit_credit_card_negative_test.py",
                 "TestDepositCreditCardNegative")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.deposit
@pytest.mark.regression
@pytest.mark.payment_service
class TestDepositCreditCardNegative(object):
    card_id = None

    @allure.step("Verify that credit card with status 'Unverified' (SQL status=1) can't be used for deposit.")
    @automation_logger(logger)
    def test_add_deposit_credit_card_unverified(self, r_customer):
        add_response = r_customer.postman.payment_service.add_credit_card(r_customer.credit_card)
        assert add_response['error'] is None
        TestDepositCreditCardNegative.card_id = add_response['result']['card']['id']
        assert add_response['result']['card']['status'] == 2

        deposit_response = r_customer.postman.payment_service.add_deposit_credit_card(
            r_customer.credit_card, 1000.0, 2)
        assert deposit_response['error'] is not None

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Verify that credit card with status 'Declined' (SQL status=3) can't be used for deposit.")
    @automation_logger(logger)
    def test_add_deposit_credit_card_declined(self, r_customer):
        r_customer.credit_card.id = TestDepositCreditCardNegative.card_id
        r_customer.set_credit_card_status(r_customer.credit_card.id, 3)

        deposit_response = r_customer.postman.payment_service.add_deposit_credit_card(
            r_customer.credit_card, 1000.0, 2)
        assert deposit_response['error'] is not None

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Verify that credit card with status 'Deleted' (SQL status=4) can't be used for deposit. ")
    @automation_logger(logger)
    def test_add_deposit_credit_card_deleted(self, r_customer):
        r_customer.credit_card.id = TestDepositCreditCardNegative.card_id
        r_customer.set_credit_card_status(r_customer.credit_card.id, 4)

        deposit_response = r_customer.postman.payment_service.add_deposit_credit_card(
            r_customer.credit_card, 1000.0, 2)
        assert deposit_response['error'] is not None

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Verify that credit card with status 'Expired' (SQL status=5) can't be used for deposit.")
    @automation_logger(logger)
    def test_add_deposit_credit_card_expiered(self, r_customer):
        r_customer.credit_card.id = TestDepositCreditCardNegative.card_id
        r_customer.set_credit_card_status(r_customer.credit_card.id, 5)

        deposit_response = r_customer.postman.payment_service.add_deposit_credit_card(
            r_customer.credit_card, 1000.0, 2)
        assert deposit_response['error'] is not None

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Verify that credit card with status 'Verified' (SQL status=1) can be used for deposit.")
    @automation_logger(logger)
    def test_add_deposit_credit_card_verified(self, r_customer):
        r_customer.credit_card.id = TestDepositCreditCardNegative.card_id
        r_customer.set_credit_card_status(r_customer.credit_card.id, 1)

        deposit_response = r_customer.postman.payment_service.add_deposit_credit_card(
            r_customer.credit_card, 1000.0, 2)
        assert deposit_response['error'] is None
        assert deposit_response['result']['depositId'] is not None

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
