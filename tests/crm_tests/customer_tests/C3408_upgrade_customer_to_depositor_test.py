import time
import allure
import pytest
from config_definitions import BaseConfig
from src.base import logger
from src.base.browser import Browser
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.customer_page import CustomerPage
from tests.crm_tests_base.home_page import HomePage
from tests.crm_tests_base.login_page import LogInPage

test_case = '3408'


@allure.title("Customer")
@allure.description("""
    Verification of upgrading "Customer" to "Depositor". UI test.
    1. Login to CRM with user has Super Admin permissions
    2. Select Customer that has Registration Step = 8 and no deposit from DB or create New Customer
     with Registration Step = 8 and no deposit
    3. Open Customer Page by customer id
    4. Check Customer Icon, it must be "Customer"
    5. Generate deposit for that customer
    6. Check Customer Icon, it must be "Depositor"
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Upgrade "Customer" to "Depositor"')
@allure.testcase(BaseConfig.GITLAB_URL_CRM +
                 "/customer_tests/C3408_upgrade_customer_to_depositor_test.py",
                 "TestCustomerUpgradeStatus")
@pytest.mark.usefixtures("r_time_count", 'web_driver', 'customer_pending')
@pytest.mark.crm_sanity
class TestCustomerUpgradeStatus(object):
    browser = Browser()
    home_page = HomePage()
    login_page = LogInPage()
    customer_page = CustomerPage()
    locators = customer_page.locators

    @allure.step("test_customer_status_upgrade")
    @automation_logger(logger)
    @allure.step("Start with: test_open_homepage")
    @automation_logger(logger)
    def test_open_homepage(self, web_driver):
        assert self.login_page.login(web_driver, self.login_page.crm_username, self.login_page.crm_password)

    @allure.step("Proceed with: test_customer_page")
    @automation_logger(logger)
    def test_customer_page(self, web_driver, customer_pending):
        assert self.home_page.choose_customer_by_option(web_driver, customer_pending.customer_id, "Id")
        customer_id_ui = self.customer_page.get_customer_id_from_customer_page(web_driver)
        assert customer_id_ui == customer_pending.customer_id

    @allure.step("Proceed with: test_customer_update_to_depositor")
    @automation_logger(logger)
    def test_customer_update_to_depositor(self, web_driver, customer_pending):
        attribute = self.customer_page.check_icon(web_driver, self.locators.CUSTOMER_ICON)
        assert attribute == 'Customer'
        assert self.customer_page.make_deposit(web_driver, "USD", 1500, "Approved")
        self.browser.refresh_browser(web_driver)
        time.sleep(3)
        attribute = self.customer_page.check_icon(web_driver, self.locators.DEPOSITOR_ICON)
        assert attribute == 'Depositor'
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
