import time
import allure
import pytest
import unittest
from src.base import logger
from ddt import ddt, data, unpack
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base import wtp_open_account_url
from tests.platform_tests_base.signup_page import SignUpPage

test_case = '6150'


@allure.feature('Sign Up')
@allure.story('Client able to registered customer account into Trading Platform.')
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Email Verification - Resend email')
@allure.testcase(BaseConfig.GITLAB_URL + "/signup_tests/C6150_email_verification_resend_test.py", "TestResendVerificationEmail")
@allure.severity(allure.severity_level.NORMAL)
@allure.title("SIGN UP")
@allure.description("""
    Functional test.
    Verify that user able to request resent JWT toke to his email.
    """)
@pytest.mark.usefixtures("r_time_count")
@pytest.mark.sign_up_page
@pytest.mark.smoke
@ddt
class TestResendVerificationEmail(unittest.TestCase):
    @allure.step("SetUp: calling Customer object with default properties.")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.locator = self.signup_page.locators.CODE_FIELD
        self.browser = self.customer.get_browser_functionality()
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.customer.email)

    @allure.step("Starting with: test_resend_verification_email")
    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    @automation_logger(logger)
    def test_resend_verification_email(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_resend_verification_email, with: browser- {0} ".format(browser))
        self.driver = WebDriverFactory.get_driver(browser)
        result, ver_token = 0, None
        delay = float(BaseConfig.UI_DELAY)
        try:
            self.assertTrue(self.home_page.open_signup_page(self.driver), "open_signup_page failed")
            self.assertTrue(self.signup_page.fill_signup_form(
                self.driver, self.customer.username, self.customer.email, self.customer.password, self.element),
                "fill_signup_form failed.")
            url = Instruments.get_mail_gun_item(self.customer)
            self.assertIsNotNone(url, "MAilGun issue (URL returned as None.)")
            if url.count('=') == 2:
                ver_token = url.split('=')[1].split('&')[0]
            elif url.count('=') == 3:
                ver_token = url.split('=')[2].split('&')[0]
            # 1 - Terms link, 2 - Privacy link, 3 - Resend email
            self.assertTrue(self.signup_page.click_on_link_on_email_screen(self.driver, wtp_open_account_url, 3),
                            "Resend email link failed.")
            time.sleep(2.0)
            url2 = Instruments.get_mail_gun_item(self.customer)
            self.assertNotEqual(ver_token, self.customer.ver_token, "JWT tokens is used.")
            self.browser.go_to_url(self.driver, url2)

            self.assertIsNotNone(self.browser.search_element(self.driver, self.locator, delay), "CODE_FIELD not found.")
            logger.logger.info("TEST CASE - {0} IS PASSED !".format(test_case))
            result = 1
        finally:
            Instruments.update_test_case(self.test_run, test_case, result)

    @allure.step("TEST STOP -> Closing browser...")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
