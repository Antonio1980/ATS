import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Payment")
@allure.title("Credit Cards")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
    Functional api test.

    """)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Credit Cards')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/get_cards_test.py",
                 "TestGetCreditCards")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.payment
@pytest.mark.regression
@pytest.mark.payment_service
class TestGetCreditCards(object):

    @allure.step("test_get_credit_cards_default")
    @automation_logger(logger)
    def test_get_credit_cards_default(self, r_customer):
        cards_response = r_customer.postman.payment_service.get_credit_cards()
        assert cards_response['error'] is None
        assert cards_response['result']['cards'] is not None
        assert isinstance(cards_response['result']['cards'], list)

        logger.logger.info("Test case - test_get_credit_cards_default - PASSED")

    @allure.step("test_check_credit_card_id")
    @automation_logger(logger)
    def test_check_credit_card_id(self, r_customer):
        add_card_resp = r_customer.postman.payment_service.add_credit_card(r_customer.credit_card)
        assert add_card_resp['result']['card']
        if isinstance(add_card_resp['result']['card'], list) and len(add_card_resp['result']['card']) > 0:
            response = add_card_resp['result']['card'][-1]
        else:
            response = add_card_resp['result']['card']
        assert r_customer.credit_card.id == response['id']
        assert r_customer.credit_card.owner_ln in response['holderName']
        assert response['status'] == 2

        logger.logger.info("Test case - test_check_get_cards_exception - PASSED")

