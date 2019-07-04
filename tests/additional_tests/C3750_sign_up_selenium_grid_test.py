import allure
import pytest
import unittest
from src.base import logger
from src.base.utils.utils import Utils
from src.base.customer.customer import Customer
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.home_page import HomePage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base.signup_page import SignUpPage

test_case = '3750'


@pytest.mark.skip
@pytest.mark.advanced
class TestSignUpFullFlowGrid(unittest.TestCase):
    @allure.step("Set Up")
    @automation_logger(logger)
    def setUp(self):
        self.customer = Customer()
        self.home_page = HomePage()
        self.signup_page = SignUpPage()
        self.signin_page = SignInPage()
        self.browser = self.customer.get_browser_functionality()
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.customer.email)

    @allure.step("Set Up")
    @automation_logger(logger)
    def test_sign_up_selenium_grid(self, browser):
        logger.logger.info("TEST CASE N: {0}".format(test_case))
        logger.logger.info("method test_sign_up_full_flow, with:  browser- {0} ".format(browser))
        WebDriverFactory.start_selenium_server(browser)
        self.driver = WebDriverFactory.get_remote_driver(browser)
        assert self.home_page.open_signup_page(self.driver)
        assert self.signup_page.fill_signup_form(self.driver, self.customer.username, self.customer.email,
                                                 self.customer.password, self.element)
        self.customer_id = self.browser.execute_js(self.driver, self.customer.scripts.script_customer_id)
        assert self.customer_id
        verification_url = Utils.get_mail_gun_item(self.customer)

        assert self.signup_page.go_by_token_url(self.driver, verification_url)
        assert self.signup_page.add_phone(self.driver, self.customer.phone)
        assert self.signup_page.enter_phone_code(self.driver, "123456")
        assert self.signup_page.fill_personal_details(self.driver, self.customer.birthday, self.customer.zip_,
                                                      self.customer.city)
        assert self.signup_page.fill_client_checklist_1(self.driver, self.customer.scripts.script_checklist)
        assert self.signup_page.fill_client_checklist_2(self.driver)
        assert self.signup_page.finish_registration(self.driver)
        assert self.home_page.sign_out(self.driver)
        assert self.home_page.open_signin_page(self.driver)
        assert self.signin_page.sign_in(self.driver, self.customer.email, self.customer.password)
        logger.logger.info(self.customer.email + "," + self.customer.password + "," + self.customer_id + "\n")

    @allure.step("Tear Down")
    @automation_logger(logger)
    def tearDown(self):
        logger.logger.info("TEST STOP -> Closing browser... {0}".format(self.driver.name))
        self.browser.close_browser(self.driver)
