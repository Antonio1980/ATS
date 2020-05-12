from src.base import logger
from src.base.log_decorator import automation_logger
from tests.platform_tests_base.base_page import BasePage
from tests.platform_tests_base import forgot_password_page_url
from tests.platform_tests_base.locators import forgot_password_page_locators


class ForgotPasswordPage(BasePage):
    
    def __init__(self):
        super(ForgotPasswordPage, self).__init__()
        self.locators = forgot_password_page_locators

    @automation_logger(logger)
    def fill_email_address_form(self, driver, email):
        try:
            assert self.wait_url_contains(driver, forgot_password_page_url, self.ui_delay)
            email_field = self.search_element(driver, self.locators.EMAIL_TEXT_FIELD, self.ui_delay)
            self.click_on_element(email_field)
            self.send_keys(email_field, email)
            self.execute_js(driver, '$("#dxPackageContainer_forgotPassword .captchaCode").val("test_QA_test");')
            self.execute_js(driver, self.script_test_token)
            submit_button = self.wait_element_clickable(driver, self.locators.SUBMIT_BUTTON, self.ui_delay)
            self.try_click(driver, submit_button, 1)
            assert self.wait_element_presented(driver, self.locators.MESSAGE, self.ui_delay)
            return True
        except Exception as e:
            logger.logger.error("{0} fill_email_address_form failed with error {1}".format(e.__class__.__name__,
                                                                                                 e.__cause__), e)
            return False

    @automation_logger(logger)
    def set_new_password(self, driver, password, new_password_url):
        flag = False
        try:
            assert self.wait_url_contains(driver, new_password_url, self.ui_delay)
            password_field = self.wait_element_presented(driver, self.locators.PASSWORD_FIELD, self.ui_delay)
            self.click_on_element(password_field)
            self.send_keys(password_field, password)
            confirm_password_field = self.find_element(driver, self.locators.CONFIRM_PASSWORD_FIELD)
            self.click_on_element(confirm_password_field)
            self.send_keys(confirm_password_field, password)
            assert self.wait_element_presented(driver, self.locators.PASSWORD_MESSAGE, self.ui_delay)
            # assert self.wait_element_presented(driver, self.locators.CONFIRM_PASSWORD_ERROR, self.ui_delay)
            confirm_button = self.search_element(driver, self.locators.CONFIRM_BUTTON, self.ui_delay)
            self.click_with_offset(driver, confirm_button, 10, 20)
            try:
                self.wait_element_clickable(driver, self.locators.CONTINUE_BUTTON, self.ui_delay)
                flag = True
                continue_button = self.search_element(driver, self.locators.CONTINUE_BUTTON, self.ui_delay)
                self.click_on_element(continue_button)
            except Exception as e:
                logger.logger.error("{0} set_new_password failed with error: {1}".format(e.__class__.__name__,
                                                                                               e.__cause__), e)
                return False
        finally:
            return flag

    @automation_logger(logger)
    def go_by_token_url(self, driver, url):
        try:
            self.go_to_url(driver, url)
            if self.wait_element_clickable(driver, self.locators.CONFIRM_BUTTON, self.ui_delay) is not False:
                return True
            else:
                return False
        except Exception as e:
            logger.logger.error("{0} go_by_token_url failed with error: {1}".format(e.__class__.__name__,
                                                                                          e.__cause__), e)
            return False
