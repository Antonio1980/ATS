import allure
import pytest

from config_definitions import BaseConfig
from src.base import logger
from src.base.browser import Browser
from src.base.enums import Browsers
from src.base.log_decorator import automation_logger
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.signin_page import SignInPage

test_case = '8083'


@allure.title("Sign In")
@allure.description("""
    Functional test.
    Verification of SignIn by deep link to Account/Settings ,  UI test
    1. Go by link.
    2. Verify that link redirect to login
    3. Sign In with registered customer
    4. Verify that link redirect to deep linked content.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Sign In and redirect by deep link Account/Settings')
@allure.testcase(BaseConfig.GITLAB_URL + "/signin_tests/C8038_sign_in_redirect_deep_link_account_settings.py",
                 "TestSignInRedirectDeepLinkAccountSettings")
@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.incremental
@pytest.mark.usefixtures('r_time_count', 'r_customer', )
class TestSignInRedirectDeepLinkAccountSettings(object):
    driver = WebDriverFactory.get_driver(Browsers.CHROME.value)
    delay = float(BaseConfig.UI_DELAY)
    sign_in_page = SignInPage()
    browser = Browser()
    url = BaseConfig.WTP_BASE_URL + '/appProxy/exchange.html?activeZonePath=myAccount/accountSettings'
    logger.logger.info("TEST CASE N: {0}".format(test_case))
    logger.logger.info(
        "method sign_in_redirect_deep_link_account_settings")

    @automation_logger(logger)
    def test_open_link(self):
        self.browser.go_to_url(self.driver, self.url)
        session_expired = self.browser.wait_element_presented(self.driver, self.sign_in_page.locators.SESSION_EXPIRED_TITLE,
                                                              self.delay + 5)
        assert session_expired is not None
        assert session_expired is not False

    @automation_logger(logger)
    def test_sign_in(self, r_customer):
        self.sign_in_page.sign_in(self.driver, r_customer.email, r_customer.password)
        account_settings = self.browser.wait_element_presented(
            self.driver, self.sign_in_page.locators.ACCOUNT_SETTINGS_SELECTED, self.delay + 5)
        assert account_settings is not None
        assert account_settings is not False
        logger.logger.info("Test {0},CustomerID {1}".format(test_case, r_customer.customer_id))
        logger.logger.info("==================== TEST IS PASSED ====================")

    @automation_logger(logger)
    def test_close_browser(self):
        self.browser.close_browser(self.driver)
