# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from tests.tests_crm_bo.login_tests.C2590_login_test import LogInTest as crm_login_test
from tests.tests_crm_bo.login_tests.C2593_login_ddt_test import LogInTestDDT
from tests.tests_crm_bo.login_tests.C2598_login_logout_test import LogInLogOutLogInTest
from tests.tests_crm_bo.forgot_password_tests.C2591_forgot_password_test import ForgotPasswordTest
from tests.tests_crm_bo.forgot_password_tests.C2694_forgot_password_ddt_test import ForgotPasswordTestDDT
from tests.tests_me_admin.login_tests.login_ddt import LogInTest


# loading test cases
crm_test_login = unittest.TestLoader().loadTestsFromTestCase(crm_login_test)
crm_test_login_logout = unittest.TestLoader().loadTestsFromTestCase(LogInLogOutLogInTest)
crm_test_login_ddt = unittest.TestLoader().loadTestsFromTestCase(LogInTestDDT)
crm_test_forgot_password = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordTest)
crm_test_forgot_password_ddt = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordTestDDT)

me_admin_test_login_ddt = unittest.TestLoader().loadTestsFromTestCase(LogInTest)

# create test suite
test_suite = unittest.TestSuite([crm_test_login, crm_test_login_logout, crm_test_login_ddt, crm_test_forgot_password, crm_test_forgot_password_ddt])
me_admin_test_suite = unittest.TestSuite([me_admin_test_login_ddt])

# execute test suite
unittest.TextTestRunner(verbosity=2).run(test_suite)
unittest.TextTestRunner(verbosity=2).run(me_admin_test_suite)