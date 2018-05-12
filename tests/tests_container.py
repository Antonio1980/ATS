# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest

# load test cases
from tests.login_tests.C2590_login import LogInTest
from tests.login_tests.C2598_login_logout import LogInLogOutLogInTest
from tests.login_tests.C2593_login_ddriven import LogInDDTTest
from tests.login_tests.C2591_forgot_password import ForgotPasswordTest

test_login = unittest.TestLoader().loadTestsFromTestCase(LogInTest)
test_login_logout = unittest.TestLoader().loadTestsFromTestCase(LogInLogOutLogInTest)
test_login_ddt = unittest.TestLoader().loadTestsFromTestCase(LogInDDTTest)
test_forgot_password = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordTest)

# create test suite
test_suite = unittest.TestSuite([test_login, test_login_logout, test_login_ddt, test_forgot_password])

# execute test suite
unittest.TextTestRunner(verbosity=2).run(test_suite)