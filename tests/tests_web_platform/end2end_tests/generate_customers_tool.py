# !/usr/bin/env python
# -*- coding: utf8 -*-

import time
import random
import pytest
import string
from faker import Faker
from src.base.enums import Browsers
from src.base.customer import Customer
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages import wtp_open_account_url
from tests.tests_web_platform.pages.signup_page import SignUpPage


# username_generator = Instruments.generate_username()
def username_generator():
    fake = Faker()
    return '_'.join(fake.name().split(' '))


def generate_phone_number():
    prefix = "052"
    phone = ''
    return prefix + phone.join(random.choice(string.digits) for _ in range(7))


@pytest.mark.parametrize('i', range(6))
def test_generate_customers(i):
    orig_state = random.getstate()
    customer = Customer()
    home_page = HomePage()
    signup_page = SignUpPage()
    zip_ = customer.zip
    city = customer.city
    birthday = customer.birthday
    password = customer.password
    username = customer.username
    phone = generate_phone_number()
    delay, customer_id, token = 5, "", ""
    response = Instruments.set_guerrilla_email(username)
    sid_token = response[1]['sid_token']
    email = username + '@guerrillamailblock.com'
    time_stamp = str(response[1]['email_timestamp'])
    element = "//*[@class='userEmail'][contains(text(),'{0}')]".format(email)
    output_file = BaseConfig.TOOL_OUTPUT_FILE
    browser = customer.get_browser_functionality()
    driver = WebDriverFactory.get_driver(Browsers.CHROME.value)
    step1, step2, step3, step4, step5, step6, step7, step8, step9, step10 = \
        False, False, False, False, False, False, False, False, False, False

    try:
        random.seed(i)
        step1 = home_page.open_signup_page(driver, delay)
        step2 = signup_page.fill_signup_form(driver, username, email, password, element)
        time.sleep(delay * delay)
        customer_id = browser.execute_js(driver, customer.script_customer_id)
        keys = Instruments.get_redis_keys("email_validation_token*")
        token_keys = Instruments.parse_redis_token(keys, "b'")
        token = Instruments.get_redis_token(token_keys, customer_id)
        url = wtp_open_account_url + "?validation_token=" + token + "&email=" + username + \
              "%40guerrillamailblock.com"
        step3 = signup_page.go_by_token_url(driver, url)
        step4 = signup_page.add_phone(driver, phone)
        step5 = signup_page.enter_phone_code(driver, "123456", delay)
        step6 = signup_page.fill_personal_details(driver, birthday, zip_, city)
        step7 = signup_page.fill_client_checklist_1(driver, "Federation of Federations", "freestyle", delay)
        step8 = signup_page.fill_client_checklist_2(driver, delay)
        step9 = signup_page.fill_client_checklist_3(driver, delay)
        step10 = signup_page.finish_registration(driver, delay)
    finally:
        random.setstate(orig_state)
        if step1 and step2 and step3 and step4 and step5 and step6 and step7 and step8 and step9 and step10 is True:
            Instruments.write_file_user(email + "," + password + "," + customer_id + "," + sid_token + "," +
                                        time_stamp + "\n", output_file)
            username = username_generator()
            phone = generate_phone_number()
            browser.close_browser(driver)
        else:
            username = username_generator()
            phone = generate_phone_number()
            browser.close_browser(driver)
