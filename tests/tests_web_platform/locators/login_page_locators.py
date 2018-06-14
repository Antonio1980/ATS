# !/usr/bin/env python
# -*- coding: utf8 -*-


class LogInPageLocators(object):
    SIGNIN_BOX = "//*[@class='formContainer formBox']"
    SIGNIN_TITLE = "//*[@class='loginTitle'][contains(text(),'Sign in')]"
    USERNAME_FIELD = "//input[@name='email']"
    PASSWORD_FIELD = "//input[@name='password']"
    CAPTCHA = "//*[@id='recaptcha-anchor']"
    SIGNIN_BUTTON = "//input[@value='Sign In']"
    KEEP_ME_CHECKBOX = "//*[@class='checkmark']"
    FORGOT_PASSWORD_LINK = "//*[@class='authPopupForgotPassword']"
    REGISTER_LINK = "//*[@class='authPopupRegister']"
