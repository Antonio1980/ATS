# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest

# load test cases
from tests.tests_login.C2590_login_positive import LogInTestPositive
from tests.tests_login.C2593_login_ddriven import LogInTestDDT
from tests.tests_login.C2591_forgot_password import ForgotPassword

test_login = unittest.TestLoader().loadTestsFromTestCase(LogInTestPositive)
test_login_ddt = unittest.TestLoader().loadTestsFromTestCase(LogInTestDDT)
test_forgot_password = unittest.TestLoader().loadTestsFromTestCase(ForgotPassword)

# create test suite
test_suite = unittest.TestSuite([test_login, test_login_ddt, test_forgot_password])

# execute test suite
unittest.TextTestRunner(verbosity=2).run(test_suite)