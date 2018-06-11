# !/usr/bin/env python
# -*- coding: utf8 -*-


class LogInPageLocators(object):
    USERNAME_FIELD_ID = "user"
    PASSWORD_FIELD_ID = "logon-form-password"
    LOGIN_BUTTON = "//*[@class='btn btn-primary'][contains(.,'Log In')]"
    NASDAQ_LOGO = "//*[@class='navbar-brand'][contains(text(),'Nasdaq ME')]"