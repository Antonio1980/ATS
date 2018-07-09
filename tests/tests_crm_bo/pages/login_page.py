from tests.test_definitions import BaseConfig
from tests.tests_crm_bo.pages import login_page_url
from tests.tests_crm_bo.pages.base_page import BasePage
from src.test_utils.file_utils import get_crm_credentials_positive
from tests.tests_crm_bo.locators.home_page_locators import HomePageLocators
from tests.tests_crm_bo.locators.login_page_locators import LogInPageLocators


class LogInPage(BasePage):
    def __init__(self):
        super(LogInPage, self).__init__()
        self.locators = LogInPageLocators()
        # data_file, row, column1, column2
        credentials = get_crm_credentials_positive(BaseConfig.CRM_LOGIN_DATA, 0, 0, 1)
        self.email = BaseConfig.CRM_CUSTOMER_EMAIL
        self.email_text = "An email has been sent to {0} which is the email address for your account. " \
                     "It includes information on changing and confirming your new password. " \
                     "Please reset your password within the next 24 hours.".format(self.email)
        self.username = credentials['username']
        self.password = credentials['password']

    def go_to_login_page(self, driver, url):
        self.go_to_url(driver, url)

    def login(self, driver, username, password):
        delay = 5
        try:
            self.go_to_login_page(driver, self.crm_base_url)
            assert login_page_url == self.get_cur_url(driver)
            username_field = self.find_element_by(driver, self.locators.USERNAME_FIELD_ID, "id")
            self.send_keys(username_field, username)
            password_field = self.find_element_by(driver, self.locators.PASSWORD_FIELD_ID, "id")
            self.send_keys(password_field, password)
            login_button = self.find_element_by(driver, self.locators.LOGIN_BUTTON_ID, "id")
            self.click_on_element(login_button)
            self.driver_wait(driver, delay)
        finally:
            if self.find_element_by(driver, HomePageLocators.HOME_PAGE_LOGO_ID, "id"):
                return True
            else:
                return False

    def forgot_password(self, driver, email, delay=+1):
        try:
            self.go_to_login_page(driver, self.crm_base_url)
            assert login_page_url == self.get_cur_url(driver)
            self.click_on_element_by_locator(driver, self.locators.FORGOT_PASSWORD_LINK, delay + 2)
            email_field = self.find_element_by(driver, self.locators.POPUP_EMAIL_FIELD_ID, "id")
            self.send_keys(email_field, email)
            self.driver_wait(driver, delay)
            send_button = self.find_element_by(driver, self.locators.POPUP_SEND_BUTTON_ID, "id")
            self.click_on_element(send_button)
            self.driver_wait(driver, delay)
        finally:
            if self.wait_element_presented(driver, self.locators.POPUP_CHECK, delay + 3):
                self.click_on_element_by_locator(driver, self.locators.EMAIL_POPUP_CLOSE_BUTTON, delay + 1)
                return True
            else:
                return False
