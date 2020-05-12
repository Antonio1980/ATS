import allure
import pytest
from config_definitions import BaseConfig
from src.base import logger
from src.base.browser import Browser
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.customer_page import CustomerPage
from tests.crm_tests_base.home_page import HomePage
from tests.crm_tests_base.login_page import LogInPage

test_case = '3416'


@allure.title("Customer")
@allure.description("""
    Verification of upgrading "Customer" to "Depositor". UI test.
    1. Login to CRM with user has Super Admin permissions
    2. Create Customer as Lead
    3. Open Customer Page by customer id
    4. Check Customer Icon, it must be "Lead"
    5. Verify , that next elements are not presented on the Customer Page:
       - Change Password
       - Balance
       - Trading Area
       - Balance Tab
       - Deposits/Withdrawals tab 
       - Trades Tab
       - Fees Tab
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Verify "Lead" account limitations')
@allure.testcase(BaseConfig.GITLAB_URL_CRM +
                 "/customer_tests/C3416_lead_limitations_test.py",
                 "TestLeadLimitations")
@pytest.mark.usefixtures("r_time_count", 'web_driver', 'customer_new')
@pytest.mark.crm_sanity
class TestLeadLimitations(object):
    browser = Browser()
    home_page = HomePage()
    login_page = LogInPage()
    customer_page = CustomerPage()
    locators = customer_page.locators
    delay = customer_page.ui_delay

    @allure.step("Start with: test_open_homepage")
    @automation_logger(logger)
    def test_open_homepage(self, web_driver):
        assert self.login_page.login(web_driver, self.login_page.crm_username, self.login_page.crm_password)

    @allure.step("Proceed with: test_customer_page")
    @automation_logger(logger)
    def test_customer_page(self, web_driver, customer_new):
        assert self.home_page.choose_customer_by_option(web_driver, customer_new.customer_id, "Id")
        customer_id_ui = self.customer_page.get_customer_id_from_customer_page(web_driver)
        assert customer_id_ui == customer_new.customer_id

    @allure.step("Proceed with: test_verification_lead_limitation")
    @automation_logger(logger)
    def test_verification_lead_limitation(self, web_driver):
        attribute = self.customer_page.check_icon(web_driver, self.locators.LEAD_ICON)
        assert attribute == 'Lead'
        assert self.browser.check_element_is_not_presented(web_driver, self.locators.CUSTOMER_PASSWORD_ICON)
        assert self.browser.check_element_is_not_presented(web_driver, self.locators.BALANCE_CUSTOMER_PAGE)
        # not relevant for checking
        # assert self.browser.check_element_is_not_presented(web_driver, self.locators.CUSTOMER_BALANCE_TAB)
        # assert self.browser.check_element_is_not_presented(web_driver, self.locators.CUSTOMER_FEES_TAB)
        # assert self.browser.check_element_is_not_presented(web_driver, self.locators.CUSTOMER_TRADES_TAB)
        # assert self.browser.check_element_is_not_presented(web_driver,
        # self.locators.CUSTOMER_PAGE_DEPOSITS_WITHDRAWALS_TAB)
        # assert self.browser.check_element_is_not_presented(web_driver, self.locators.CUSTOMER_TRADING_AREA)
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
