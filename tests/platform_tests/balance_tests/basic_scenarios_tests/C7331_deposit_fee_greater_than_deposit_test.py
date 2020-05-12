import unittest
import allure
import pytest
from src.base import logger
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '7331'


@pytest.mark.skip(reason='Need to fix crm method add deposit')
@allure.title("API BALANCE")
@allure.description("""
    Functional test.
    Validation of 'total' balance if Deposit Fee greater than Deposit, via API
    1. Checking of 'total' GBP balance before new deposit.
    2. Add new deposit(it must be less then value of wireDepositFee from DB) via CRM
    3. Checking of 'total' GBP balance after deposit. 
    4. Verified that 'total' GBP balance = 0 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case, name='Deposit Fee Greater Than Deposit')
@allure.testcase(BaseConfig.GITLAB_URL + "/balance_tests/C7331_deposit_fee_greater_than_deposit_test.py",
                 "TestDepositFeeGreaterThanDeposit")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.balance
class TestDepositFeeGreaterThanDeposit(unittest.TestCase):
    @allure.step("SetUp: registration new customer, adding credit card with USD to balance.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.customer.clean_up_customer()
        self.currency_id = 18
        self.customer.add_credit_card_and_deposit(1000.0, 1)
        self.test_run = BaseConfig.TESTRAIL_RUN

    @allure.step("Starting with: test_deposit_fee_greater_than_deposit")
    @automation_logger(logger)
    def test_deposit_fee_greater_than_deposit(self):
        logger.logger.info("TEST CASE N: {0} STARTED !".format(test_case))
        logger.logger.info("method test_deposit_fee_greater_than_deposit ")
        result = 0
        try:
            deposit = int(Instruments.run_mysql_query(
                "SELECT wireDepositFee FROM params_deposit_withdrawal_fees WHERE currencyId =" + str(
                    self.currency_id) + ";")[0][0]) - 1
            balance_before = self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id,
                                                                                        self.currency_id)
            total_gpb_before = float(balance_before['result']['balance']['total'])
            assert total_gpb_before == 0
            self.customer.add_credit_card_and_deposit(1000.0, 2)
            assert self.customer.postman.crm.log_in_to_crm()
            crm_response = self.customer.postman.crm.add_new_deposit(self.customer.customer_id, self.customer, 2, 'GBP',
                                                                     18, deposit)
            assert crm_response['status'] == "success"
            balance_after = self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id,
                                                                                       self.currency_id)
            total_gpb_after = balance_after['result']['balance']['total']
            assert total_gpb_after == 0
            logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
            logger.logger.info("==================== TEST IS PASSED ====================")
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)
