import time
import allure
import pytest
from config_definitions import BaseConfig
from src.base import logger
from src.base.browser import Browser
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.customer_page import CustomerPage
from tests.crm_tests_base.home_page import HomePage
from tests.crm_tests_base.login_page import LogInPage

test_case = '3409'


@allure.title("Customer")
@allure.description("""
    Verification of adding deposit for a customer account. UI test.
    1. Login to CRM with user has Super Admin permissions
    2. Open Customer Page by customer id
    3. Check deposit 'amount by currency before' deposit for Customer
    4. Generate deposit for that customer with 'deposit_amount'
    5. Check deposit 'amount by currency after' deposit for Customer
    6. Calculation: 'amount by currency after' == 'amount by currency before' + 'deposit_amount'
    
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Add deposit for a customer account')
@allure.testcase(BaseConfig.GITLAB_URL_CRM +
                 "/customer_tests/C3408_upgrade_customer_to_depositor_test.py",
                 "TestAddDeposit")
@pytest.mark.usefixtures("r_time_count", 'web_driver', 'r_customer')
@pytest.mark.crm_sanity
class TestAddDeposit(object):
    browser = Browser()
    home_page = HomePage()
    login_page = LogInPage()
    customer_page = CustomerPage()
    locators = customer_page.locators
    deposit_amount = 1000

    @allure.step("test_customer_status_upgrade")
    @automation_logger(logger)
    def test_add_deposit(self, web_driver, r_customer):
        assert self.login_page.login(web_driver, self.login_page.crm_username, self.login_page.crm_password)
        deposit_amount_query = ("SELECT SUM(amount)FROM deposits WHERE customerId = " + str(
            r_customer.customer_id) + " and currencyId = 18;")
        deposit_amount_before = Instruments.run_mysql_query(deposit_amount_query)[0][0]
        if deposit_amount_before is None:
            deposit_amount_before = 0.0
        assert self.home_page.choose_customer_by_option(web_driver, r_customer.customer_id, "Id")
        assert self.customer_page.make_deposit(web_driver, "GBP", self.deposit_amount, "Approved")
        time.sleep(4.0)
        deposit_amount_after = float(Instruments.run_mysql_query(deposit_amount_query)[0][0])
        assert deposit_amount_after == (deposit_amount_before + self.deposit_amount)
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
