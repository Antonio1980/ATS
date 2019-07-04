import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger

test_case = "8146"


@allure.feature("Balance")
@allure.story("Verify that API returns error for invalid currency id")
@allure.title("Test for Invalid currency identifier")
@allure.description("""
    Functional api test.
    Coverage:
    balance_service, balance, api
    1 test Invalid currency identifier (To send request with invalid currency id)
    """)
@allure.severity(allure.severity_level.BLOCKER)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Invalid Currency Identifier')
@allure.testcase(BaseConfig.GITLAB_URL + "/api_tests/balance_service_tests/C8146_invalid_currency_identifier_negative_test.py",
                 "TestInvalidCurrencyIdentifierNegative")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.balance
@pytest.mark.regression
@pytest.mark.balance_service
class TestInvalidCurrencyIdentifierNegative(object):
    currency_id = 3
    amount = 10
    error = 101
    transaction_guid = "587756e2-47c9-4ff7-9c6d-77410ba636a0"
    total_balance, frozen_balance = None, None

    @allure.step("Starting with: getting balance with invalid currency")
    @automation_logger(logger)
    def test_get_balance_invalid_currency(self, r_customer):
        get_balance = r_customer.postman.balance_service.get_currency_balance(r_customer.customer_id, 0)
        assert get_balance['error']['code'] is not None
        assert self.error == get_balance['error']['code']
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: frozen balance with invalid currency")
    @automation_logger(logger)
    def test_frozen_invalid_currency(self, r_customer):
        frozen = r_customer.postman.balance_service.subtract_transaction_initialize(r_customer.customer_id, 0,
                                                                                    self.amount)
        assert frozen['error']['code'] is not None
        assert self.error == frozen['error']['code']
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: subtract (partial commit) balance with invalid currency")
    @automation_logger(logger)
    def test_subtract_transaction_invalid_currency(self, r_customer):
        partial_commit = r_customer.postman.balance_service.subtract_transaction_partial_commit(self.transaction_guid,
                                                                                                r_customer.customer_id,
                                                                                                0, self.amount)
        assert partial_commit['error']['code'] is not None
        assert self.error == partial_commit['error']['code']
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: subtract (partial commit) balance with invalid currency")
    @automation_logger(logger)
    def test_subtract_transaction_invalid_currency(self, r_customer):
        partial_commit = r_customer.postman.balance_service.subtract_transaction_partial_commit(self.transaction_guid,
                                                                                                r_customer.customer_id,
                                                                                                0, self.amount)
        assert partial_commit['error']['code'] is not None
        assert self.error == partial_commit['error']['code']
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: subtract (partial rollback) balance with invalid currency")
    @automation_logger(logger)
    def test_partial_rollback_invalid_currency(self, r_customer):
        partial_rollback = (r_customer.postman.balance_service.subtract_transaction_partial_rollback
                            (self.transaction_guid, r_customer.customer_id, 0, self.amount))
        assert partial_rollback['error']['code'] is not None
        assert self.error == partial_rollback['error']['code']
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: subtract balance with invalid currency")
    @automation_logger(logger)
    def test_subtract_balance_invalid_currency(self, r_customer):
        subtract_balance = r_customer.postman.balance_service.subtract_balance(r_customer.customer_id, 0, self.amount)
        assert subtract_balance['error']['code'] is not None
        assert self.error == subtract_balance['error']['code']
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))

    @allure.step("Starting with: adding balance with invalid currency")
    @automation_logger(logger)
    def test_add_balance_invalid_currency(self, r_customer):
        add_balance = r_customer.postman.balance_service.subtract_balance(r_customer.customer_id, 0, self.amount)
        assert add_balance['error']['code'] is not None
        assert self.error == add_balance['error']['code']
        logger.logger.info("================== TEST CASE PASSED ===================".format(test_case))