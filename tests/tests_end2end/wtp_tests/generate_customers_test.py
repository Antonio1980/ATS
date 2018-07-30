# !/usr/bin/env python
# -*- coding: utf8 -*-

import random
import string
import pytest
from src.base.enums import Browsers
from src.drivers.webdriver_factory import WebDriverFactory
from tests.tests_web_platform.pages.home_page import HomePage
from tests.tests_web_platform.pages.signup_page import SignUpPage
from src.base.instruments import get_redis_keys, get_redis_value, write_file_user, get_redis_token, parse_redis_token


def _email_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


generator = _email_generator


@pytest.mark.parametrize('i', range(50))
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
    customers = home_page.WTP_TESTS_CUSTOMERS
    driver = WebDriverFactory.get_browser(Browsers.CHROME.value)
    delay = 3
    customer_id = ""
    result1, result2, result3, result4, result5, result6, result7, result8, result9, result10 = \
        False, False, False, False, False, False, False, False, False, False
    try:
        random.seed(i)
        result1 = home_page.open_signup_page(driver, delay)
        result2 = signup_page.fill_signup_form(driver, username, email, password, )
        customer_id = signup_page.execute_js(driver, signup_page.script_customer_id)
        keys = get_redis_keys("email_validation_token*")
        token_keys = parse_redis_token(keys, "b'")
        token = get_redis_token(token_keys, customer_id)
        url = signup_page.wtp_open_account_url + "?validation_token=" + token + "&email=" + username + "%40mailinator.com"
        result3 = signup_page.go_by_token_url(driver, url)
        result4 = signup_page.add_phone(driver, phone)
        sms_code = get_redis_value(customer_id)
        result5 = signup_page.enter_phone_code(driver, sms_code)
        result6 = signup_page.fill_personal_details(driver, birthday, zip_, city)
        result7 = signup_page.fill_client_checklist_1(driver, "Federation of Federations", "freestyle")
        result8 = signup_page.fill_client_checklist_2(driver, "61")
        result9 = signup_page.fill_client_checklist_3(driver)
        result10 = signup_page.finish_registration(driver)
    finally:
        random.setstate(orig_state)
        if result1 and result3 and result4 and result5 and result6 and result7 and result8 and result9 and result10 \
                is True and result2 is False:
            write_file_user(email + "," + password + "," + customer_id + "\n", customers)
            username = generator()
            signup_page.close_browser(driver)
        else:
            username = generator()
            signup_page.close_browser(driver)
