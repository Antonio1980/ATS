# !/usr/bin/env python
# -*- coding: utf8 -*-
from tests_resources.locators.base_page_locators import BasePageLocators


class LogInPageLocators(BasePageLocators):
    USERNAME_FIELD = "//*[@id='user']"
    PASSWORD_FIELD = "//*[@id='logon-form-password']"
    LOGIN_BUTTON = "//*[@class='btn btn-primary']"