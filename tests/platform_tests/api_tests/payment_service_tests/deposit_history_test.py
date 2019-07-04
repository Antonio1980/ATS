import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger

test_case = ""


@allure.feature("Deposit")
@allure.title("Deposit History")
@allure.description("""
    Functional api test.
    Validation of response after getting deposit history.
    1)Get deposit history for customer that has deposit.
    2)Get deposit history for customer that has no deposit
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Deposit History Test')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/deposit_history_tests.py",
                 "TestDepositHistory")
@pytest.mark.usefixtures("r_time_count", "r_customer", )
@pytest.mark.deposit
@pytest.mark.regression
@pytest.mark.payment_service
class TestDepositHistory(object):

    @pytest.fixture
    @automation_logger(logger)
    def another_customer(self):
        customer = Customer()
        customer.insert_customer_sql()
        return customer

    @allure.step("Starting: test_add_deposit_credit_card")
    @automation_logger(logger)
    def test_get_deposit_history_customer_has_deposit(self, r_customer):
        add_response = r_customer.postman.payment_service.add_credit_card(r_customer.credit_card)
        assert add_response['error'] is None
        r_customer.credit_card.id = add_response['result']['card']['id']
        r_customer.set_credit_card_status(r_customer.credit_card.id, 1)

        deposit_response = r_customer.postman.payment_service.add_deposit_credit_card(r_customer.credit_card, 100.0, 2)
        assert deposit_response['error'] is None
        deposit_history = r_customer.postman.payment_service.get_deposit_history()
        assert deposit_history['error'] is None
        for customer_id in deposit_history['result']['deposits']:
            assert int(customer_id.get('customerId')) == r_customer.customer_id
        assert deposit_history['result']['deposits'][0] != {}
        keys = list(deposit_history['result']['deposits'][0].keys())
        assert keys == ['customerId', 'currencyId', 'amount', 'time', 'rateUsd', 'statusId', 'creditCardDetails',
                        'cryptoDetails', 'fee', 'id', 'balanceChangeTransactionGuid']
        assert deposit_history['result']['deposits'][0]['id'] is not None
        
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting: test_get_deposit_history_customer_has_no_deposit")
    @automation_logger(logger)
    def test_get_deposit_history_customer_has_no_deposit(self, another_customer):
        deposit_history = another_customer.postman.payment_service.get_deposit_history()
        assert deposit_history['error'] is None
        assert deposit_history['result']['deposits'] is None

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
