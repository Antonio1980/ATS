# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
import xmlrunner as xmlrunner

from tests.tests_crm_bo.end2end_tests.C3440_forgot_password_remote_test import ForgotPasswordRemoteTest
from tests.tests_crm_bo.end2end_tests.C3440_forgot_password_standalone_test import ForgotPasswordStandaloneTest
from tests.tests_crm_bo.end2end_tests.C5846_reset_password_standalone_test import ResetPasswordTest

from tests.tests_crm_bo.login_tests.C2590_login_test import LogInTest
from tests.tests_crm_bo.login_tests.C2593_login_ddt_test import LogInDDTTest
from tests.tests_crm_bo.login_tests.C2598_login_logout_test import LogInLogOutLogInTest
from tests.tests_crm_bo.login_tests.C3436_login_page_ui_test import LogInUITest
from tests.tests_crm_bo.login_tests.C3440_login_with_generated_password_test import LogInWithNewPasswordTest

from tests.tests_crm_bo.forgot_password_tests.C2591_forgot_password_test import ForgotPasswordTest
from tests.tests_crm_bo.forgot_password_tests.C2694_forgot_password_ddt_test import ForgotPasswordDDTTest
from tests.tests_crm_bo.forgot_password_tests.C3437_forgot_password_po_pup_test import ForgotPasswordPopUpTest
from tests.tests_crm_bo.forgot_password_tests.C3411_set_new_password_ddt_test import NewPasswordFlowDDTTest
from tests.tests_crm_bo.forgot_password_tests.C3438_forgot_password_email_test import ForgotPasswordEmailTest
from tests.tests_crm_bo.forgot_password_tests.C3439_generate_new_password_test import GenerateNewPasswordTest
from tests.tests_crm_bo.forgot_password_tests.C3440_forgot_password_full_flow_test import ForgotPasswordFullFlowTest
from tests.tests_crm_bo.forgot_password_tests.C3441_expiered_token_test import ExpiredTokenTest

from tests.tests_crm_bo.management_tests.C5741_create_user_test import CreateNewUserTest
from tests.tests_crm_bo.management_tests.C5742_create_user_ddt_test import CreateNewUserDDTTest
from tests.tests_crm_bo.management_tests.C5844_create_user_page_ui_test import CreateNewUserUITest
from tests.tests_crm_bo.management_tests.C5845_edit_user_page_ui_test import EditNewUserUITest
from tests.tests_crm_bo.management_tests.C5846_edit_user_reset_password_test import EditUserResetPasswordTest

from tests.tests_crm_bo.change_password_tests.C3412_update_default_password_test import UpdateDefaultPasswordTest
from tests.tests_crm_bo.change_password_tests.C3502_change_password_new_user_test import ChangePasswordNewUserTest
from tests.tests_crm_bo.change_password_tests.C3503_change_password_existing_user_test import ChangePasswordExistingUserTest
from tests.tests_crm_bo.change_password_tests.C3504_change_password_with_old_password_test import ChangePasswordForgottenUserTest
from tests.tests_crm_bo.change_password_tests.C3505_change_password_screen_test import ChangePasswordScreenTest

# from tests.tests_crm_bo.customer_tests.NF_C3408_upgrade_customer_to_depositor_test import CustomerUpgradeStatusTest
# from tests.tests_crm_bo.customer_tests.NF_C3409_add_deposit_test import AddDepositTest


# loading test cases

# e2e test cases
forgot_remote = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordRemoteTest)
forgot_standalone = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordStandaloneTest)
reset_standalone = unittest.TestLoader().loadTestsFromTestCase(ResetPasswordTest)

# sign_in test cases
login = unittest.TestLoader().loadTestsFromTestCase(LogInTest)
login_logout = unittest.TestLoader().loadTestsFromTestCase(LogInLogOutLogInTest)
login_ddt = unittest.TestLoader().loadTestsFromTestCase(LogInDDTTest)
login_ui = unittest.TestLoader().loadTestsFromTestCase(LogInUITest)
login_new_password = unittest.TestLoader().loadTestsFromTestCase(LogInWithNewPasswordTest)

# forgot password test cases
forgot_password = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordTest)
forgot_password_ddt = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordDDTTest)
forgot_password_popup = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordPopUpTest)
new_password_ddt = unittest.TestLoader().loadTestsFromTestCase(NewPasswordFlowDDTTest)
forgot_password_email = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordEmailTest)
new_forgot_password = unittest.TestLoader().loadTestsFromTestCase(GenerateNewPasswordTest)
forgot_password_full_flow = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordFullFlowTest)
expired_token = unittest.TestLoader().loadTestsFromTestCase(ExpiredTokenTest)

# management test cases
create_new_user = unittest.TestLoader().loadTestsFromTestCase(CreateNewUserTest)
create_new_user_ddt = unittest.TestLoader().loadTestsFromTestCase(CreateNewUserDDTTest)
create_new_ui = unittest.TestLoader().loadTestsFromTestCase(CreateNewUserUITest)
edit_new_user_ui = unittest.TestLoader().loadTestsFromTestCase(EditNewUserUITest)
edit_user_reset_password = unittest.TestLoader().loadTestsFromTestCase(EditUserResetPasswordTest)

# change_password test cases
update_default_password = unittest.TestLoader().loadTestsFromTestCase(UpdateDefaultPasswordTest)
change_password_new_user = unittest.TestLoader().loadTestsFromTestCase(ChangePasswordNewUserTest)
change_password_existing_user = unittest.TestLoader().loadTestsFromTestCase(ChangePasswordExistingUserTest)
change_password_forgotten_user = unittest.TestLoader().loadTestsFromTestCase(ChangePasswordForgottenUserTest)
change_password_screen = unittest.TestLoader().loadTestsFromTestCase(ChangePasswordScreenTest)

# customer test cases
# upgrade_customer = unittest.TestLoader().loadTestsFromTestCase(CustomerUpgradeStatusTest)
# add_deposit = unittest.TestLoader().loadTestsFromTestCase(AddDepositTest)

# create test suites
e2d_suite = unittest.TestSuite([forgot_remote, forgot_standalone, reset_standalone, ])

login_suite = unittest.TestSuite([login, login_logout, login_ddt, login_ui, login_new_password, ])

forgot_password_suite = unittest.TestSuite([forgot_password, forgot_password_ddt, forgot_password_popup, new_password_ddt,
                                            forgot_password_email, new_forgot_password, forgot_password_full_flow,
                                            expired_token, ])

management_suite = unittest.TestSuite([create_new_user, create_new_user_ddt, create_new_ui, edit_new_user_ui,
                                       edit_user_reset_password])

change_password_suite = unittest.TestSuite([update_default_password, change_password_new_user, change_password_existing_user,
                                            change_password_forgotten_user, change_password_screen])

# customer_suite = unittest.TestSuite([upgrade_customer, add_deposit, ])

# execute test suite
unittest.TextTestRunner(verbosity=2).run(e2d_suite)
unittest.TextTestRunner(verbosity=2).run(login_suite)
unittest.TextTestRunner(verbosity=2).run(forgot_password_suite)
unittest.TextTestRunner(verbosity=2).run(change_password_suite)
    

# if __name__ == '__main__':
    # unittest.main(testRunner=xmlrunner.XMLTestRunner(output="./python_unittests_xml"))
