<<<<<<< a6ac884835aaa047de5b5f6bf0e391f6806c43ed:tests/me_admin/locators/login_page_locators.py
# !/usr/bin/env python
# -*- coding: utf8 -*-


class LogInPageLocators(object):
    USERNAME_FIELD_ID = "user"
    PASSWORD_FIELD_ID = "logon-form-password"
    LOGIN_BUTTON = "//*[@class='btn btn-primary'][contains(.,'Log In')]"
=======
# !/usr/bin/env python
# -*- coding: utf8 -*-


class LogInPageLocators(object):
    USERNAME_FIELD = "user"
    PASSWORD_FIELD = "logon-form-password"
    LOGIN_BUTTON = "//*[@class='btn btn-primary'][contains(.,'Log In')]"
>>>>>>> 46d3ea0049230292881d76fb45bbfa6fde5f95e8:tests/tests_me_admin/locators/login_page_locators.py
    NASDAQ_LOGO = "//*[@class='navbar-brand'][contains(text(),'Nasdaq ME')]"