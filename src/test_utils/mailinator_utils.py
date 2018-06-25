# !/usr/bin/env python
# -*- coding: utf8 -*-

import re
import string
import random
from tests.tests_web_platform.pages import wtp_open_account_url


def email_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_email_updates(driver, email, action):
    pattern2 = r"([\w\.-]+)"
    e, = email
    e = re.findall(pattern2, e)
    e = e[0]
    change_password = "//a[@href='{{.changePasswordUrl}}']"
    verify_email = "//a[@href='{{.verifyEmailUrl}}']"
    mailinator_box_url = "http://www.mailinator.com/v2/inbox.jsp?zone=public&query={0}".format(e)
    driver.get(mailinator_box_url)
    pause_button = driver.find_element_by_xpath("//*[@id='play_button']")
    pause_button.click()
    email = driver.find_element_by_xpath("//*[@id='inboxpane']/li[1]")
    email.click()
    driver.implicitly_wait(3)
    # 1 - get_updates, 2 - click on change_password, 3 - click on verify_email
    if action == 1:
        return _get_updates(driver)
    elif action == 2:
        return _click_on(driver, change_password)
    elif action == 3:
        return _click_on(driver, verify_email)


def _get_updates(driver):
    try:
        driver.implicitly_wait(3)
    finally:
        mail_content = driver.find_element_by_xpath("//*[@id='msgpane']")
        driver.implicitly_wait(3)
        if mail_content:
            return mail_content
        else:
            return False


def _click_on(driver, locator):
    try:
        driver.implicitly_wait(3)
        button = driver.find_element_by_xpath(locator)
        button.click()
        driver.implicitly_wait(3)
    finally:
        if driver.current_url() == wtp_open_account_url:
            return True
        else:
            return False
