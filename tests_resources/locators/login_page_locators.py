# !/usr/bin/env python
# -*- coding: utf8 -*-


class LogInPageLocators():
    USERNAME_FIELD = "//*[@id='username']"
    PASSWORD_FIELD = "//*[@id='password']"
    LOGIN_BUTTON = "//*[@id='loginBtn']"
    CRM_LOGO = "//*[@class='crmLogo crmLogoOverride']"
    PASSWORD_INCORRECT_MESSAGE = "//*[@class='alert alert-danger'][contains(.,' The login details you are using are incorrect.')]"
    FORGOT_PASSWORD_LINK = "//*[@class='forgot help-block']/a[contains(.,'Forgot your password?')]"