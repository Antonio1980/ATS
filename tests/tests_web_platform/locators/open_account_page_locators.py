# !/usr/bin/env python
# -*- coding: utf8 -*-


class OpenAccountPageLocators(object):
    OPEN_ACCOUNT_FRAME = "//*[@id='platformAuthDialog']"
    OPEN_ACCOUNT_BOX_ID = "openAccountDxForm"
    OPEN_ACCOUNT_BOX = "//*[@id='openAccountDxForm']"
    OPEN_ACCOUNT_LOGO = "//div[@class='title'][contains(text(),'Create your account')]"
    FIRST_NAME_FIELD = "//input[@name='firstName'][@placeholder='First name']"
    LAST_NAME_FIELD = "//input[@name='lastName'][@placeholder='Last name']"
    EMAIL_FIELD = "//input[@name='email'][@placeholder='Email address']"
    PASSWORD_FIELD = "//input[@name='password'][@placeholder='Password']"
    CAPTCHA = "//input[@name='captcha']" # "//div[@class='recaptcha-checkbox-checkmark'][@role='presentation']"
    CAPTCHA_FRAME = "//*[@class='g-recaptcha']//iframe"
    CAPTCHA_MAIN_FRAME = "//*[@class='g-recaptcha'][@data-theme='light']"
    CREATE_ACCOUNT_BUTTON = "//*[@class='registration-form-wrapper']//input[@class='formButton']" # "//input[@class='formButton'][@value='Create Account']"
    NEWSLETTERS_CHECKBOX = "//div[@class='receivePromoEmail']//span[@class='checkmark']"
    CERTIFY_CHECKBOX = "//div[@class='acceptTerms']//span[@class='checkmark']"
    PASSWORD_NOT_SECURE = "//span[@class='text'][contains(text(),'Password is not secure')]"
    TERM_OF_USE_LINK = "//a[@href='#'][contains(text(),'Terms of Use')]"
    PRIVACY_POLICY_LINK = "//a[@href='#'][contains(text(),'Privacy Policy')]"
    SIGNIN_LINK = "//a[@href='#'][contains(text(),'Sign in')]"
    
    