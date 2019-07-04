import time
import allure
import pytest
import unittest
from src.base import logger
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '5682'


@allure.title("Maintenance Time")
@allure.description("""
    Generate Fiat Deposit via Credit Card during Maintenance time, API
    1. Get me-state 
    2. Verify that me-state equal 2 (Maintenance time)
    3. Add credit card and deposit
    4. Verify that balance after deposit more that balance before deposit
    Calculation: balance_after > balance_before 
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Generate Fiat Deposit via Credit Card during Maintenance time')
@allure.testcase(
    BaseConfig.GITLAB_URL +
    "/maintenance_time_tests/C5682_fiat_deposit_via_cc_at_maintenance_time_test.py",
    "TestGenerateFiatDepositViaCreditCardDuringMaintenanceTime")
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.maintenance_time
class TestGenerateFiatDepositViaCreditCardDuringMaintenanceTime(unittest.TestCase):
    @automation_logger(logger)
    @allure.step("SetUp: calling registered customer and get me-state.")
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.state_me = Instruments.get_me_state()
        self.currency_id = 2

    @automation_logger(logger)
    @allure.step("Starting with: test_ability_to_register_during_maintenance_time")
    def test_buy_order_is_matched_with_two_and_more_orders(self):
        assert self.state_me == 2
        balance_before = float(
            self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, self.currency_id)[
                'result']['balance']['total'])
        self.customer.add_credit_card_and_deposit(1000.0, self.currency_id)
        time.sleep(5)
        balance_after = float(
            self.customer.postman.balance_service.get_currency_balance(self.customer.customer_id, self.currency_id)[
                'result']['balance']['total'])
        assert balance_after > balance_before
        logger.logger.info("Test {0}, with CustomerID {1}".format(test_case, self.customer.customer_id))
        logger.logger.info("==================== TEST IS PASSED ====================")
