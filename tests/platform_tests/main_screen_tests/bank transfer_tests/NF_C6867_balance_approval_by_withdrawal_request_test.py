# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import unittest
from ddt import ddt, data, unpack
from src.base.browser import Browser
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.customer.registered_customer import RegisteredCustomer
from src.drivers.webdriver_factory import WebDriverFactory
from tests.platform_tests_base.home_page import HomePage
from tests.platform_tests_base.signin_page import SignInPage
from tests.platform_tests_base.fiat_withdrawal_page import FiatWithdrawalPage


@ddt
class VerifyBalanceByApprovedCRMWithdrawalRequestTest(unittest.TestCase):
    def setUp(self):
        self.test_case = '6867'
        self.home_page = HomePage()
        self.signin_page = SignInPage()
        self.customer = RegisteredCustomer()
        Instruments.change_customer_phone(self.customer.customer_id, '+972543029564', '+972543029564')
        self.customer.postman.balance_service.add_balance(int(self.customer.customer_id), 2, 10000)
        self.test_run = BaseConfig.TESTRAIL_RUN
        self.fiat_withdrawal = FiatWithdrawalPage()
        self.locators = self.fiat_withdrawal.locators
        self.browser = self.customer.get_browser_functionality()

    @data(*Instruments.get_csv_data(BaseConfig.BROWSERS))
    @unpack
    def test_verify_balance_by_approved_crm_withdrawal_request(self, browser):
        self.driver = WebDriverFactory.get_driver(browser)
        delay = 5
        step1, step2, step3, step4 = False, False, False, False
        try:
            self.customer.postman.payment_service.w(int(self.customer.customer_id), 2, 10000)
            assert self.browser.wait_element_presented(self.driver, self.locators.EUR_TITLE_ON_WITHDRAWAL_PAGE, delay)
            step4 = self.fiat_withdrawal.withdrawal_input_data(self.driver, "100")
            time.sleep(3)
            assert self.browser.wait_element_presented(self.driver, self.locators.CONFIRMATION_CODE_PAGE_FOR_EUR, delay)
            self.browser.open_new_tab(self.driver)
            new_window = self.driver.window_handles
            Browser.switch_window(self.driver, new_window[1])
            self.browser.go_to_url(self.driver, "https://www.receive-sms-online.info/972543029564-Israel")
            time.sleep(5)
            text_message = self.browser.execute_js(self.driver, self.locators.TEXT_MESSAGE_JQ)
            new_window = self.driver.window_handles
            Browser.switch_window(self.driver, new_window[0])
            code = text_message.split(': ')[1][:6]
            input_confirmation_code = self.browser.wait_element_presented(self.driver, self.locators.ENTER_CONFIRMATION_CODE_FOR_EUR, delay)
            self.browser.input_data(input_confirmation_code, code)
            assert self.browser.wait_element_presented(self.driver, self.locators.SUCCESSFUL_WITHDRAWAL_PAGE_EUR, delay)
            finish_button = self.browser.wait_element_presented(self.driver, self.locators.FINISH_BUTTON_EUR, delay)
            self.browser.click_on_element(finish_button)
            self.customer.postman.crm_service.update_customer_withdrawal(self.customer.customer_id)
            time_mail = time.time() + 30
            emails_list_response = Instruments.get_guerrilla_emails(self.customer.username, self.customer.sid_token)
            while emails_list_response[1]['list'][0]['mail_subject'] != "Forgot Password" and time_mail > time.time():
                emails_list_response = Instruments.get_guerrilla_emails(self.customer.username, self.customer.sid_token)
            sid_token = emails_list_response[1]['sid_token']
            mail_id = str(emails_list_response[1]['list'][0]['mail_id'])
            fetch_email_response = Instruments.get_last_guerrilla_email(self.customer.time_stamp, mail_id, sid_token)
            html = fetch_email_response[1]['mail_body']
            parsed_html = Instruments.parse_html(html)
            withdrowal_url = parsed_html.center.find_all('a')[1]['href']


            eur_currency_avail_balance_after = self.browser.execute_js(self.driver,
                                                                        self.locators.EUR_CURRENCY_TOTAL_BALANS_FUNDS_PAGE_JQ)






        finally:
            if step1 and step2 and step3 and step4 is True:
                Instruments.update_test_case(self.test_run, self.test_case, 1)
            else:
                print("=================TEST IS NOT PASSED==========================")
                Instruments.update_test_case(self.test_run, self.test_case, 0)

    def tearDown(self):
        Browser.close_browser(self.driver)
