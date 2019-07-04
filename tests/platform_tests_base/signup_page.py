import time
import random
import string
from src.base import logger
from config_definitions import BaseConfig
from selenium.webdriver.common.by import By
from src.base.log_decorator import automation_logger
from selenium.common.exceptions import TimeoutException
from tests.platform_tests_base.base_page import BasePage
from selenium.webdriver.support import expected_conditions
from tests.platform_tests_base.locators import signup_page_locators
from tests.platform_tests_base import wtp_dashboard_url, wtp_open_account_url


class SignUpPage(BasePage):

    def __init__(self):
        super(SignUpPage, self).__init__()
        self.locators = signup_page_locators
        self.terms_url = self.wtp_base_url + "/termsOfUse.html"
        self.privacy_url = self.wtp_base_url + "/privacyPolicy.html"
        self.captcha_terms_url = "https://policies.google.com/terms?hl=en"
        self.captcha_privacy_url = "https://policies.google.com/privacy?hl=en"
        self.script_text_on_enter_phone_code = "return $('.upperText').text()"

    @automation_logger(logger)
    def go_by_token_url(self, driver, url):
        try:
            self.go_to_url(driver, url)
            self.wait_url_contains(driver, url, self.ui_delay)
            return True
        except Exception as e:
            logger.logger.error("{0} go_by_token_url failed with error: {1}".format(e.__class__.__name__,
                                                                                    e.__cause__), e)
            return False

    @automation_logger(logger)
    def fill_signup_form(self, driver, first_last_name, email, password, _element=''):
        try:
            assert self.wait_url_contains(driver, wtp_open_account_url, self.ui_delay)
            firstname_field = self.search_element(driver, self.locators.FIRST_NAME_FIELD, self.ui_delay)
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
            self.execute_js(driver, '$("#openAccountDxForm .captchaCode").val("test_QA_test");')
            self.execute_js(driver, self.script_test_token)
            create_account_button = self.search_element(driver, self.locators.CREATE_ACCOUNT_BUTTON, self.ui_delay)
            self.click_with_wait_and_offset(driver, create_account_button, 5, 5)
            return self.wait_element_visible(driver, _element, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} fill_signup_form failed with error: {1}".format(e.__class__.__name__,
                                                                                     e.__cause__), e)
            return False

    @automation_logger(logger)
    def click_on_link_on_email_screen(self, driver, url_to_check, option):
        # 1 - Email verified link, 2 - Go back link, 3 - Resend email
        try:
            assert self.wait_url_contains(driver, wtp_open_account_url, self.ui_delay)
            if option == 1:
                element = self.search_element(driver, self.locators.EMAIL_ALREADY_VERIFIED, self.ui_delay)
            elif option == 2:
                element = self.search_element(driver, self.locators.GO_BACK_LINK, self.ui_delay)
            else:
                element = self.search_element(driver, self.locators.EMAIL_NOT_ARRIVED, self.ui_delay)
            self.click_on_element(element)
            return self.wait_url_contains(driver, url_to_check, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} click_on_link_on_email_screen failed with error: {1}".format(e.__class__.__name__,
                                                                                                  e.__cause__), e)
            return False

    @automation_logger(logger)
    def click_on_link_on_signup_page(self, driver, option):
        # 1 - Terms link, 2 - Privacy link
        windows = []
        try:
            assert self.wait_url_contains(driver, wtp_open_account_url, self.ui_delay)
            if option == 1:
                element = self.search_element(driver, self.locators.TERM_OF_USE_LINK, self.ui_delay)
            else:
                element = self.search_element(driver, self.locators.PRIVACY_POLICY_LINK, self.ui_delay)
            self.click_on_element(element)
            windows = driver.window_handles
        finally:
            if option == 1:
                self.switch_window(driver, windows[1])
                result = self.wait_url_contains(driver, self.terms_url, self.ui_delay)
            else:
                self.switch_window(driver, windows[2])
                result = self.wait_url_contains(driver, self.privacy_url, self.ui_delay)
            self.switch_window(driver, windows[0])
            return result

    @automation_logger(logger)
    def add_phone(self, driver, phone, country='isra'):

        def sms_error():
            return self.driver_wait(driver, self.ui_delay).until(expected_conditions.visibility_of_element_located(
                (By.XPATH, self.locators.ERROR_SENDING_SMS)))

        try:
            self.execute_js(driver, self.script_test_token)
            assert self.wait_url_contains(driver, wtp_open_account_url, self.ui_delay)
            time.sleep(2.0)
            country_dropdown = self.wait_element_presented(driver, self.locators.SELECT_COUNTRY_DROPDOWN, self.ui_delay)
            self.click_on_element(country_dropdown)
            self.type_text_by_locator(driver, self.locators.SELECT_COUNTRY_FIELD, country)
            phone_field = self.find_element(driver, self.locators.PHONE_FIELD)
            self.send_keys(phone_field, phone)
            send_button = self.find_element(driver, self.locators.SEND_BUTTON)
            self.click_on_element(send_button)
            time_ = time.perf_counter() + 30.0
            try:
                while sms_error() and time_ > time.perf_counter():
                    phone = ''.join(random.choice(string.digits) for _ in range(9))
                    self.send_keys(phone_field, phone)
                    send_button = self.find_element(driver, self.locators.SEND_BUTTON)
                    self.click_with_wait_and_offset(driver, send_button)
            except TimeoutException:
                pass
            if self.wait_element_clickable(driver, self.locators.ANOTHER_PHONE_LINK, self.ui_delay):
                return True
            else:
                return False
        except Exception as e:
            logger.logger.error("{0} click_on_link_on_email_screen failed with error: {1}".format(e.__class__.__name__,
                                                                                                  e.__cause__), e)
            return False

    @automation_logger(logger)
    def enter_phone_code(self, driver, code):
        try:
            assert self.wait_url_contains(driver, wtp_open_account_url, self.ui_delay)
            code_field = self.find_element(driver, self.locators.CODE_FIELD)
            self.click_on_element(code_field)
            self.send_keys(code_field, code)
            self.execute_js(driver, self.script_test_token)
            submit_button = self.wait_element_clickable(driver, self.locators.SUBMIT_BUTTON, self.ui_delay)
            self.click_on_element(submit_button)
            error_text = self.execute_js(driver, '''return $("[class='validatePhoneNumber hidden'] div[class='error fieldError hidden'] span[class='text']").text();''')
            if error_text != '':
                return False
            else:
                return True
        except Exception as e:
            logger.logger.error("{0} enter_phone_code method throws error: {1}".format(e.__class__.__name__,
                                                                                       e.__cause__), e)
            return False

    @automation_logger(logger)
    def fill_personal_details(self, driver, birthday, zip_, city):
        # 13/07/1980
        try:
            _birthday, _zip, _city = birthday, zip_, city
            _day = _birthday.split('/')[0]
            _month = int(_birthday.split('/')[1])-1
            _year = _birthday.split('/')[2]
            day_birthday = self.wait_element_clickable(driver, self.locators.DATE_OF_BIRTH, self.ui_delay)
            self.click_on_element(day_birthday)
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
            input_field_country = self.find_element(driver, self.locators.INPUT_FIELD_FOR_COUNTRY)
            self.input_data(input_field_country, "Israel")

            city_field = self.find_element(driver, self.locators.CITY_FIELD)
            self.send_keys(city_field, _city)
            zip_field = self.find_element(driver, self.locators.ZIP_FIELD)
            self.send_keys(zip_field, _zip)
            address_field = self.find_element(driver, self.locators.ADDRESS_FIELD)
            self.send_keys(address_field, _city)
            next_button = self.find_element(driver, self.locators.NEXT_BUTTON)
            self.click_on_element(next_button)
            if self.wait_element_clickable(driver, self.locators.NEXT_BUTTON_CHECKLIST2, self.ui_delay) is not False:
                return True
            else:
                return False
        except Exception as e:
            logger.logger.error("{0} fill_personal_details method throws error: {1}".format(e.__class__.__name__,
                                                                                            e.__cause__), e)
            return False

    @staticmethod
    def _select_from_calendar(table, day, month):
        items = []
        for row in table.find_elements_by_xpath(".//tr"):
            for cell in row.find_elements_by_xpath("//td[@data-handler='selectDay'][@data-month='{0}']".format(month)):
                for item in cell.find_elements_by_xpath("//a[@class='ui-state-default'][contains(text(),'')]"):
                    items.append(item)
        for i in items:
            text = i.text
            if text.lower() == day.lower():
                return i.click()

    @automation_logger(logger)
    def fill_client_checklist_1(self, driver, script):
        try:
            self.execute_js(driver, script)
            next_button = self.find_element(driver, self.locators.NEXT_BUTTON_CHECKLIST2)
            self.click_on_element(next_button)
            if self.wait_element_clickable(driver, self.locators.NEXT_BUTTON_CHECKLIST3, self.ui_delay) is not False:
                return True
            else:
                return False
        except Exception as e:
            logger.logger.error("{0} fill_client_checklist_2 method throws error: {1}".format(e.__class__.__name__,
                                                                                              e.__cause__), e)
            return False

    @automation_logger(logger)
    def fill_client_checklist_2(self, driver):
        try:
            assert self.wait_url_contains(driver, wtp_open_account_url, self.ui_delay)
            document_1 = self.search_element(driver, self.locators.DOCUMENT_1, self.ui_delay)
            self.execute_js(driver, "$('.doc_1_1_0Hidden.hidden').show();")
            self.send_keys(document_1, BaseConfig.DOCUMENT_PNG)
            document_2 = self.find_element(driver, self.locators.DOCUMENT_2)
            self.execute_js(driver, "$('.doc_1_2_0Hidden.hidden').show();")
            self.send_keys(document_2, BaseConfig.DOCUMENT_PNG)
            document_3 = self.find_element(driver, self.locators.DOCUMENT_3)
            self.execute_js(driver, "$('.doc_2_1_0Hidden.hidden').show();")
            self.send_keys(document_3, BaseConfig.DOCUMENT_JPG)
            next_button = self.wait_element_clickable(driver, self.locators.NEXT_BUTTON_CHECKLIST3, self.ui_delay)
            self.click_with_wait_and_offset(driver, next_button, 30, 30)
            if self.wait_element_clickable(driver, self.locators.FINISH_BUTTON, self.ui_delay) is not False:
                return True
            else:
                return False
        except Exception as e:
            logger.logger.error("{0} fill_client_checklist_3 method throws error: {1}".format(e.__class__.__name__,
                                                                                              e.__cause__), e)
            return False

    @automation_logger(logger)
    def finish_registration(self, driver):
        try:
            finish_button = self.wait_element_clickable(driver, self.locators.FINISH_BUTTON, self.ui_delay)
            self.click_on_element(finish_button)
            return self.wait_url_contains(driver, wtp_dashboard_url, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} finish_registration method throws error: {1}".format(e.__class__.__name__,
                                                                                          e.__cause__), e)
            return False
