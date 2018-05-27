# !/usr/bin/env python
# -*- coding: utf8 -*-


class LogInPageLocators(object):
    USERNAME_FIELD = "username" #"//*[@id='username']"
    PASSWORD_FIELD = "password" #"//*[@id='password']"
    LOGIN_BUTTON = "loginBtn" #"//*[@id='loginBtn']"
    CRM_LOGO = "//*[@class='crmLogo crmLogoOverride']"
    PASSWORD_INCORRECT_MESSAGE = "//*[@class='alert alert-danger'][contains(.,' The login details you are using are incorrect.')]"
    FORGOT_PASSWORD_LINK = "//*[@class='forgot help-block']" #"//*[@class='pull-left'][contains(.,'Forgot your password?')]"

    # Forgot password pop up
    FORGOT_POPUP = "//div[@class='modal-body']"
    POP_UP_CHECK = "//*[@aria-hidden='true'][@id='myModal']"
    SEND_BUTTON = "sendMail" #"//*[@id='sendMail']"
    CLOSE_BUTTON = "//button[@class='btn btn-default'][contains(text(),'Close')]"
    EMAIL_FIELD = "email" #"//input[@id='email']"
    ERROR_MESSAGE = "errorMsg" #"//span[@id='errorMsg'][contains(text(),'Please enter a valid email address')]"
    MESSAGE_POPUP = "//*[contains(text(),'   Change your password in two easy steps. This helps to keep your new password secure.   ')]"
    NOTE_POPUP = "//*[@class='modal-note'][contains(text(),'  Note that in order to use this features, you must already have a valid email address and be an active user.   ')]"