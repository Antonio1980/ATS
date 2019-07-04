import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = ""


@pytest.mark.incremental
@allure.feature("Deposit")
@allure.title("Deposit Credit Card")
@allure.description("""
    Functional api test.
    Validation of response after deposit credit card 
    1)Add deposit with valid amount and currency_id.
    2)Add deposit with not valid amount and valid currency_id
    3)Add deposit with valid amount and not valid currency_id
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Deposit Credit Card')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/deposit_credit_card_tests.py",
                 "TestDepositCreditCard")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.deposit
@pytest.mark.regression
@pytest.mark.payment_service
class TestDepositCreditCard(object):

    @allure.step("Starting: test_add_deposit_credit_card")
    @automation_logger(logger)
    def test_add_deposit_credit_card(self, r_customer):
        cards_response = r_customer.postman.payment_service.get_credit_cards()
        try:
            card_status = cards_response['result']['cards'][-1]['status']
            if card_status != 1:
                r_customer.set_credit_card_status(cards_response['result']['cards'][-1]['id'], 1)
            r_customer.credit_card.id = cards_response['result']['cards'][-1]['id']
        except (IndexError, TypeError, ValueError):
            add_response = r_customer.postman.payment_service.add_credit_card(r_customer.credit_card)
            assert add_response['error'] is None
            r_customer.credit_card.id = add_response['result']['card']['id']
            r_customer.set_credit_card_status(r_customer.credit_card.id, 1)
            
        deposit_response = r_customer.postman.payment_service.add_deposit_credit_card(r_customer.credit_card, 1000.0, 2)
        assert deposit_response['error'] is None
        assert deposit_response['result']['depositId'] is not None

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting: test_add_deposit_with_not_valid_amount_credit_card_negative")
    @automation_logger(logger)
    def test_add_deposit_with_negative_amount(self, r_customer):
        add_response = r_customer.postman.payment_service.add_credit_card(r_customer.credit_card)
        assert add_response['error'] is None
        deposit_response = r_customer.postman.payment_service.add_deposit_credit_card(r_customer.credit_card, -10.0, 1)
        assert deposit_response['error'] == 'requested amount is less than min amount'

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting:  test_add_deposit_with_incorrect_instrument_id_credit_card_negative")
    @automation_logger(logger)
    def test_add_deposit_with_incorrect_currency_negative(self, r_customer):
        add_response = r_customer.postman.payment_service.add_credit_card(r_customer.credit_card)
        assert add_response['error'] is None
        deposit_response = r_customer.postman.payment_service.add_deposit_credit_card(r_customer.credit_card, 10.0, 122)
        assert deposit_response['error'] == 'deposit error'
        
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
