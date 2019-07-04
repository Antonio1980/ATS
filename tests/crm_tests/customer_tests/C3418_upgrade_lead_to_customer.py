import allure
import pytest
from config_definitions import BaseConfig
from src.base import logger
from src.base.browser import Browser
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.customer_page import CustomerPage
from tests.crm_tests_base.home_page import HomePage
from tests.crm_tests_base.login_page import LogInPage

test_case = '3418'


@allure.title("Lead")
@allure.description("""
    Verification of upgrading "Lead" to "Customer". UI test.
    1. Login to CRM with user has Super Admin permissions
    2. Select Customer that 'Lead' has Registration Step less than marked at the local config from DB or create New Lead
    3. Open Customer Page by customer id
    4. Check Customer Icon, it must be "Lead"
    5. Proceed with all registration steps with current customer
    6. Check Customer Icon, it must be "Customer"
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Upgrade "Lead" to "Customer"')
@allure.testcase(BaseConfig.GITLAB_URL_CRM +
                 "/customer_tests/C3418_upgrade_lead_to_customer_test.py",
                 "TestLeadUpgradeStatus")
@pytest.mark.usefixtures('r_time_count', 'customer_new', 'web_driver')
@pytest.mark.crm_sanity
class TestCustomerUpgradeStatus(object):
    browser = Browser()
    home_page = HomePage()
    login_page = LogInPage()
    customer_page = CustomerPage()
    locators = customer_page.locators
    attribute = None

    @allure.step("Start with: test_open_homepage")
    @automation_logger(logger)
    def test_open_homepage(self, web_driver):
        assert self.login_page.login(web_driver, self.login_page.crm_username, self.login_page.crm_password)

    @allure.step("Proceed with: test_customer_page")
    @automation_logger(logger)
    def test_customer_page(self, web_driver, customer_new):
        assert self.home_page.choose_customer_by_option(web_driver, customer_new.customer_id, "Id")

    @allure.step("Proceed with: test_check_lead_status")
    @automation_logger(logger)
    def test_check_lead_status(self, web_driver, customer_new):
        TestCustomerUpgradeStatus.attribute = self.customer_page.check_icon(web_driver, self.locators.LEAD_ICON)
        assert self.attribute == 'Lead'

    @allure.step("Proceed with: test_update_lead_to_customer")
    @automation_logger(logger)
    def test_update_lead_to_customer(self, web_driver, customer_new):
        customer_new.registration_from_step_2_to_8()
        self.browser.refresh_browser(web_driver)
        TestCustomerUpgradeStatus.attribute = self.customer_page.check_icon(web_driver, self.locators.CUSTOMER_ICON)
        assert self.attribute == 'Customer'
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
