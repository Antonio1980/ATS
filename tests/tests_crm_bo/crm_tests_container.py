# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from tests.tests_crm_bo.login_tests.C2590_login_test import LogInTest
from tests.tests_crm_bo.login_tests.C2593_login_ddt_test import LogInDDTTest
from tests.tests_crm_bo.login_tests.C2598_login_logout_test import LogInLogOutLogInTest
from tests.tests_crm_bo.login_tests.C3436_login_page_ui_test import LogInUITest

from tests.tests_crm_bo.forgot_password_tests.C2591_forgot_password_test import ForgotPasswordTest
from tests.tests_crm_bo.forgot_password_tests.C2694_forgot_password_ddt_test import ForgotPasswordDDTTest
from tests.tests_crm_bo.forgot_password_tests.C3437_forgot_password_po_pup_test import ForgotPasswordPopUpTest

from tests.tests_crm_bo.management_tests.C1132_create_user_test import CreateNewUserTest
from tests.tests_crm_bo.management_tests.C1132_create_user_ddt_test import CreateNewUserDDTTest

from tests.tests_crm_bo.customer_tests.C3408_upgrade_customer_to_depositor_test import CustomerUpgradeStatusTest
from tests.tests_crm_bo.customer_tests.C3409_add_deposit_test import AddDepositTest


# loading test cases

# sign_in test suite
login = unittest.TestLoader().loadTestsFromTestCase(LogInTest)
login_logout = unittest.TestLoader().loadTestsFromTestCase(LogInLogOutLogInTest)
login_ddt = unittest.TestLoader().loadTestsFromTestCase(LogInDDTTest)
login_ui = unittest.TestLoader().loadTestsFromTestCase(LogInUITest)

# forgot password test suite
forgot_password = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordTest)
forgot_password_ddt = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordDDTTest)
forgot_password_popup = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordPopUpTest)

# management test suite
create_new_user = unittest.TestLoader().loadTestsFromTestCase(CreateNewUserTest)
create_new_user_ddt = unittest.TestLoader().loadTestsFromTestCase(CreateNewUserDDTTest)

# customer test suite
upgrade_customer = unittest.TestLoader().loadTestsFromTestCase(CustomerUpgradeStatusTest)
add_deposit = unittest.TestLoader().loadTestsFromTestCase(AddDepositTest)

# create test suites
login_suite = unittest.TestSuite([login, login_logout, login_ddt, login_ui, ])

forgot_password_suite = unittest.TestSuite([forgot_password, forgot_password_ddt, forgot_password_popup, ])

management_suite = unittest.TestSuite([create_new_user, create_new_user_ddt, ])

customer_suite = unittest.TestSuite([upgrade_customer, add_deposit, ])

# execute test suite
unittest.TextTestRunner(verbosity=2).run(login_suite)
unittest.TextTestRunner(verbosity=2).run(forgot_password_suite)
unittest.TextTestRunner(verbosity=2).run(management_suite)
unittest.TextTestRunner(verbosity=2).run(customer_suite)