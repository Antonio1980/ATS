import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Payment")
@allure.title("Credit Card")
@allure.description("""
    Functional api test.
    Validation of responses after adding credit card 
    1)Checking that required keys are existed in response
    2)Checking that required keys have value is Not None
    Required keys: 'id', 'cardType', 'lastFourDigits', 'expireMonth', 'expireYear', 'holderName', 'status'
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Add Credit Card')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/add_card_tests.py", "TestDepositCreditCard")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.payment
@pytest.mark.regression
@pytest.mark.payment_service
class TestAddCreditCard(object):

    @allure.step("Starting: test_add_credit_card")
    @automation_logger(logger)
    def test_add_credit_card_method_works(self, r_customer):
        add_response = r_customer.postman.payment_service.add_credit_card(r_customer.credit_card)
        assert add_response['error'] is None
        assert isinstance(add_response['result']['card'], dict)
        assert add_response['result']['card'] != {}
        keys = list(add_response['result']['card'].keys())
        assert keys == ['id', 'cardType', 'lastFourDigits', 'expireMonth', 'expireYear', 'holderName', 'status']
        for value in add_response['result']['card'].values():
            assert value is not None
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
