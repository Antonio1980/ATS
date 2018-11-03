from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.base_exception import AutomationError
from selenium.webdriver.remote.webelement import WebElement
from tests.tests_web_platform.pages.base_page import BasePage
from tests.tests_web_platform.locators import signup_page_locators
from tests.tests_web_platform.pages import wtp_dashboard_url, wtp_open_account_url


class SignUpPage(BasePage):
    def __init__(self):
        super(SignUpPage, self).__init__()
        self.locators = signup_page_locators
        self.terms_url = self.wtp_base_url + "/termsOfUse.html"
        self.privacy_url = self.wtp_base_url + "/privacyPolicy.html"
        self.captcha_terms_url = "https://policies.google.com/terms?hl=en"
        self.captcha_privacy_url = "https://policies.google.com/privacy?hl=en"
        self.script_text_on_enter_phone_code = "return $('.upperText').text()"

    def go_by_token_url(self, driver, url):
        delay = 5
        try:
            self.go_to_url(driver, url)
            if self.wait_element_clickable(driver, self.locators.SEND_BUTTON, delay + 5) is not False:
                return True
            else:
                return False
        except AutomationError as e:
            print("{0} go_by_token_url failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    def fill_signup_form(self, driver, first_last_name, email, password, _element=''):
        delay = 5
        try:
            assert self.wait_url_contains(driver, wtp_open_account_url, delay)
            firstname_field = self.search_element(driver, self.locators.FIRST_NAME_FIELD, delay)
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
            certify_checkbox = self.find_element(driver, self.locators.CERTIFY_CHECKBOX)
            self.click_on_element(certify_checkbox)
            newsletters_checkbox = self.find_element(driver, self.locators.NEWSLETTERS_CHECKBOX)
            self.click_on_element(newsletters_checkbox)
            self.execute_js(driver, self.script_signup)
            self.execute_js(driver, self.script_test_token)
            create_account_button = self.search_element(driver, self.locators.CREATE_ACCOUNT_BUTTON, delay + 5)
            self.click_with_wait_and_offset(driver, create_account_button, 5, 5, 1)
            if self.wait_element_visible(driver, _element, delay) is not False:
                return True
            else:
                return False
        except AutomationError as e:
            print("{0} fill_signup_form failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    def click_on_link_on_email_screen(self, driver, url_to_check, option):
        # 1 - Email verified link, 2 - Go back link, 3 - Resend email
        delay = 5
        try:
            assert self.wait_url_contains(driver, wtp_open_account_url, delay)
            if option == 1:
                element = self.search_element(driver, self.locators.EMAIL_ALREADY_VERIFIED, delay)
            elif option == 2:
                element = self.search_element(driver, self.locators.GO_BACK_LINK, delay)
            else:
                element = self.search_element(driver, self.locators.EMAIL_NOT_ARRIVED, delay)
            self.click_on_element(element)
            return self.wait_url_contains(driver, url_to_check, delay)
        except AutomationError as e:
            print("{0} click_on_link_on_email_screen failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    def click_on_link_on_signup_page(self, driver, option):
        # 1 - Terms link, 2 - Privacy link
        delay = 3
        try:
            assert self.wait_url_contains(driver, wtp_open_account_url, delay)
            if option == 1:
                element = self.search_element(driver, self.locators.TERM_OF_USE_LINK, delay)
            else:
                element = self.search_element(driver, self.locators.PRIVACY_POLICY_LINK, delay)
            self.click_on_element(element)
        finally:
            if option == 1:
                return self.wait_url_contains(driver, self.terms_url, delay)
            else:
                return self.wait_url_contains(driver, self.privacy_url, delay)

    def add_phone(self, driver, phone, country='isra'):
        delay = 5
        try:
            assert self.wait_url_contains(driver, wtp_open_account_url, delay)
            country_dropdown = self.search_element(driver, self.locators.SELECT_COUNTRY_DROPDOWN, delay)
            self.click_on_element(country_dropdown)
            self.type_text_by_locator(driver, self.locators.SELECT_COUNTRY_FIELD, country)
            phone_field = self.find_element(driver, self.locators.PHONE_FIELD)
            self.send_keys(phone_field, phone)
            send_button = self.find_element(driver, self.locators.SEND_BUTTON)
            self.click_on_element(send_button)
            while isinstance(self.search_element(driver, self.locators.ERROR_SENDING_SMS, delay), WebElement):
                phone = Instruments.generate_phone_number()
                self.send_keys(phone_field, phone)
                send_button = self.find_element(driver, self.locators.SEND_BUTTON)
                self.click_on_element(send_button)
                break
            if self.wait_element_clickable(driver, self.locators.ANOTHER_PHONE_LINK, delay):
                return True
            else:
                return False
        except AutomationError as e:
            print("{0} click_on_link_on_email_screen failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    def enter_phone_code(self, driver, code, delay):
        try:
            assert self.wait_url_contains(driver, wtp_open_account_url, delay)
            code_field = self.find_element(driver, self.locators.CODE_FIELD)
            self.click_on_element(code_field)
            self.send_keys(code_field, code)
            self.execute_js(driver, self.script_test_token)
            submit_button = self.wait_element_clickable(driver, self.locators.SUBMIT_BUTTON, delay+5)
            self.click_on_element(submit_button)
            error_text = self.execute_js(driver, '''return $("[class='validatePhoneNumber hidden'] div[class='error fieldError hidden'] span[class='text']").text();''')
            if error_text != '':
                return False
            else:
                return True
        except AutomationError as e:
            print("{0} enter_phone_code method throws error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    def fill_personal_details(self, driver, birthday, zip_, city):
        delay = 5
        # 13/07/1980
        try:
            _birthday, _zip, _city = birthday, zip_, city
            _day = _birthday.split('/')[0]
            _month = int(_birthday.split('/')[1])-1
            _year = _birthday.split('/')[2]
            self.search_element(driver, self.locators.DATE_OF_BIRTH, delay)
            self.click_on_element_by_locator(driver, self.locators.DATE_OF_BIRTH, delay)
            year_selector = self.find_element(driver, self.locators.YEAR_SELECT)
            self.select_by_value(year_selector, _year)
            month_selector = self.find_element(driver, self.locators.MONTH_SELECT)
            self.select_by_value(month_selector, _month)
            calendar_table = self.find_element(driver, self.locators.CALENDAR_TABLE)
            self._select_from_calendar(calendar_table, _day, _month)

            gender_dropdown = self.find_element_by(driver, self.locators.GENDER_DROPDOWN_ID, "id")
            self.click_on_element(gender_dropdown)
            male_option_from_gender = self.find_element(driver, self.locators.GENDER_MALE_OPTION_FROM_DROPDOWN)
            self.click_on_element(male_option_from_gender)

            country_dropdown = self.find_element_by(driver, self.locators.COUNTRY_DROPDOWN_ID, "id")
            self.click_on_element(country_dropdown)
            input_field_country = self. find_element(driver, self.locators.INPUT_FIELD_FOR_COUNTRY)
            self.input_data(input_field_country, "Israel")

            city_field = self.find_element(driver, self.locators.CITY_FIELD)
            self.send_keys(city_field, _city)
            zip_field = self.find_element(driver, self.locators.ZIP_FIELD)
            self.send_keys(zip_field, _zip)
            address_field = self.find_element(driver, self.locators.ADDRESS_FIELD)
            self.send_keys(address_field, _city)
            next_button = self.find_element(driver, self.locators.NEXT_BUTTON)
            self.click_on_element(next_button)
            if self.wait_element_clickable(driver, self.locators.EMPLOYMENT_DROPDOWN, delay) is not False:
                return True
            else:
                return False
        except AutomationError as e:
            print("{0} fill_personal_details method throws error: {1}".format(e.__class__.__name__, e.__cause__))
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

    def fill_client_checklist_1(self, driver, business_name, occupancy, delay):
        try:
            employment_dropdown = self.find_element(driver, self.locators.EMPLOYMENT_DROPDOWN)
            self.click_on_element(employment_dropdown)
            employment_options = self.find_elements(driver, self.locators.EMPLOYMENT_OPTIONS)
            self.click_on_element(employment_options[0])
            business_name_field = self.find_element(driver, self.locators.BUSINESS_NAME_INPUT)
            self.send_keys(business_name_field, business_name)
            occupancy_field = self.find_element(driver, self.locators.OCCUPATION_INPUT)
            self.send_keys(occupancy_field, occupancy)
            industry_dropdown = self.find_element(driver, self.locators.INDUSTRY_DROPDOWN)
            self.click_on_element(industry_dropdown)
            industry_options = self.find_elements(driver, self.locators.INDUSTRY_OPTIONS)
            self.click_on_element(industry_options[0])
            next_button = self.wait_element_clickable(driver, self.locators.NEXT_BUTTON_CHECKLIST1, delay)
            self.click_on_element(next_button)
            if self.wait_element_clickable(driver, self.locators.ANNUAL_INCOME, delay) is not False:
                return True
            else:
                return False
        except AutomationError as e:
            print("{0} fill_client_checklist_1 method throws error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    def fill_client_checklist_2(self, driver, delay):
        try:
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
            if self.wait_element_clickable(driver, self.locators.NEXT_BUTTON_CHECKLIST3, delay) is not False:
                return True
            else:
                return False
        except AutomationError as e:
            print("{0} fill_client_checklist_2 method throws error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    def fill_client_checklist_3(self, driver, delay):
        try:
            document_1 = self.find_element(driver, self.locators.DOCUMENT_1)
            self.execute_js(driver, self.script_document_1)
            self.send_keys(document_1, BaseConfig.DOCUMENT_PNG)
            document_2 = self.find_element(driver, self.locators.DOCUMENT_2)
            self.execute_js(driver, self.script_document_2)
            self.send_keys(document_2, BaseConfig.DOCUMENT_PNG)
            document_3 = self.find_element(driver, self.locators.DOCUMENT_3)
            self.execute_js(driver, self.script_document_3)
            self.send_keys(document_3, BaseConfig.DOCUMENT_JPG)
            next_button = self.wait_element_clickable(driver, self.locators.NEXT_BUTTON_CHECKLIST3, delay + delay)
            self.click_with_wait_and_offset(driver, next_button, 30, 30, delay - 3)
            if self.wait_element_clickable(driver, self.locators.FINISH_BUTTON, delay) is not False:
                return True
            else:
                return False
        except AutomationError as e:
            print("{0} fill_client_checklist_3 method throws error: {1}".format(e.__class__.__name__, e.__cause__))
            return False

    def finish_registration(self, driver, delay):
        try:
            self.click_on_element_by_locator(driver, self.locators.FINISH_BUTTON, delay)
            return self.wait_url_contains(driver, wtp_dashboard_url, delay)
        except AutomationError as e:
            print("{0} finish_registration method throws error: {1}".format(e.__class__.__name__, e.__cause__))
            return False
