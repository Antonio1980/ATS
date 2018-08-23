# !/usr/bin/env python
# -*- coding: utf8 -*-

import re
import time
from queue import Queue
from threading import Thread
from src.base.enums import Browsers
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages import wtp_signin_page_url
from tests.tests_web_platform.pages.signin_page import SignInPage
from tests.tests_web_platform.pages.signup_page import SignUpPage
from tests.tests_web_platform.pages.forgot_password_page import ForgotPasswordPage


q = Queue(maxsize=0)

mac_chrome_details = ('Chrome', '68.0', 'OS X', 'Sierra', '1920x1080')
mac_safari_details = ('Safari', '10.1', 'OS X', 'Sierra', '1920x1080')
win_chrome_details = ('Chrome', '68.0', 'Windows', '10', '2048x1536')
win_firefox_details = ('Firefox', '58.0', 'Windows', '10', '2048x1536')
win_edge_details = ('Edge', '17.0', 'Windows', '10', '2048x1536')
browsers = [mac_chrome_details, mac_safari_details, win_chrome_details, win_firefox_details, win_edge_details, ]

for browser in browsers:
    q.put(browser)
num_threads = 5


def test_forgot_password_full_flow():
    driver = None
    test_case = '3668'
    home_page = HomePage()
    signin_page = SignInPage()
    signup_page = SignUpPage()
    password = signup_page.password
    new_password = password + "Qa"
    test_run = BaseConfig.TESTRAIL_RUN
    forgot_password_page = ForgotPasswordPage()
    results_file = BaseConfig.WTP_TESTS_RESULT
    customers_file = BaseConfig.WTP_TESTS_CUSTOMERS
    response = Instruments.get_guerrilla_email()
    email = response[1]['email_addr']
    sid_token = response[1]['sid_token']
    time_stamp = str(response[1]['email_timestamp'])
    username = re.findall(r"([\w.-]+)", email)[0]
    element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(email)
    while q.empty() is False:
        try:
            _browser = q.get()
            delay, customer_id = 5, ""
            driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
            step1, step2, step3, step4, step5, step6, step7 = False, False, False, False, False, False, False
            try:
                step1 = home_page.open_signup_page(driver, delay)
                step2 = signup_page.fill_signup_form(driver, username, email, password,
                                                      element)
                customer_id = signup_page.execute_js(driver, signup_page.script_customer_id)
                step3 = signin_page.go_by_token_url(driver, wtp_signin_page_url)
                # Option 1- forgot password, Option 2- register link
                step4 = signin_page.click_on_link(driver, 1, delay)
                step5 = forgot_password_page.fill_email_address_form(driver, email, delay)
                time.sleep(delay * 2)
                emails_list_response = Instruments.get_guerrilla_emails(username, sid_token)
                sid_token = emails_list_response[1]['sid_token']
                mail_id = str(emails_list_response[1]['list'][0]['mail_id'])
                fetch_email_response = Instruments.get_last_guerrilla_email(time_stamp, mail_id, sid_token)
                html = fetch_email_response[1]['mail_body']
                parsed_html = Instruments.parse_html(html)
                new_password_url = parsed_html.center.find_all('a')[1]['href']
                sid_token = new_password_url.split('=')[1].split('&')[0]
                step6 = forgot_password_page.go_by_token_url(driver, new_password_url)
                step7 = forgot_password_page.set_new_password(driver, new_password, new_password_url)
            finally:
                if step1 and step2 and step3 and step4 and step5 and step6 and step7 is True:
                    Instruments.write_file_user(
                        email + "," + password + "," + customer_id + "," + sid_token + "\n",
                        customers_file)
                    Instruments.write_file_result(test_case + "," + test_run + "," + "1 \n", results_file)
                    Instruments.update_test_case(test_run, test_case, 1)
                else:
                    Instruments.write_file_result(test_case + "," + test_run + "," + "0 \n", results_file)
                    Instruments.update_test_case(test_run, test_case, 0)
        finally:
            driver.quit()
            time.sleep(15)
            q.task_done()


for i in range(num_threads):
    worker = Thread(target=test_forgot_password_full_flow, args=(q,))
    worker.setDaemon(True)
    worker.start()

q.join()

