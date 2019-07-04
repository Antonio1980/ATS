import time
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.customer.customer import Customer
from src.base.data_bases.sql_db import SqlDb
from src.base.log_decorator import automation_logger

test_case = ""
currency_id = 2
c_currency_id = 4


@allure.feature("Withdrawal")
@allure.title("Withdrawal History")
@allure.severity(allure.severity_level.BLOCKER)
@allure.description("""
    Functional api test.
    1. Verify that withdrawal history method works for customer 
    """)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Withdrawal History')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/payment_service_tests/withdrawal_history_test.py",
                 "TestWithdrawalHistory")
@pytest.mark.usefixtures("r_time_count", "conf_customer")
@pytest.mark.withdrawal
@pytest.mark.regression
@pytest.mark.payment_service
class TestWithdrawalHistory(object):
    @pytest.fixture
    @automation_logger(logger)
    def another_customer(self):
        customer = Customer()
        customer.insert_customer_sql()
        return customer

    @allure.step("Starting with: test_withdrawal_history_customer_has_withdrawal")
    @automation_logger(logger)
    def test_withdrawal_history_customer_has_withdrawal(self, conf_customer):
        history_response = conf_customer.postman.payment_service.get_withdrawal_history()
        assert history_response['error'] is None
        assert history_response['result']

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: test_withdrawal_history_customer_has_withdrawal")
    @pytest.mark.parametrize("min_withdrawal_for_currency", [[c_currency_id]], indirect=True)
    @automation_logger(logger)
    def test_crypto_withdrawal_history_and_customer_id(self, conf_customer, min_withdrawal_for_currency):
        payment_method = 3

        withdrawal_response = conf_customer.postman.payment_service.withdrawal_crypto(
            c_currency_id, min_withdrawal_for_currency, conf_customer.btc_wallet)
        assert withdrawal_response['error'] is None
        time.sleep(5.0)

        withdrawals = SqlDb.get_withdrawals_by_customer(conf_customer.customer_id, payment_method, '')
        logger.logger.info(F"Customer crypto withdrawals before confirmation: {withdrawals}")
        withdrawal_id = withdrawals[0][0]
        logger.logger.info(F"Withdrawal wire ID: {withdrawal_id}")

        history_response = conf_customer.postman.payment_service.get_withdrawal_history(payment_method)
        assert isinstance(history_response['result']['withdrawals'], list)
        assert len(withdrawals) == history_response['result']['total']['count']
        assert history_response['result']['withdrawals'][0]['id'] == withdrawal_id

        for customer_id in history_response['result']['withdrawals']:
            assert int(customer_id.get('customerId')) == int(conf_customer.customer_id)

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting with: test_withdrawal_history_customer_has_withdrawal")
    @pytest.mark.parametrize("min_withdrawal_for_currency", [[currency_id]], indirect=True)
    @automation_logger(logger)
    def test_wire_withdrawal_history_and_customer_id(self, conf_customer, min_withdrawal_for_currency):
        payment_method = 2
        time.sleep(10.0)
        
        withdrawal_response = conf_customer.postman.payment_service.withdrawal_wire(
            conf_customer.bank, currency_id, min_withdrawal_for_currency)
        assert withdrawal_response['error'] is None
        time.sleep(5.0)

        withdrawals = SqlDb.get_withdrawals_by_customer(conf_customer.customer_id, payment_method, '')
        logger.logger.info(F"Customer wire withdrawals before confirmation: {withdrawals}")
        withdrawal_id = withdrawals[0][0]
        logger.logger.info(F"Withdrawal wire ID: {withdrawal_id}")

        history_response = conf_customer.postman.payment_service.get_withdrawal_history(payment_method)
        assert isinstance(history_response['result']['withdrawals'], list)
        assert len(withdrawals) == history_response['result']['total']['count']
        assert history_response['result']['withdrawals'][0]['id'] == withdrawal_id

        for customer_id in history_response['result']['withdrawals']:
            assert int(customer_id.get('customerId')) == int(conf_customer.customer_id)

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @pytest.mark.parametrize("min_withdrawal_for_currency", [[currency_id]], indirect=True)
    @automation_logger(logger)
    def test_sepa_withdrawal_history_and_customer_id(self, conf_customer, min_withdrawal_for_currency):
        payment_method = 4
        time.sleep(10.0)
        
        withdrawal_response = conf_customer.postman.payment_service.withdrawal_sepa(
            conf_customer.bank, currency_id, min_withdrawal_for_currency)
        assert withdrawal_response['error'] is None
        time.sleep(5.0)

        withdrawals = SqlDb.get_withdrawals_by_customer(conf_customer.customer_id, payment_method, '')
        logger.logger.info(F"Customer sepa withdrawals before confirmation: {withdrawals}")
        withdrawal_id = withdrawals[0][0]
        logger.logger.info(F"Withdrawal wire ID: {withdrawal_id}")
        
        history_response = conf_customer.postman.payment_service.get_withdrawal_history(payment_method)
        assert isinstance(history_response['result']['withdrawals'], list)
        assert len(withdrawals) == history_response['result']['total']['count']
        assert history_response['result']['withdrawals'][0]['id'] == withdrawal_id

        for customer_id in history_response['result']['withdrawals']:
            assert int(customer_id.get('customerId')) == int(conf_customer.customer_id)

        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))

    @allure.step("Starting: test_get_withdrawal_history_customer_has_no_withdrawal")
    @automation_logger(logger)
    def test_get_withdrawal_history_customer_has_no_withdrawal(self, another_customer):
        history_response = another_customer.postman.payment_service.get_withdrawal_history()
        assert history_response['error'] is None
        assert history_response['result']['withdrawals'] is None
        
        logger.logger.info("================== TEST CASE {0} PASSED ===================".format(test_case))
