# !/usr/bin/env python
# -*- coding: utf8 -*-


class BasePageLocators(object):
    CHANGE_PASSWORD_BUTTON = "//a[@href='{{.changePasswordUrl}}']"
    VERIFY_EMAIL_BUTTON = "//a[contains(text(),'Verify Email')]"
    PAUSE_BUTTON_ID = "play_button" # "//*[@id='play_button']"
    EMAIL_FRAME_ID = "msg_body" # "//*[@id='msg_body']"
    FIRST_EMAIL = "//*[@id='inboxpane']/li[1]"

