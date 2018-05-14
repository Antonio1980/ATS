# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
<<<<<<< HEAD
<<<<<<< HEAD
from proboscis import test
from ddt import ddt, data, unpack
=======
from ddt import ddt, data, unpack
from proboscis import test
>>>>>>> 83d150a... forgot data driven added
=======
from proboscis import test
from ddt import ddt, data, unpack
>>>>>>> f84205b... readme
from tests.pages.browser import Browser
from tests.pages.login_page import LogInPage
from tests_sources.test_definitions import BaseConfig
from tests_sources.test_utils.file_util import get_csv_data


@test(groups=['end2end', 'functional', 'sanity'])
@ddt
class ForgotPasswordTestDDT(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        Browser.setUpClass("chrome")

        
    @test(groups=['login_page', 'positive'])
    @data(*get_csv_data(BaseConfig.W_TEST_FORGOT_DATA))
    @unpack
    def test_forgot_password_ddt(self, email):
        delay = 1
        LogInPage.forgot_password(delay, email)


    @classmethod
    def tearDownClass(self):
        Browser.tearDownClass()
