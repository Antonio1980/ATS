import allure
import pytest
from config_definitions import BaseConfig
from src.base import logger
from src.base.browser import Browser
from src.base.log_decorator import automation_logger
from tests.crm_tests_base.customer_page import CustomerPage
from tests.crm_tests_base.home_page import HomePage
from tests.crm_tests_base.login_page import LogInPage

test_case = '8190'


@allure.title("Customer page. Personal Information Tab")
@allure.description("""
    Verification Personal Information Tab. UI test.
    1. Log in to the CRM. OPen Home page.
    2. Open th customer page.
    3. Verify UI elements at the Personal Information Tab.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Personal Information Tab UI Test')
@allure.testcase(BaseConfig.GITLAB_URL_CRM +
                 "/customer_tests/C8190_personal_information_tab_ui_test.py",
                 "TestPersonalInformationTabUI")
@pytest.mark.usefixtures("r_time_count", 'web_driver', 'customer_pending')
@pytest.mark.crm_sanity
class TestPersonalInformationTabUI(object):
    browser = Browser()
    home_page = HomePage()
    login_page = LogInPage()
    customer_page = CustomerPage()
    locators = customer_page.locators
    delay = customer_page.ui_delay

    @allure.step("Proceed with: test_open_home_page")
    @automation_logger(logger)
    def test_open_homepage(self, web_driver):
        assert self.login_page.login(web_driver, self.login_page.crm_username, self.login_page.crm_password)

    @allure.step("Proceed with: test_open_customer_page")
    @automation_logger(logger)
    def test_customer_page(self, web_driver, customer_pending):
        assert self.home_page.choose_customer_by_option(web_driver, customer_pending.customer_id, "Id")
        customer_id_ui = self.customer_page.get_customer_id_from_customer_page(web_driver)
        assert customer_id_ui == customer_pending.customer_id

    @allure.step("Proceed with: test_personal_information_verification_ui")
    @automation_logger(logger)
    def test_personal_(self, web_driver, customer_pending):
        assert self.browser.wait_element_presented(web_driver, self.locators.CUSTOMER_PERSONAL_INFORMATION_TAB,
                                                   self.delay)
        assert self.browser.wait_element_presented(web_driver, self.locators.PERSONAL_TAB_FIRST_NAME,
                                                   self.delay)
        assert self.browser.wait_element_presented(web_driver, self.locators.PERSONAL_TAB_INPUT_FIELD_FIRST_NAME,
                                                   self.delay)
        assert self.browser.wait_element_presented(web_driver, self.locators.PERSONAL_TAB_LAST_NAME,
                                                   self.delay)
        assert self.browser.wait_element_presented(web_driver, self.locators.PERSONAL_TAB_INPUT_FIELD_FIRST_NAME,
                                                   self.delay)
        assert self.browser.wait_element_presented(web_driver, self.locators.PERSONAL_TAB_PERSONAL_ID,
                                                   self.delay)
        assert self.browser.wait_element_presented(web_driver, self.locators.PERSONAL_TAB_INPUT_FIELD_PERSONAL_ID,
                                                   self.delay)
        pass
        logger.logger.info("Test {0}".format(test_case))
        logger.logger.info("==================== TEST IS PASSED ====================")
