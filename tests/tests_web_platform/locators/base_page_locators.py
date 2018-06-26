# !/usr/bin/env python
# -*- coding: utf8 -*-


class BasePageLocators(object):
    CHANGE_PASSWORD_BUTTON = "//a[@href='{{.changePasswordUrl}}']"
    VERIFY_EMAIL_BUTTON = "//a[contains(text(),'Verify Email')]"
    PAUSE_BUTTON_ID = "play_button" # "//*[@id='play_button']"
    MAIL_CONTENT_ID = "msgpane" # "//*[@id='msgpane']"
    FIRST_EMAIL = "//*[@id='inboxpane']/li[1]"
