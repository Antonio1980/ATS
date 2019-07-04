import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@pytest.mark.incremental
@allure.feature("Payment")
@allure.title("Credit Card Status")
@allure.description("""
    Functional api test.
    Validation of responses after change status credit card 
    1)test_update_credit_card_status_method_works, error check
    2)test_update_credit_card_status_declined, disabled -3  status
    3)test_update_credit_card_status_deleted, expiered -4 status
    4)test_update_credit_card_status_expired, deleted -5 status
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Update Credit Card Status')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/update_credit_card_status_test.py",
                 "TestUpdateCreditCardStatus")
@pytest.mark.usefixtures("r_time_count", "r_customer_sql")
@pytest.mark.cc
@pytest.mark.regression
@pytest.mark.payment_service
class TestUpdateCreditCardStatus(object):

    @allure.step("Starting: test_update_credit_card_status_method_works")
    @automation_logger(logger)
    def test_update_credit_card_status_method_works(self, r_customer_sql):
        add_response = r_customer_sql.postman.payment_service.add_credit_card(r_customer_sql.credit_card)
        assert add_response['error'] is None
        r_customer_sql.credit_card.id = add_response['result']['card']['id']

        cards_response = r_customer_sql.postman.payment_service.get_credit_cards()
        assert cards_response['error'] is None
        assert r_customer_sql.credit_card.id == cards_response['result']['cards'][-1]['id']
        assert cards_response['result']['cards'][0]['status'] == 2

        update_response = r_customer_sql.postman.payment_service.update_credit_card(r_customer_sql.credit_card.id, 6)
        assert update_response['error'] == 'unable to modify card with current status'

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting: test_update_credit_card_status_declined")
    def test_update_credit_card_status_declined(self, r_customer_sql):
        update_response = r_customer_sql.postman.payment_service.update_credit_card(r_customer_sql.credit_card.id, 3)
        assert update_response['error'] == 'unable to modify card with current status'

        cards_response = r_customer_sql.postman.payment_service.get_credit_cards()
        assert cards_response['error'] is None
        assert r_customer_sql.credit_card.id == cards_response['result']['cards'][-1]['id']
        assert cards_response['result']['cards'][0]['status'] == 2

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting: test_update_credit_card_status_deleted")
    @automation_logger(logger)
    def test_update_credit_card_status_deleted(self, r_customer_sql):
        update_response2 = r_customer_sql.postman.payment_service.update_credit_card(r_customer_sql.credit_card.id, 4)
        assert update_response2['error'] is None

        cards_response = r_customer_sql.postman.payment_service.get_credit_cards()
        assert cards_response['error'] is None
        assert r_customer_sql.credit_card.id not in cards_response['result']['cards']

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting: test_update_credit_card_status_expired")
    @automation_logger(logger)
    def test_update_credit_card_status_expired(self, r_customer_sql):
        r_customer_sql.set_credit_card_status(r_customer_sql.credit_card.id, 1)
        update_response = r_customer_sql.postman.payment_service.update_credit_card(r_customer_sql.credit_card.id, 5)
        assert update_response['error'] is None

        r_customer_sql.set_credit_card_status(r_customer_sql.credit_card.id, 1)
        cards_response = r_customer_sql.postman.payment_service.get_credit_cards()
        assert cards_response['error'] is None
        assert cards_response['result']['cards'][-1]['status'] == 1

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
