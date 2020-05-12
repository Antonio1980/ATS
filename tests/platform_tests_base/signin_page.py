from src.base import logger
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.base_page import BasePage
from tests.platform_tests_base.locators import signin_page_locators
from tests.platform_tests_base import wtp_signin_page_url, forgot_password_page_url, wtp_dashboard_url, \
    wtp_open_account_url


class SignInPage(BasePage):

    def __init__(self):
        super(SignInPage, self).__init__()
        self.locators = signin_page_locators

    @automation_logger(logger)
    def sign_in(self, driver, email, password):
        try:
            username_field = self.search_element(driver, self.locators.USERNAME_FIELD, self.ui_delay)
            self.click_on_element(username_field)
            self.send_keys(username_field, email)
            password_field_true = self.find_element(driver, self.locators.PASSWORD_FIELD_TRUE)
            password_field = self.find_element(driver, self.locators.PASSWORD_FIELD)
            self.click_on_element(password_field)
            self.click_on_element(password_field_true)
            self.send_keys(password_field_true, password)
            self.execute_js(driver, '$(".formContainer.formBox input.captchaCode").val("test_QA_test");')
            # keep_me_checkbox = self.find_element(driver, self.locators.KEEP_ME_CHECKBOX)
            # self.click_on_element(keep_me_checkbox)
            login_button = self.wait_element_clickable(driver, self.locators.SIGNIN_BUTTON, self.ui_delay)
            self.execute_js(driver, self.script_test_token)
            self.click_on_element(login_button)
            customer_logged_name = self.wait_element_presented(driver, self.locators.CUSTOMER_LOGGED_NAME, self.ui_delay)
            customer_name = customer_logged_name.__getattribute__("text").split()[0]
            logger.logger.info(F"Customer Name is {customer_name}")
            assert customer_name in email
            return self.wait_url_contains(driver, wtp_dashboard_url, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} sign_in failed with error: {1}".format(e.__class__.__name__, e.__cause__), e)
            return False

    @automation_logger(logger)
    def click_on_link(self, driver, option):
        # Option 1- forgot password, Option 2- register link
        try:
            self.wait_url_contains(driver, wtp_signin_page_url, self.ui_delay)
            if option == 1:
                link = self.search_element(driver, self.locators.FORGOT_PASSWORD_LINK, self.ui_delay)
            else:
                link = self.search_element(driver, self.locators.REGISTER_LINK, self.ui_delay)
            self.click_on_element(link)
            if option == 1:
                return self.wait_url_contains(driver, forgot_password_page_url, self.ui_delay)
            else:
                return self.wait_url_contains(driver, wtp_open_account_url, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} click_on_link failed with error: {1}".format(e.__class__.__name__,
                                                                                  e.__cause__), e)
            return False

    @automation_logger(logger)
    def go_by_token_url(self, driver, url):
        try:
            self.go_to_url(driver, url)
            if self.wait_element_clickable(driver, self.locators.SIGNIN_BUTTON, self.ui_delay) is not False:
                return True
            else:
                return False
        except Exception as e:
            logger.logger.error("{0} go_by_token_url failed with error: {1}".format(e.__class__.__name__,
                                                                                    e.__cause__), e)
            return False
