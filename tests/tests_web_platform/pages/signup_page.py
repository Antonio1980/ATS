from tests.tests_web_platform.pages.base_page import BasePage
from tests.tests_web_platform.locators.signup_page_locators import SignUpPageLocators


class SignUpPage(BasePage):
    def __init__(self):
        super(SignUpPage, self).__init__()
        email_suffix = "@mailinator.com"
        self.email = self.email_generator() + email_suffix
        self.terms_url = self.wtp_base_url + "/termsOfUse.html"
        self.privacy_url = self.wtp_base_url + "/privacyPolicy.html"
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.email)
        self.email_verified_locator = SignUpPageLocators.EMAIL_ALREADY_VERIFIED
        self.go_back_locator = SignUpPageLocators.GO_BACK_TO_DX
        self.email_not_arrived_locator = SignUpPageLocators.EMAIL_NOT_ARRIVED

    def fill_signup_form(self, driver, first_last_name, email, password):
        delay = 3
        try:
            self.driver_wait(driver, delay)
            assert self.get_cur_url(driver) == self.wtp_open_account_url
            firstname_field = self.find_element(driver, SignUpPageLocators.FIRST_NAME_FIELD)
            self.click_on_element(firstname_field)
            self.send_keys(firstname_field, first_last_name)
            lastname_field = self.find_element(driver, SignUpPageLocators.LAST_NAME_FIELD)
            self.click_on_element(lastname_field)
            self.send_keys(lastname_field, first_last_name)
            email_field = self.find_element(driver, SignUpPageLocators.EMAIL_FIELD)
            self.click_on_element(email_field)
            self.send_keys(email_field, email)
            password_field = self.find_element(driver, SignUpPageLocators.PASSWORD_FIELD)
            self.click_on_element(password_field)
            self.send_keys(password_field, password)
            self.driver_wait(driver, delay)
            assert self.check_element_not_visible(driver, delay, SignUpPageLocators.PASSWORD_ERROR)
            self.driver_wait(driver, delay)
            certify_checkbox = self.find_element(driver, SignUpPageLocators.CERTIFY_CHECKBOX)
            self.click_on_element(certify_checkbox)
            newsletters_checkbox = self.find_element(driver, SignUpPageLocators.NEWSLETTERS_CHECKBOX)
            self.click_on_element(newsletters_checkbox)
            self.execute_js(driver, self.script_signup)
            create_account_button = self.find_element(driver, SignUpPageLocators.CREATE_ACCOUNT_BUTTON)
            self.click_on_element(create_account_button)
            self.driver_wait(driver, delay + 5)
        finally:
            if (self.wait_element_presented(driver, delay, self.element) and self.check_element_not_visible(driver, delay, SignUpPageLocators.EMAIL_ERROR)) \
                    or self.check_element_not_visible(driver, delay, SignUpPageLocators.PASSWORD_ERROR):
                return True
            else:
                return False

    def signup_ui_test(self, driver, delay=1):
        assert self.get_cur_url(driver) == self.wtp_open_account_url
        self.driver_wait(driver, delay + 2)
        assert self.wait_element_presented(driver, delay, SignUpPageLocators.FIRST_NAME_FIELD)
        assert self.wait_element_presented(driver, delay, SignUpPageLocators.LAST_NAME_FIELD)
        assert self.wait_element_presented(driver, delay, SignUpPageLocators.EMAIL_FIELD)
        assert self.wait_element_presented(driver, delay, SignUpPageLocators.PASSWORD_FIELD)
        assert self.wait_element_presented(driver, delay, SignUpPageLocators.CAPTCHA_FRAME)
        assert self.wait_element_presented(driver, delay, SignUpPageLocators.NEWSLETTERS_CHECKBOX)
        assert self.wait_element_presented(driver, delay, SignUpPageLocators.CERTIFY_CHECKBOX)
        assert self.wait_element_presented(driver, delay, SignUpPageLocators.TERM_OF_USE_LINK)
        assert self.wait_element_presented(driver, delay, SignUpPageLocators.PRIVACY_POLICY_LINK)
        assert self.wait_element_presented(driver, delay, SignUpPageLocators.SIGNIN_LINK)
        assert self.wait_element_clickable(driver, delay, SignUpPageLocators.CREATE_ACCOUNT_BUTTON)
        return True

    def verify_email_screen_test(self, driver, delay=1):
        assert self.get_cur_url(driver) == self.wtp_open_account_url
        self.driver_wait(driver, delay + 2)
        assert self.wait_element_presented(driver, delay, SignUpPageLocators.EMAIL_NOT_ARRIVED)
        assert self.wait_element_presented(driver, delay, SignUpPageLocators.EMAIL_ALREADY_VERIFIED)
        assert self.wait_element_presented(driver, delay, self.go_back_locator)
        return True

    def click_on_link_on_email_screen(self, driver, url_to_check, option):
        delay = 3
        try:
            self.wait_driver(driver, delay)
            assert self.wtp_open_account_url == self.get_cur_url(driver)
            if option == 1:
                element = self.find_element(driver, self.email_verified_locator)
            elif option == 2:
                element = self.find_element(driver, self.go_back_locator)
            else:
                element = self.find_element(driver, self.email_not_arrived_locator)
            self.click_on_element(element)
            self.driver_wait(driver, delay + 1)
        finally:
            if self.get_cur_url(driver) == url_to_check:
                return True
            else:
                return False

    def click_on_link_on_signup_page(self, driver, option):
        # 1 - Terms link, 2 - Privacy link
        delay = 3
        try:
            self.wait_driver(driver, delay)
            assert self.wtp_open_account_url == self.get_cur_url(driver)
            if option == 1:
                element = self.find_element(driver, SignUpPageLocators.TERM_OF_USE_LINK)
            else:
                element = self.find_element(driver, SignUpPageLocators.PRIVACY_POLICY_LINK)
            self.click_on_element(element)
            self.driver_wait(driver, delay + 1)
        finally:
            if option == 1:
                if self.get_cur_url(driver) == self.terms_url:
                    return True
                else:
                    return False
            else:
                if self.get_cur_url(driver) == self.privacy_url:
                    return True
                else:
                    return False
