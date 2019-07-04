import allure
import pytest
from src.base import logger
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.signin_page import SignInPage

test_case = '8036'


@allure.title("Sign In")
@allure.description("""
    Functional test.
    Verification of SignIn by deep link to Funds ,  UI test
    1. Go by link.
    2. Verify that link redirect to login
    3. Sign In with registered customer
    4. Verify that link redirect to deep linked content.
    """)
@allure.severity(allure.severity_level.CRITICAL)
@allure.link(BaseConfig.TEST_RAIL_URL + "/index.php?/cases/view/" + test_case,
             name='Sign In and redirect by deep link myAccount')
@allure.testcase(BaseConfig.GITLAB_URL + "/signin_tests/C8036_sign_in_redirect_deep_link_funds.py",
                 "TestSignInRedirectDeepLinkFunds")
@pytest.mark.smoke
@pytest.mark.ui
@pytest.mark.incremental
@pytest.mark.usefixtures('r_time_count', 'r_customer', "web_driver")
class TestSignInRedirectDeepLinkFunds(object):

    delay = float(BaseConfig.UI_DELAY)
    browser = Browser()
    sign_in_page = SignInPage()
    url = BaseConfig.WTP_BASE_URL + '/appProxy/exchange.html?activeZone=funds'
    logger.logger.info("TEST CASE N: {0}".format(test_case))
    logger.logger.info(
        "method sign_in_redirect_deep_link_funds")

    @automation_logger(logger)
    def test_open_link(self, web_driver):
        self.browser.go_to_url(web_driver, self.url)
        session_expired = self.browser.wait_element_presented(web_driver, self.sign_in_page.locators.SESSION_EXPIRED_TITLE,
                                                              self.delay + 5)
        assert session_expired is not None
        assert session_expired is not False

    @automation_logger(logger)
    def test_sign_in(self, r_customer):
        self.sign_in_page.sign_in(self.driver, r_customer.email, r_customer.password)
        account_settings = self.browser.wait_element_presented(
            self.driver, self.sign_in_page.locators.BALANCE_SELECTED, self.delay + 5)
        assert account_settings is not None
        assert account_settings is not False
        logger.logger.info("Test {0},CustomerID {1}".format(test_case, r_customer.customer_id))
        logger.logger.info("==================== TEST IS PASSED ====================")
