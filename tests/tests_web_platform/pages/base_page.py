# !/usr/bin/env python
# -*- coding: utf8 -*-

from src.base.browser import Browser
from tests.test_definitions import BaseConfig


class BasePage(Browser):
    def __init__(self):
        self.wtp_base_url = BaseConfig.WTP_STAGING_URL
        self.script_login = '$(".formContainer.formBox input.captchaCode").val("test_test");'
        #self.script_signup = '$("input[name=\'captcha\']").val("test_test");'
        self.script_signup = '$("#openAccountDxForm .captchaCode").val("test_test");'
        self.script_forgot = '$("#dxPackageContainer_forgotPassword .captchaCode").val("test_test");'
