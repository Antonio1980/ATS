# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from tests.tests_crm_bo.login_tests.C2590_login_test import LogInTest as crm_login
from tests.tests_crm_bo.login_tests.C2593_login_ddt_test import LogInTestDDT as crm_ddt_login
from tests.tests_crm_bo.login_tests.C2598_login_logout_test import LogInLogOutLogInTest
from tests.tests_crm_bo.login_tests.C3436_login_page_ui_test import LogInUiTest

from tests.tests_crm_bo.forgot_password_tests.C2591_forgot_password_test import ForgotPasswordTest
from tests.tests_crm_bo.forgot_password_tests.C2694_forgot_password_ddt_test import ForgotPasswordTestDDT as crm_ddtforgot
from tests.tests_crm_bo.forgot_password_tests.C3437_forgot_password_popup_ui_test import ForgotPasswordPopUpTest

from tests.tests_crm_bo.management_tests.C1132_create_user_test import CreateNewUserTest
from tests.tests_crm_bo.management_tests.C1132_create_user_ddt_test import CreateNewUserTestDDT

from tests.tests_crm_bo.customer_tests.C3408_upgrade_customer_to_depositor_test import CustomerUpgradeStatusTest
from tests.tests_crm_bo.customer_tests.C3409_add_deposit_test import AddDepositTest

from tests.tests_me_admin.login_tests.login_ddt import LogInTest as me_login

from tests.tests_web_platform.forgot_password_tests.C3558_forgot_password_ui_test import ForgotPasswordUITest
from tests.tests_web_platform.forgot_password_tests.C3666_forgot_password_ddt_test import ForgotPasswordDDTTest
from tests.tests_web_platform.forgot_password_tests.C3667_wrong_email_test import WrongEmailTest
from tests.tests_web_platform.forgot_password_tests.C3669_reset_password_email_test import ResetPasswordEmailTest

from tests.tests_web_platform.signin_tests.C3671_login_page_ui_test import SignInPageUITest
from tests.tests_web_platform.signin_tests.C3983_login_test import SignInTest
from tests.tests_web_platform.signin_tests.C3966_login_ddt_test import SignInDDTTest
from tests.tests_web_platform.signin_tests.C3962_links_on_login_page_test import LinksOnSignInPageTest
from tests.tests_web_platform.signin_tests.C3984_login_without_captcha_test import LogInWithoutCaptchaTest

from tests.tests_web_platform.signup_tests.C3963_email_verification_screen_test import EmailVerificationScreenTest
from tests.tests_web_platform.signup_tests.C3961_signup_ddt_test import SignUpDDTTest
from tests.tests_web_platform.signup_tests.C3964_links_on_email_verification_screen_test import LinksOnVerifyEmailScreenTest
from tests.tests_web_platform.signup_tests.C3690_signup_test import SignUpTest
from tests.tests_web_platform.signup_tests.C4431_signup_page_ui_test import SignUpPageUITest
from tests.tests_web_platform.signup_tests.C4432_links_on_signup_page_test import LinksOnSignUpPageTest


# loading test cases

# me admin tests
me_login_test = unittest.TestLoader().loadTestsFromTestCase(me_login)
me_login_suite = unittest.TestSuite([me_login_test, ])

# forgot password suite wtp
wtp_forgot_password_ui = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordUITest)
wtp_forgot_password_ddt = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordDDTTest)
wtp_wrong_email = unittest.TestLoader().loadTestsFromTestCase(WrongEmailTest)
wtp_reset_password = unittest.TestLoader().loadTestsFromTestCase(ResetPasswordEmailTest)

# login suite
wtp_login_ui = unittest.TestLoader().loadTestsFromTestCase(SignInPageUITest)
wtp_login = unittest.TestLoader().loadTestsFromTestCase(SignInTest)
wtp_login_ddt = unittest.TestLoader().loadTestsFromTestCase(SignInDDTTest)
wtp_login_links = unittest.TestLoader().loadTestsFromTestCase(LinksOnSignInPageTest)
wtp_login_without_captcha = unittest.TestLoader().loadTestsFromTestCase(LogInWithoutCaptchaTest)

