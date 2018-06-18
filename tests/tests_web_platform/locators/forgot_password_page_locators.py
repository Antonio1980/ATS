# !/usr/bin/env python
# -*- coding: utf8 -*-


class ForgotPasswordPageLocators(object):
    FORGOT_PASSWORD_TITLE = "//*[@class='forgotInfo'][contains(text(),'Please enter your verified Email address')]"
    EMAIL_TEXT_FIELD = "//input[@class='popupTextInput'][@name='email']"
    SUBMIT_BUTTON = "//input[@class='forgotPasswordSubmit formButton'][@value='Submit']"