# !/usr/bin/env python
# -*- coding: utf8 -*-


class OpenAccountPageLocators(object):
    FIRST_NAME_FIELD = "//input[@name='firstName'][@placeholder='First name']"
    LAST_NAME_FIELD = "//input[@name='lastName'][@placeholder='Last name']"
    EMAIL_FIELD = "//input[@name='email'][@placeholder='Email address']"
    PASSWORD_FIELD = "//input[@name='password'][@placeholder='Password']"
    CAPTCHA = "//div[@class='recaptcha-checkbox-checkmark'][@role='presentation']"
    CREATE_ACCOUNT_BUTTON = "//input[@class='formButton'][@value='Create Account']"
    NEWSLETTERS_CHECKBOX = "//div[@class='receivePromoEmail']//span[@class='checkmark']"
    CERTIFY_CHECKBOX = "//div[@class='acceptTerms']//span[@class='checkmark']"
    PASSWORD_NOT_SECURE = "//span[@class='text'][contains(text(),'Password is not secure')]"
    
    