# signup suite
wtp_signup_email_links = unittest.TestLoader().loadTestsFromTestCase(LinksOnVerifyEmailScreenTest)
wtp_signup_ddt = unittest.TestLoader().loadTestsFromTestCase(SignUpDDTTest)
wtp_email_screen_ui = unittest.TestLoader().loadTestsFromTestCase(EmailVerificationScreenTest)
wtp_signup = unittest.TestLoader().loadTestsFromTestCase(SignUpTest)
wtp_signup_ui = unittest.TestLoader().loadTestsFromTestCase(SignUpPageUITest)
wtp_signup_links = unittest.TestLoader().loadTestsFromTestCase(LinksOnSignUpPageTest)

# create test suites
wtp_forgot_password_suite = unittest.TestSuite([wtp_forgot_password_ui, wtp_forgot_password_ddt, wtp_wrong_email, wtp_reset_password, ])
wtp_login_suite = unittest.TestSuite([wtp_login_ui, wtp_login, wtp_login_ddt, wtp_login_links, wtp_login_without_captcha, ])
wtp_signup_suite = unittest.TestSuite([wtp_signup_email_links, wtp_signup_ddt, wtp_email_screen_ui, wtp_signup, wtp_signup_ui, wtp_signup_links, ])

# login test suite crm
crm_login_test = unittest.TestLoader().loadTestsFromTestCase(crm_login)
crm_login_logout = unittest.TestLoader().loadTestsFromTestCase(LogInLogOutLogInTest)
crm_login_ddt = unittest.TestLoader().loadTestsFromTestCase(crm_ddt_login)
crm_login_ui = unittest.TestLoader().loadTestsFromTestCase(LogInUiTest)

# forgot password test suite
crm_forgot_password = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordTest)
crm_forgot_password_ddt = unittest.TestLoader().loadTestsFromTestCase(crm_ddtforgot)
crm_forgot_password_popup = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordPopUpTest)

# management test suite
crm_create_new_user = unittest.TestLoader().loadTestsFromTestCase(CreateNewUserTest)
crm_create_new_user_ddt = unittest.TestLoader().loadTestsFromTestCase(CreateNewUserTestDDT)

# customer test suite
crm_upgrade_customer = unittest.TestLoader().loadTestsFromTestCase(CustomerUpgradeStatusTest)
crm_add_deposit = unittest.TestLoader().loadTestsFromTestCase(AddDepositTest)

# create test suites
crm_login_suite = unittest.TestSuite([crm_login_test, crm_login_logout, crm_login_ddt, crm_login_ui, ])
crm_forgot_password_suite = unittest.TestSuite([crm_forgot_password, crm_forgot_password_ddt, crm_forgot_password_popup, ])
crm_management_suite = unittest.TestSuite([crm_create_new_user, crm_create_new_user_ddt, ])
crm_customer_suite = unittest.TestSuite([crm_upgrade_customer, crm_add_deposit, ])

# execute me test suite
unittest.TextTestRunner(verbosity=2).run(me_login_suite)

# execute test suite
unittest.TextTestRunner(verbosity=2).run(crm_login_suite)
unittest.TextTestRunner(verbosity=2).run(crm_forgot_password_suite)
unittest.TextTestRunner(verbosity=2).run(crm_management_suite)
unittest.TextTestRunner(verbosity=2).run(crm_customer_suite)

# execute test suite according "one by one" ordering.
unittest.TextTestRunner(verbosity=2).run(wtp_login_suite)
unittest.TextTestRunner(verbosity=2).run(wtp_forgot_password_suite)
unittest.TextTestRunner(verbosity=2).run(wtp_signup_suite)
