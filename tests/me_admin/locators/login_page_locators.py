# !/usr/bin/env python
# -*- coding: utf8 -*-


class LogInPageLocators():
    USERNAME_FIELD = "user" #"//*[@id='user']"
    PASSWORD_FIELD = "logon-form-password" #"//*[@id='logon-form-password']"
    LOGIN_BUTTON = "//*[@class='btn btn-primary'][contains(.,'Log In')]"
    BODY = "//body"