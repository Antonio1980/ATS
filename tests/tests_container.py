# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from tests.login_tests.C2590_login import LogInTest
from tests.login_tests.C2593_login_ddt import LogInTestDDT
from tests.login_tests.C2598_login_logout import LogInLogOutLogInTest
from tests.login_tests.C2591_forgot_password import ForgotPasswordTest
from tests.login_tests.C2694_forgot_password_ddt import ForgotPasswordTestDDT


# loading test cases
test_login = unittest.TestLoader().loadTestsFromTestCase(LogInTest)
test_login_logout = unittest.TestLoader().loadTestsFromTestCase(LogInLogOutLogInTest)
test_login_ddt = unittest.TestLoader().loadTestsFromTestCase(LogInTestDDT)
test_forgot_password = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordTest)
test_forgot_password_ddt = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordTestDDT)

# create test suite
test_suite = unittest.TestSuite([test_login, test_login_logout, test_login_ddt, test_forgot_password, test_forgot_password_ddt])

# execute test suite
unittest.TextTestRunner(verbosity=2).run(test_suite)