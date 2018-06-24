# !/usr/bin/env python
# -*- coding: utf8 -*-

import re
import string
import random


def email_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def get_email_updates(driver, email, action):
    change_password = "//a[contains(text(),'Change Password')]"
    verify_email = "//a[contains(text(),'Verify Email')]"
    mailinator_box_url = "http://www.mailinator.com/v2/inbox.jsp?zone=public&query={0}".format(email)
    driver.get(mailinator_box_url)
    pause_button = driver.find_element_by_xpath("//*[@id='play_button']")
    pause_button.click()
    email = driver.find_element_by_xpath("//*[@id='inboxpane']/li[1]")
    email.click()
    driver.implicitly_wait(3)
    # 1 - get_updates, 2 - click on change_pasword, 3 - click on verify_email
    if action == 1:
        _get_updates(driver)
    elif action == 2:
        _verify_email(driver, change_password)
    elif action == 3:
        _verify_email(driver, verify_email)


def _get_updates(driver):
    mail_content = driver.find_element_by_xpath("//*[@id='msgpane']")
    driver.implicitly_wait(3)
    return mail_content


def _verify_email(driver, locator):
    button = driver.find_element_by_xpath(locator)
    button.click()
    driver.implicitly_wait(3)
