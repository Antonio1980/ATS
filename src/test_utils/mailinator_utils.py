# !/usr/bin/env python
# -*- coding: utf8 -*-

import re
from src.base.browser import Browser


def get_mailinator_updates(driver, email):
    _driver = driver
    print(email)
    pattern = r"[a-zA-Z0-9]@$"
    email_box = re.match(pattern, email)
    mailinator_box_url = "http://www.mailinator.com/v2/inbox.jsp?zone=public&query={0}#".format(email_box)
    _driver.get(mailinator_box_url)
    #email_field = driver.find_element_by_xpath("//input[@id='inboxfield']")
    #email_field.send_keys(email)
    pause_button = _driver.find_element_by_xpath("//*[@id='play_button']")
    pause_button.click()
    mail = _driver.find_element_by_xpath("//*[@id='inboxpane']/li[1]")
    _driver.implicitly_wait(3)
    mail.click()
    mail_content = _driver.find_element_by_xpath("//*[@id='msgpane']")
    _driver.implicitly_wait(3)
    return Browser.get_element_span_html(mail_content)
