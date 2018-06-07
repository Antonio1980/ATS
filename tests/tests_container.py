# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from tests.crm_bo.login_tests.C2590_login_test import LogInTest
from tests.crm_bo.login_tests.C2593_login_ddt_test import LogInTestDDT
from tests.crm_bo.login_tests.C2598_login_logout_test import LogInLogOutLogInTest
from tests.crm_bo.forgot_password_tests.C2591_forgot_password_test import ForgotPasswordTest
from tests.crm_bo.forgot_password_tests.C2694_forgot_password_ddt_test import ForgotPasswordTestDDT
from tests.crm_bo.newman_tests.XXX_services_smoke import SmokeTest
from tests.me_admin.login_tests.login_ddt import LogInTest as me_login_test


# loading test cases
crm_test_login = unittest.TestLoader().loadTestsFromTestCase(LogInTest)
crm_test_login_logout = unittest.TestLoader().loadTestsFromTestCase(LogInLogOutLogInTest)
crm_test_login_ddt = unittest.TestLoader().loadTestsFromTestCase(LogInTestDDT)
crm_test_forgot_password = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordTest)
crm_test_forgot_password_ddt = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordTestDDT)
crm_test_newman_smoke = unittest.TestLoader().loadTestsFromTestCase(SmokeTest)
me_admin_test_login_ddt = unittest.TestLoader().loadTestsFromTestCase(me_login_test)

# create test suite
test_suite = unittest.TestSuite([crm_test_login, crm_test_login_logout, crm_test_login_ddt, crm_test_forgot_password, crm_test_forgot_password_ddt, crm_test_newman_smoke])
me_admin_test_suite = unittest.TestSuite([me_admin_test_login_ddt])

# execute test suite
unittest.TextTestRunner(verbosity=2).run(test_suite)
unittest.TextTestRunner(verbosity=2).run(me_admin_test_suite)