import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.data_bases.sql_db import SqlDb
from src.base.equipment.deposit import Deposit
from src.base.log_decorator import automation_logger

test_case = ""
currency_id = 1
max_deposit_for_currency = 500.0


@pytest.mark.incremental
@allure.story("Client able to perform withdrawal from his trading account.")
@allure.title("DEPOSIT FIAT")
@allure.description("""
    Functional tests.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='First Fiat Deposit')
@allure.testcase(BaseConfig.GITLAB_URL + "/payment_sanity_tests/first_fiat_deposit_test.py", "TestFirstFiatDeposit")
@pytest.mark.usefixtures("r_time_count", "r_customer")
@pytest.mark.deposit
@pytest.mark.payment_sanity
class TestFirstFiatDeposit(object):
    next_process_date_before, next_process_date_after = None, None

    @allure.step("Start with: test_first_fiat_deposit")
    @automation_logger(logger)
    def test_first_fiat_deposit(self, r_customer):
        logger.logger.info("test case {0} method test_withdrawal_crypto_negative".format(test_case))

        r_customer.add_credit_card_and_deposit(max_deposit_for_currency, currency_id)

        logger.logger.info("DEPOSIT SUCCESS: {0}".format(r_customer.transactions[0]))

    @allure.step("Proceed with: test_next_process_date_before")
    @automation_logger(logger)
    def test_next_process_date_before(self, r_customer):
        query = "SELECT nextProcessDate FROM fee_scheduler WHERE customerId=" + str(r_customer.customer_id) + ";"
        query_result = SqlDb.run_mysql_query(query)
        TestFirstFiatDeposit.next_process_date_before = str(query_result[0][0])

        logger.logger.info("1 Next process date: {0}".format(TestFirstFiatDeposit.next_process_date_before))

    @allure.step("Proceed with: test_next_process_date_before")
    @automation_logger(logger)
    def test_second_fiat_deposit(self, r_customer):
        deposit_credit_card = r_customer.postman.payment_service.add_deposit_credit_card(
            r_customer.credit_card, max_deposit_for_currency, currency_id)
        assert deposit_credit_card['error'] is None
        deposit_id = deposit_credit_card['result']['depositId']
        r_customer.transactions.append(Deposit(deposit_id))

        logger.logger.info("DEPOSIT SUCCESS: {0}".format(deposit_id))

    @allure.step("Proceed with: test_check_next_process_date_after")
    @automation_logger(logger)
    def test_check_next_process_date_after(self, r_customer):
        query = "SELECT nextProcessDate FROM fee_scheduler WHERE customerId=" + str(r_customer.customer_id) + ";"
        next_process_date_after = str(SqlDb.run_mysql_query(query)[0][0])
        logger.logger.info("2 Next process date: {0}".format(next_process_date_after))

        assert TestFirstFiatDeposit.next_process_date_before == next_process_date_after

        logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, r_customer.customer_id))
