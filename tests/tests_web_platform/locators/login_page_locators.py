# !/usr/bin/env python
# -*- coding: utf8 -*-


class LogInPageLocators(object):
    SIGNIN_BOX = "//*[@class='content']" # "//*[@id='dialogBody']" "//*[@class='authForm popupForm']" "//*[@class='formContainer formBox']"
    SIGNIN_TITLE = "//*[@class='loginTitle'][contains(text(),'Sign in')]"
    USERNAME_FIELD = "//input[@name='email']"
    PASSWORD_FIELD = "//input[@name='passwordPopupFake']"
    PASSWORD_TRUE_FIELD = "//input[@name='password']"
    CAPTCHA = "//input[@name='captcha']"  # "//div[@class='recaptcha-checkbox-checkmark'][@role='presentation']"
    CAPTCHA_FRAME = "//*[@class='g-recaptcha']//iframe"
    CAPTCHA_MAIN_FRAME = "//*[@class='g-recaptcha'][@data-theme='light']"
    SIGNIN_BUTTON = "//input[@class='formButton']" # "//input[@value='Sign In']"
    KEEP_ME_CHECKBOX = "//*[@class='checkmark']"
    FORGOT_PASSWORD_LINK = "//*[@class='authPopupForgotPassword']" # [contains(text(),'Forgot you password?')]
    REGISTER_LINK = "//*[@class='authPopupRegister']"

