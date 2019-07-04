import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signup_page import SignUpPage
from src.base.customer.registered_customer import RegisteredCustomer

test_case = '6152'


@allure.feature('Sign Up')
@allure.story('Client able to registered customer account into Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Verify Unique Email')
@allure.testcase(BaseConfig.GITLAB_URL + "/signup_tests/C6152_unique_email_test.py", "TestUniqueEmail")
@allure.severity(allure.severity_level.MINOR)
@allure.title("SIGN UP")
@allure.description("""
    Negative test.
    Verify that reusing of the email address is not available.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.smoke
@pytest.mark.negative
@pytest.mark.sign_up_page
@ddt
class TestUniqueEmail(unittest.TestCase):
    @allure.step("SetUp: calling Customer object with default properties.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = RegisteredCustomer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locators = self.signup_page.locators
        self.browser = self.customer.get_browser_functionality()
        self.script_test_token = self.signup_page.script_test_token
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.customer.email)

    @allure.step("Starting with: test_unique_email")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_unique_email(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_unique_email, with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result = 0
        delay = float(BaseConfig.UI_DELAY)
        try:
            self.assertTrue(self.home_page.open_signup_page(self.driver), "open_signup_page")

            firstname_field = self.browser.search_element(self.driver, self.locators.FIRST_NAME_FIELD, delay)
            self.browser.click_on_element(firstname_field)
            self.browser.send_keys(firstname_field, self.customer.username)
            lastname_field = self.browser.find_element(self.driver, self.locators.LAST_NAME_FIELD)
            self.browser.click_on_element(lastname_field)
            self.browser.send_keys(lastname_field, self.customer.username)
            email_field = self.browser.find_element(self.driver, self.locators.EMAIL_FIELD)
            self.browser.click_on_element(email_field)
            self.browser.send_keys(email_field, self.customer.email)
            password_field = self.browser.find_element(self.driver, self.locators.PASSWORD_FIELD)
            self.browser.click_on_element(password_field)
            self.browser.send_keys(password_field, self.customer.password)
            certify_checkbox = self.browser.find_element(self.driver, self.locators.CERTIFY_CHECKBOX)
            self.browser.click_on_element(certify_checkbox)
            newsletters_checkbox = self.browser.find_element(self.driver, self.locators.NEWSLETTERS_CHECKBOX)
            self.browser.click_on_element(newsletters_checkbox)
            self.browser.execute_js(self.driver, '$("#openAccountDxForm .captchaCode").val("test_QA_test");')
            self.browser.execute_js(self.driver, self.script_test_token)
            create_account_button = self.browser.search_element(self.driver, self.locators.CREATE_ACCOUNT_BUTTON, delay)
            self.browser.click_with_wait_and_offset(self.driver, create_account_button, 5, 5)
            self.assertTrue(self.browser.wait_element_presented(self.driver, self.locators.CUSTOMER_EXIST_ERROR, delay),
                            "CUSTOMER_EXIST_ERROR is not found.")

            logger.logger.info("TEST CASE - {0} IS PASSED !".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
