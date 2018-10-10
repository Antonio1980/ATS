# !/usr/bin/env python
# -*- coding: utf8 -*-

import random
import pytest
from src.base.enums import Browsers
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage

generator = Instruments.generate_user_first_last_name()


@pytest.mark.parametrize('i', range(0))
def test_generate_customers(i):
    orig_state = random.getstate()
    zip_ = "45263"
    city = "Ashdod"
    phone = "0528259547"
    password = "1Aa@<>12"
    birthday = "13/08/1980"
    home_page = HomePage()
    signup_page = SignUpPage()
    username = generator()
    email = username + "@mailinator.com"
    customers_file = BaseConfig.WTP_TESTS_CUSTOMERS
    driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
    delay = 3
    customer_id, token = "", ""
    step1, step2, step3, step4, step5, step6, step7, step8, step9, step10 = \
        False, False, False, False, False, False, False, False, False, False
    try:
        random.seed(i)
        step1 = home_page.open_signup_page(driver, delay)
        step2 = signup_page.fill_signup_form(driver, username, email, password, )
        customer_id = Browser.execute_js(driver, signup_page.script_customer_id)
        keys = Instruments.get_redis_keys("email_validation_token*")
        token_keys = Instruments.parse_redis_token(keys, "b'")
        token = Instruments.get_redis_token(token_keys, customer_id)
        url = signup_page.wtp_open_account_url + "?validation_token=" + token + "&email=" + username + "%40mailinator.com"
        step3 = signup_page.go_by_token_url(driver, url)
        step4 = signup_page.add_phone(driver, phone)
        sms_code = Instruments.get_redis_value(customer_id)
        step5 = signup_page.enter_phone_code(driver, sms_code)
        step6 = signup_page.fill_personal_details(driver, birthday, zip_, city)
        step7 = signup_page.fill_client_checklist_1(driver, "Federation of Federations", "freestyle")
        step8 = signup_page.fill_client_checklist_2(driver)
        step9 = signup_page.fill_client_checklist_3(driver)
        step10 = signup_page.finish_registration(driver)
    finally:
        random.setstate(orig_state)
        if step1 and step2 and step3 and step4 and step5 and step6 and step7 and step8 and step9 and step10 is True:
            Instruments.write_file_user(email + "," + password + "," + customer_id + "," + token + "\n", customers_file)
            username = generator()
            Browser.close_browser(driver)
        else:
            username = generator()
            Browser.close_browser(driver)
