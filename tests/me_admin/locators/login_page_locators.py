# !/usr/bin/env python
# -*- coding: utf8 -*-


class LogInPageLocators(object):
    USERNAME_FIELD = "user"
    PASSWORD_FIELD = "logon-form-password"
    LOGIN_BUTTON = "//*[@class='btn btn-primary'][contains(.,'Log In')]"
    NASDAQ_LOGO = "//*[@class='navbar-brand'][contains(text(),'Nasdaq ME')]"