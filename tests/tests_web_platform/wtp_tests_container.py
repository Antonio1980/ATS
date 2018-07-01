# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from tests.tests_web_platform.forgot_password_tests.C3558_forgot_password_ui_test import ForgotPasswordUiTest
from tests.tests_web_platform.forgot_password_tests.C3666_forgot_password_ddt_test import ForgotPasswordTestDDT
from tests.tests_web_platform.forgot_password_tests.C3667_wrong_email_test import WrongEmailTest
from tests.tests_web_platform.forgot_password_tests.C3669_reset_password_email_test import ResetPasswordEmailTest
from tests.tests_web_platform.signin_tests.C3671_login_page_ui_test import LogInPageUiTest
from tests.tests_web_platform.signin_tests.C3983_login_test import LogInTest
from tests.tests_web_platform.signin_tests.C3966_login_ddt_test import LogInTestDDT
from tests.tests_web_platform.signin_tests.C3962_links_on_login_page_test import LinksOnLogInPageTest
from tests.tests_web_platform.signup_tests.C3963_email_verification_ui_test import EmailVerificationScreenTest
from tests.tests_web_platform.signup_tests.C3961_signup_ddt_test import RegistrationTestDDT
from tests.tests_web_platform.signup_tests.C3964_links_on_email_verification_screen_test import LinksOnVerifyEmailScreenTest


# loading test cases
# forgot password suite
forgot_password_ui = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordUiTest)
forgot_password_ddt = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordTestDDT)
wrong_email = unittest.TestLoader().loadTestsFromTestCase(WrongEmailTest)
reset_password = unittest.TestLoader().loadTestsFromTestCase(ResetPasswordEmailTest)
# login suite
login_ui = unittest.TestLoader().loadTestsFromTestCase(LogInPageUiTest)
login = unittest.TestLoader().loadTestsFromTestCase(LogInTest)
login_ddt = unittest.TestLoader().loadTestsFromTestCase(LogInTestDDT)
login_links = unittest.TestLoader().loadTestsFromTestCase(LinksOnLogInPageTest)
email_screen_ui = unittest.TestLoader().loadTestsFromTestCase(EmailVerificationScreenTest)
# registration suite
registration_ddt = unittest.TestLoader().loadTestsFromTestCase(RegistrationTestDDT)
# signup suite
signup_links = unittest.TestLoader().loadTestsFromTestCase(LinksOnVerifyEmailScreenTest)

# create test suites
forgot_password_suite = unittest.TestSuite([forgot_password_ui, forgot_password_ddt, wrong_email, reset_password, ])
login_suite = unittest.TestSuite([login_ui, login, login_ddt, login_links, email_screen_ui, ])
registration_suite = unittest.TestSuite([registration_ddt, ])
signup_suite = unittest.TestSuite([signup_links, ])

# execute test suite according "one by one" ordering.
# unittest.TextTestRunner(verbosity=2).run(login_suite)
# unittest.TextTestRunner(verbosity=2).run(forgot_password_suite)
# unittest.TextTestRunner(verbosity=2).run(registration_suite)
# unittest.TextTestRunner(verbosity=2).run(signup_suite)