import allure
import pytest
import unittest
from src.base import logger
from ddt import unpack, ddt, data
from src.base.enums import Browsers
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage

test_case = '3966'


@pytest.mark.skip
@allure.feature('Sign In')
@allure.story('Registered customer able to log in to Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Sign-In Form Input Fields Validation')
@allure.testcase(BaseConfig.GITLAB_URL + "/signin_tests/C3966_signin_ddt_test.py", "TestSignInDDT")
@allure.severity(allure.severity_level.MINOR)
@allure.title("SIGN IN")
@allure.description("""
    Negative test.
    Verify that AuthorizationService validate not valid email/password pairs.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.sign_in_page
@pytest.mark.negative
@ddt
class TestSignInDDT(unittest.TestCase):
    @allure.step("SetUp: calling Customer object and pages.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.browser = self.customer.get_browser_functionality()
        self.driver = WebDriverFactory.get_driver(Browsers.CHROME.value)

    @allure.step("Starting with: test_sign_in_ddt")
    @data(*Instruments.get_csv_data(BaseConfig.WTP_LOGIN_DATA))
    @unpack
    @automation_logger(logger)
    def test_sign_in_ddt(self, email, password):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_sign_in_ddt, with: credentials: {0} {1}".format(email, password))
        result = 0
        try:
            self.assertTrue(self.home_page.open_signin_page(self.driver), "open_signin_page failed")
            self.assertFalse(self.signin_page.sign_in(self.driver, email, password), "sign_in NEGATIVE failed")
            logger.logger.info("TEST CASE - {0} IS PASSED !!!".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
