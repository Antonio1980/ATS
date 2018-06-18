# !/usr/bin/env python
# -*- coding: utf8 -*-

import re
import string
import random


def get_mailinator_updates(driver, email):
    try:
        pattern = r"[a-zA-Z0-9]@$"
        email_box = re.match(pattern, email)
        mailinator_box_url = "http://www.mailinator.com/v2/inbox.jsp?zone=public&query={0}#".format(email_box)
        driver.get(mailinator_box_url)
        # email_field = driver.find_element_by_xpath("//input[@id='inboxfield']")
        # email_field.send_keys(email)
        pause_button = driver.find_element_by_xpath("//*[@id='play_button']")
        pause_button.click()
        mail = driver.find_element_by_xpath("//*[@id='inboxpane']/li[1]")
        driver.implicitly_wait(3)
        mail.click()
        mail_content = driver.find_element_by_xpath("//*[@id='msgpane']")
        driver.implicitly_wait(3)
    finally:
        if mail_content is not None:
            return mail_content
        else:
            return False


def email_generator(size=8, chars=string.ascii_lowercase + string.digits):
    return ''.join(random.choice(chars) for _ in range(size))


def click_mailinator_confirm(driver, email):
    try:
        pattern = r"[a-zA-Z0-9]@$"
        email_box = re.match(pattern, email)
        mailinator_box_url = "http://www.mailinator.com/v2/inbox.jsp?zone=public&query={0}#".format(email_box)
        driver.get(mailinator_box_url)
        pause_button = driver.find_element_by_xpath("//*[@id='play_button']")
        pause_button.click()
        mail = driver.find_element_by_xpath("//*[@id='inboxpane']/li[1]")
        driver.implicitly_wait(3)
        mail.click()
        driver.implicitly_wait(3)
        verify_email_button = driver.find_element_by_xpath("//a[contains(text(),'Verify Email')]")
        verify_email_button.click()
        driver.implicitly_wait(3)
    finally:
        if mail_content is not None:
            return mail_content
        else:
            return False