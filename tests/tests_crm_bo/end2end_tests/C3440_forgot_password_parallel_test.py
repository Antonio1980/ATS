# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
from queue import Queue
from threading import Thread
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from tests.tests_crm_bo.pages.home_page import HomePage
from tests.tests_crm_bo.pages.login_page import LogInPage
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_crm_bo.pages.create_user_page import CreateUserPage
from tests.tests_crm_bo.pages.users_management_page import UsersManagementPage

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


def test_forgot_password_full_flow(_q):
    driver = None
    test_case = '3440'
    phone = '123456789'
    home_page = HomePage()
    login_page = LogInPage()
    create_user_page = CreateUserPage()
    new_email = create_user_page.email
    test_run = BaseConfig.TESTRAIL_RUN
    sid_token = create_user_page.sid_token
    users_file = BaseConfig.CRM_TESTS_USERS
    user_management_page = UsersManagementPage()
    time_stamp = create_user_page.time_stamp
    login_username = login_page.login_username
    login_password = login_page.login_password
    new_username = create_user_page.guerrilla_username
    first_last_name = create_user_page.first_last_name

    while q.empty() is False:
        try:
            _browser = q.get()
            delay, new_password = 5, ""
            driver = WebDriverFactory.get_remote_driver(_browser)
            user_details = {'first_last_name': first_last_name, 'phone': phone, 'username': new_username,
                            'language': "eng", 'permissions': "sup", 'status': "act", 'user_type': "Admin"}
            step1, step2, step3, step4, step5, step6, step7, step8, step9 = False, False, False, False, False, False, False, False, False
            try:
                step1 = login_page.login(driver, login_username, login_password)
                step2 = home_page.go_to_management_inset_with_users_option(driver)
                step3 = user_management_page.click_on_create_new_user(driver)
                step4 = create_user_page.fill_user_details(driver, new_email, user_details)
                step5 = home_page.logout(driver, delay)
                time.sleep(delay * 3)
                emails_list_response = Instruments.get_guerrilla_emails(new_username, sid_token)
                sid_token = emails_list_response[1]['sid_token']
                mail_id = str(emails_list_response[1]['list'][0]['mail_id'])
                fetch_email_response = Instruments.get_last_guerrilla_email(time_stamp, mail_id, sid_token)
                html = fetch_email_response[1]['mail_body']
                parsed_html = Instruments.parse_html(html)
                new_password = parsed_html.table.find_all('td')[1].span.string
                step6 = login_page.login(driver, new_username, new_password)
                step7 = login_page.set_new_password(driver, new_password, new_password + "Qa!Qa")
                step8 = home_page.logout(driver, delay)
                step9 = login_page.login(driver, new_username, new_password + "Qa!Qa")
            finally:
                if step1 and step2 and step3 and step4 and step5 and step6 and step7 and step8 and step9 is True:
                    Instruments.write_file_user(
                        new_email + "," + new_password + "Qa!Qa1" + "," + new_username +
                        "," + sid_token + "\n", users_file)
                    Instruments.update_test_case(test_run, test_case, 1)
                else:
                    Instruments.update_test_case(test_run, test_case, 0)
        finally:
            driver.quit()
            time.sleep(15)
            q.task_done()


for i in range(num_threads):
    runner = Thread(target=test_forgot_password_full_flow, args=(q,))
    runner.setDaemon(True)
    runner.start()

q.join()
