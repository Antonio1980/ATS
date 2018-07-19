from tests.tests_web_platform.pages.base_page import BasePage
from tests.tests_web_platform.locators.signup_page_locators import SignUpPageLocators


class SignUpPage(BasePage):
    def __init__(self):
        super(SignUpPage, self).__init__()
        self.phone = "0528259547"
        self.password = "1Aa@<>12"
        self.username = "QA_test_QA"
        self.suffix = "@mailinator.com"
        self.prefix = self.email_generator()
        self.locators = SignUpPageLocators()
        self.email = self.prefix + self.suffix
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
        # 1 - Email verified link, 2 - Go back link, 3 - Resend email
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
        delay = 5
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
        delay = 5
        dr_delay = self.driver_wait(driver, delay)
        try:
            self.driver_wait(driver, delay)
            assert self.wtp_open_account_url == self.get_cur_url(driver)
            code_field = self.find_element(driver, self.locators.CODE_FIELD)
            self.click_on_element(code_field)
            self.send_keys(code_field, code)
            submit_button = self.wait_element_clickable(driver, self.locators.SUBMIT_BUTTON, delay+5)
            self.driver_wait(driver, delay+5)
            self.click_on_element(submit_button)
            self.driver_wait(driver, delay)
        finally:
            if self.wait_element_clickable(driver, self.locators.NEXT_BUTTON, delay):
                return True
            else:
                return False

    def go_by_token_url(self, driver, token):
        delay = 5
        if token is not None:
            try:
                self.driver_wait(driver, delay)
                self.go_to_url(driver, token)
                self.wait_driver(driver, delay)
            finally:
                if self.wait_element_clickable(driver, self.locators.SEND_BUTTON, delay + 5):
                    return True
                else:
                    return False

    def fill_personal_details(self, driver, birthday, zip, city):
        delay = 5
        # 13/07/1980
        try:
            _birthday, _zip, _city = birthday, zip, city
            _day = _birthday.split('/')[0]
            _month = int(_birthday.split('/')[1])-1
            _year = _birthday.split('/')[2]
            self.driver_wait(driver, delay)
            date_field = self.find_element(driver, self.locators.DATE_OF_BIRTH)
            self.click_on_element(date_field)
            year_selector = self.find_element(driver, self.locators.YEAR_SELECT)
            self.select_by_value(year_selector, _year)
            month_selector = self.find_element(driver, self.locators.MONTH_SELECT)
            self.select_by_value(month_selector, _month)
            calendar_table = self.find_element(driver, self.locators.CALENDAR_TABLE)
            self._select_from_calendar(calendar_table, _day, _month)
            self.driver_wait(driver, delay)
            city_field = self.find_element(driver, self.locators.CITY_FIELD)
            self.send_keys(city_field, _city)
            zip_field = self.find_element(driver, self.locators.ZIP_FIELD)
            self.send_keys(zip_field, _zip)
            address_field = self.find_element(driver, self.locators.ADDRESS_FIELD)
            self.send_keys(address_field, _city)
            next_button = self.find_element(driver, self.locators.NEXT_BUTTON)
            self.click_on_element(next_button)
            self.driver_wait(driver, delay)
        finally:
            if self.wait_element_clickable(driver, self.locators.EMPLOYMENT_DROPDOWN, delay+2):
                return True
            else:
                return False

    def _select_from_calendar(self, table, day, month):
        items = []
        for row in table.find_elements_by_xpath(".//tr"):
            for cell in row.find_elements_by_xpath("//td[@data-handler='selectDay'][@data-month='{0}']".format(month)):
                for item in cell.find_elements_by_xpath("//a[@class='ui-state-default'][contains(text(),'')]"):
                    items.append(item)
        for i in items:
            text = i.text
            if text.lower() == day.lower():
                return i.click()

    def fill_client_checklist_1(self, driver, business_name, occupancy):
        delay = 10
        try:
            self.driver_wait(driver, delay)
            employment_dropdown = self.find_element(driver, self.locators.EMPLOYMENT_DROPDOWN)
            self.click_on_element(employment_dropdown)
            employment_options = self.find_elements(driver, self.locators.EMPLOYMENT_OPTIONS)
            self.click_on_element(employment_options[0])
            self.driver_wait(driver, delay)
            business_name_field = self.find_element(driver, self.locators.BUSINESS_NAME_INPUT)
            self.send_keys(business_name_field, business_name)
            occupancy_field = self.find_element(driver, self.locators.OCCUPATION_INPUT)
            self.send_keys(occupancy_field, occupancy)
            industry_dropdown = self.find_element(driver, self.locators.INDUSTRY_DROPDOWN)
            self.click_on_element(industry_dropdown)
            industry_options = self.find_elements(driver, self.locators.INDUSTRY_OPTIONS)
            self.click_on_element(industry_options[0])
            next_button = self.wait_element_clickable(driver, self.locators.NEXT_BUTTON_CHECKLIST1)
            self.click_on_element(next_button)
            self.driver_wait(driver, delay)
        finally:
            if self.wait_element_clickable(driver, self.locators.ANNUAL_INCOME, delay):
                return True
            else:
                return False

    def fill_client_checklist_2(self, driver, value):
        delay = 5
        try:
            self.driver_wait(driver, delay)
            annual_dropdown = self.find_element(driver, self.locators.ANNUAL_INCOME)
            self.click_on_element(annual_dropdown)
            annual_options = self.find_elements(driver, self.locators.ANNUAL_OPTIONS)
            self.click_on_element(annual_options[0])
            source_selector = self.find_element(driver, self.locators.SOURCE_SELECT)
            self.click_on_element(source_selector)
            source_options = self.find_elements(driver, self.locators.SOURCE_OPTIONS)
            self.click_on_element(source_options[0])
            checkbox = self.find_element(driver, self.locators.INHERITANCE_CHECKBOX)
            self.click_on_element(checkbox)
            next_button = self.find_element(driver, self.locators.NEXT_BUTTON_CHECKLIST2)
            self.click_on_element(next_button)
            self.driver_wait(driver, delay)
        finally:
            if self.wait_element_clickable(driver, self.locators.NEXT_BUTTON_CHECKLIST3, delay):
                return True
            else:
                return False

    def fill_client_checklist_3(self, driver):
        delay = 5
        try:
            self.driver_wait(driver, delay)
            document_1 = self.find_element(driver, self.locators.DOCUMENT_1)
            self.execute_js(driver, self.script_document_1)
            self.send_keys(document_1, self.DOCUMENT_JPG)
            document_2 = self.find_element(driver, self.locators.DOCUMENT_2)
            self.execute_js(driver, self.script_document_2)
            self.send_keys(document_2, self.DOCUMENT_JPG)
            document_3 = self.find_element(driver, self.locators.DOCUMENT_3)
            self.execute_js(driver, self.script_document_3)
            self.send_keys(document_3, self.DOCUMENT_JPG)
            next_button = self.wait_element_clickable(driver, self.locators.NEXT_BUTTON_CHECKLIST3, delay)
            self.click_on_element(next_button)
            self.driver_wait(driver, delay)
        finally:
            if self.wait_element_clickable(driver, self.locators.FINISH_BUTTON, delay):
                return True
            else:
                return False

    def finish_registration(self, driver):
        delay = 5
        try:
            self.driver_wait(driver, delay)
            finish_button = self.find_element(driver, self.locators.FINISH_BUTTON)
            self.click_on_element(finish_button)
            self.driver_wait(driver, delay)
        finally:
            if self.wait_element_clickable(driver, self.base_locators.SIGN_UP_BUTTON, delay):
                return True
            else:
                return False
