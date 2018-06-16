# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from tests.tests_crm_bo.tests_login.C2590_login_test import LogInTest as crm_login_test
from tests.tests_crm_bo.tests_login.C2593_login_ddt_test import LogInTestDDT
from tests.tests_crm_bo.tests_login.C2598_login_logout_test import LogInLogOutLogInTest
from tests.tests_crm_bo.tests_login.C3436_login_page_ui_test import LogInUiTest
from tests.tests_crm_bo.tests_forgot_password.C2591_forgot_password_test import ForgotPasswordTest
from tests.tests_crm_bo.tests_forgot_password.C2694_forgot_password_ddt_test import ForgotPasswordTestDDT
from tests.tests_crm_bo.tests_management.C1132_create_user_test import CreateNewUserTest


# loading test cases
crm_test_login = unittest.TestLoader().loadTestsFromTestCase(crm_login_test)
crm_test_login_logout = unittest.TestLoader().loadTestsFromTestCase(LogInLogOutLogInTest)
crm_test_login_ddt = unittest.TestLoader().loadTestsFromTestCase(LogInTestDDT)
crm_test_login_ui = unittest.TestLoader().loadTestsFromTestCase(LogInUiTest)

crm_test_forgot_password = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordTest)
crm_test_forgot_password_ddt = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordTestDDT)

crm_test_create_new_user = unittest.TestLoader().loadTestsFromTestCase(CreateNewUserTest)

# create test suite
test_suite_login = unittest.TestSuite([crm_test_login, crm_test_login_logout, crm_test_login_ddt, crm_test_login_ui, ])

test_suite_forgot_password = unittest.TestSuite([crm_test_forgot_password, crm_test_forgot_password_ddt, ])

test_suite_management = unittest.TestSuite([crm_test_create_new_user])

# execute test suite
unittest.TextTestRunner(verbosity=2).run(test_suite_login, )
unittest.TextTestRunner(verbosity=2).run(test_suite_forgot_password, )
unittest.TextTestRunner(verbosity=2).run(test_suite_management, )