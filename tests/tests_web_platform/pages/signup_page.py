from tests.tests_web_platform.pages.base_page import BasePage
from tests.tests_web_platform.locators.signup_page_locators import SignUpPageLocators


class SignUpPage(BasePage):
    def __init__(self):
        super(SignUpPage, self).__init__()
        self.locators = SignUpPageLocators()
        email_suffix = "@mailinator.com"
        self.email = self.email_generator() + email_suffix
        self.password = "1Aa@<>12"
        self.first_last_name = "QA_test_QA"
        self.phone = "0528259547"
        self.terms_url = self.wtp_base_url + "/termsOfUse.html"
        self.privacy_url = self.wtp_base_url + "/privacyPolicy.html"
        self.element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(self.email)

    def fill_signup_form(self, driver, first_last_name, email, password):
        delay = 3
        try:
            self.driver_wait(driver, delay)
            assert self.get_cur_url(driver) == self.wtp_open_account_url
            firstname_field = self.find_element(driver, self.locators.FIRST_NAME_FIELD)
            self.click_on_element(firstname_field)
            self.send_keys(firstname_field, first_last_name)
            lastname_field = self.find_element(driver, self.locators.LAST_NAME_FIELD)
            self.click_on_element(lastname_field)
            self.send_keys(lastname_field, first_last_name)
            email_field = self.find_element(driver, self.locators.EMAIL_FIELD)
            self.click_on_element(email_field)
            self.send_keys(email_field, email)
            password_field = self.find_element(driver, self.locators.PASSWORD_FIELD)
            self.click_on_element(password_field)
            self.send_keys(password_field, password)
            self.driver_wait(driver, delay)
            certify_checkbox = self.find_element(driver, self.locators.CERTIFY_CHECKBOX)
            self.click_on_element(certify_checkbox)
            newsletters_checkbox = self.find_element(driver, self.locators.NEWSLETTERS_CHECKBOX)
            self.click_on_element(newsletters_checkbox)
            self.execute_js(driver, self.script_signup)
            create_account_button = self.find_element(driver, self.locators.CREATE_ACCOUNT_BUTTON)
            self.click_on_element(create_account_button)
            self.driver_wait(driver, delay + 5)
        finally:
            if self.find_element(driver, self.element) and \
                    self.check_element_not_visible(driver, self.locators.EMAIL_ERROR, delay) and \
                    self.check_element_not_visible(driver, self.locators.PASSWORD_ERROR, delay):
                return True
            else:
                return False

    def signup_ui_test(self, driver, delay=+1):
        assert self.get_cur_url(driver) == self.wtp_open_account_url
        self.driver_wait(driver, delay + 2)
        assert self.wait_element_presented(driver, self.locators.FIRST_NAME_FIELD, delay)
        assert self.wait_element_presented(driver, self.locators.LAST_NAME_FIELD, delay)
        assert self.wait_element_presented(driver, self.locators.EMAIL_FIELD, delay)
        assert self.wait_element_presented(driver, self.locators.PASSWORD_FIELD, delay)
        assert self.wait_element_presented(driver, self.locators.CAPTCHA_FRAME, delay)
        assert self.wait_element_presented(driver, self.locators.NEWSLETTERS_CHECKBOX, delay)
        assert self.wait_element_presented(driver, self.locators.CERTIFY_CHECKBOX, delay)
        assert self.wait_element_presented(driver, self.locators.TERM_OF_USE_LINK, delay)
        assert self.wait_element_presented(driver, self.locators.PRIVACY_POLICY_LINK, delay)
        assert self.wait_element_presented(driver, self.locators.SIGNIN_LINK, delay)
        assert self.wait_element_clickable(driver, self.locators.CREATE_ACCOUNT_BUTTON, delay)
        return True

    def verify_email_screen_test(self, driver, delay=+1):
        assert self.get_cur_url(driver) == self.wtp_open_account_url
        self.driver_wait(driver, delay + 2)
        assert self.wait_element_presented(driver, self.locators.EMAIL_NOT_ARRIVED, delay)
        assert self.wait_element_presented(driver, self.locators.EMAIL_ALREADY_VERIFIED, delay)
        assert self.wait_element_presented(driver, self.locators.GO_BACK_LINK, delay)
        return True

    def click_on_link_on_email_screen(self, driver, url_to_check, option):
        delay = 3
        try:
            self.wait_driver(driver, delay)
            assert self.wtp_open_account_url == self.get_cur_url(driver)
            if option == 1:
                element = self.find_element(driver, self.locators.EMAIL_ALREADY_VERIFIED)
            elif option == 2:
                element = self.find_element(driver, self.locators.GO_BACK_LINK)
            else:
                element = self.find_element(driver, self.locators.EMAIL_NOT_ARRIVED)
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
                element = self.find_element(driver, self.locators.TERM_OF_USE_LINK)
            else:
                element = self.find_element(driver, self.locators.PRIVACY_POLICY_LINK)
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

    def add_phone(self, driver, phone):
        delay = 3
        try:
            self.wait_driver(driver, delay)
            assert self.wtp_open_account_url == self.get_cur_url(driver)
            country_dropdown = self.find_element(driver, self.locators.SELECT_COUNTRY_DROPDOWN)
            self.click_on_element(country_dropdown)
            country_field = self.type_text_by_locator(driver, self.locators.SELECT_COUNTRY_FIELD, "isra")
            phone_field = self.find_element(driver, self.locators.PHONE_FIELD)
            self.send_keys(phone_field, phone)
            send_button = self.find_element(driver, self.locators.SEND_BUTTON)
            self.click_on_element(send_button)
            self.driver_wait(driver, delay)
        finally:
            if self.wait_element_clickable(driver, self.locators.ANOTHER_PHONE_LINK, delay):
                return True
            else:
                return False

    def enter_phone_code(self, driver, code):
        delay = 3
        try:
            self.driver_wait(driver, delay)
            assert self.wtp_open_account_url == self.get_cur_url(driver)
            code_field = self.find_element(driver, self.locators.CODE_FIELD)
            self.click_on_element(code_field)
            self.send_keys(code_field, code)
            submit_button = self.find_element(driver, self.locators.SUBMIT_BUTTON)
            self.click_on_element(submit_button)
            self.driver_wait(driver, delay)
        finally:
            if self.wait_element_clickable(driver, self.locators.NEXT_BUTTON, delay):
                return True
            else:
                return False

    def go_by_token_url(self, driver, token):
        delay = 3
        if token is not None:
            try:
                self.driver_wait(driver, delay)
                self.go_to_url(driver, token)
            finally:
                if self.wait_element_clickable(driver, self.locators.SEND_BUTTON, delay + 5):
                    return True
                else:
                    return False

    def fill_personal_details(self, driver, birthday, zip, city):
        delay = 3
        # 13/07/2000
        try:
            _birthday, _zip, _city = birthday, zip, city
            _text = _birthday.split('/')[0]
            self.driver_wait(driver, delay)
            date_field = self.find_element(driver, self.locators.DATE_OF_BIRTH)
            self.click_on_element(date_field)
            calendar_table = self.find_element(driver, self.locators.CALENDAR_TABLE)
            self.select_from_table(calendar_table, _text)
            city_field = self.find_element(driver, self.locators.CITY_FIELD)
            self.click_on_element(city_field)
            self.send_keys(city_field, _city)
            zip_field = self.find_element(driver, self.locators.ZIP_FIELD)
            self.send_keys(zip_field, _zip)
            address_field = self.find_element(driver, self.locators.ADDRESS_FIELD)
            self.send_keys(address_field, _city)
            next_button = self.find_element(driver, self.locators.NEXT_BUTTON)
            self.click_on_element(next_button)
            self.driver_wait(driver, delay)
        finally:
            if self.wait_element_clickable(driver, self.locators.EMPLOYMENT_SELECT, delay+2):
                return True
            else:
                return False



        
