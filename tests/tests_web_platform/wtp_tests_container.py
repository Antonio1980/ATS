# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
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

# forgot password suite
forgot_password_ui = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordUITest)
forgot_password_ddt = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordDDTTest)
wrong_email = unittest.TestLoader().loadTestsFromTestCase(WrongEmailTest)
reset_password = unittest.TestLoader().loadTestsFromTestCase(ResetPasswordEmailTest)

# login suite
login_ui = unittest.TestLoader().loadTestsFromTestCase(SignInPageUITest)
login = unittest.TestLoader().loadTestsFromTestCase(SignInTest)
login_ddt = unittest.TestLoader().loadTestsFromTestCase(SignInDDTTest)
login_links = unittest.TestLoader().loadTestsFromTestCase(LinksOnSignInPageTest)
login_without_captcha = unittest.TestLoader().loadTestsFromTestCase(LogInWithoutCaptchaTest)

# signup suite
signup_email_links = unittest.TestLoader().loadTestsFromTestCase(LinksOnVerifyEmailScreenTest)
registration_ddt = unittest.TestLoader().loadTestsFromTestCase(SignUpDDTTest)
email_screen_ui = unittest.TestLoader().loadTestsFromTestCase(EmailVerificationScreenTest)
signup = unittest.TestLoader().loadTestsFromTestCase(SignUpTest)
signup_ui = unittest.TestLoader().loadTestsFromTestCase(SignUpPageUITest)
signup_links = unittest.TestLoader().loadTestsFromTestCase(LinksOnSignUpPageTest)

# create test suites
forgot_password_suite = unittest.TestSuite([forgot_password_ui, forgot_password_ddt, wrong_email, reset_password, ])
login_suite = unittest.TestSuite([login_ui, login, login_ddt, login_links, login_without_captcha, ])
signup_suite = unittest.TestSuite([signup_email_links, registration_ddt, email_screen_ui, signup, signup_ui, signup_links, ])

# execute test suite according "one by one" ordering.
unittest.TextTestRunner(verbosity=2).run(login_suite)
unittest.TextTestRunner(verbosity=2).run(forgot_password_suite)
unittest.TextTestRunner(verbosity=2).run(signup_suite)