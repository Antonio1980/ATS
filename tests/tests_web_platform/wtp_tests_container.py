# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from tests.tests_web_platform.end2end_tests.C3668_forgot_password_test import ForgotPasswordStandAloneTest
from tests.tests_web_platform.end2end_tests.C3750_sign_up_with_given_email_remote_test import SignUpWithGivenEmailRemoteTest
from tests.tests_web_platform.end2end_tests.C3750_sign_up_with_given_email_test import SignUpWithGivenEmailTest
from tests.tests_web_platform.end2end_tests.C3750_sign_up_with_random_email_test import SignUpWithRandomEmailTest
from tests.tests_web_platform.end2end_tests.C3750_signup_full_flow_test import SignUpFullFlowRedisTest

from tests.tests_web_platform.forgot_password_tests.C3558_forgot_password_ui_test import ForgotPasswordUITest
from tests.tests_web_platform.forgot_password_tests.C3666_forgot_password_ddt_test import ForgotPasswordDDTTest
from tests.tests_web_platform.forgot_password_tests.C3667_wrong_email_test import WrongEmailTest
from tests.tests_web_platform.forgot_password_tests.C3669_reset_password_email_test import ResetPasswordEmailTest
from tests.tests_web_platform.forgot_password_tests.C3668_forgot_password_full_flow_test import ForgotPasswordFullFlowTest

from tests.tests_web_platform.signin_tests.C3671_signin_page_ui_test import SignInPageUITest
from tests.tests_web_platform.signin_tests.C3983_signin_positive_test import SignInTest
from tests.tests_web_platform.signin_tests.C3966_signin_ddt_test import SignInDDTTest
from tests.tests_web_platform.signin_tests.C3962_links_on_signin_page_test import LinksOnSignInPageTest
from tests.tests_web_platform.signin_tests.C3984_signin_without_captcha_test import LogInWithoutCaptchaTest

from tests.tests_web_platform.signup_tests.C3963_email_verification_screen_test import EmailVerificationScreenTest
from tests.tests_web_platform.signup_tests.C3961_fill_signup_form_ddt_test import SignUpDDTTest
from tests.tests_web_platform.signup_tests.C3964_links_on_email_verification_screen_test import LinksOnVerifyEmailScreenTest
from tests.tests_web_platform.signup_tests.C3690_fill_signup_form_test import SignUpTest
from tests.tests_web_platform.signup_tests.C4431_signup_page_ui_test import SignUpPageUITest
from tests.tests_web_platform.signup_tests.C4432_links_on_signup_page_test import LinksOnSignUpPageTest
from tests.tests_web_platform.signup_tests.C3750_sign_up_full_flow_test import SignUpFullFlowTest


# loading test cases

# e2e tests
forgot_password = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordStandAloneTest)
signup_remote = unittest.TestLoader().loadTestsFromTestCase(SignUpWithGivenEmailRemoteTest)
signup_standalone = unittest.TestLoader().loadTestsFromTestCase(SignUpWithGivenEmailTest)
signup_random = unittest.TestLoader().loadTestsFromTestCase(SignUpWithRandomEmailTest)
signup_redis = unittest.TestLoader().loadTestsFromTestCase(SignUpFullFlowRedisTest)

# forgot password tests
forgot_password_ui = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordUITest)
forgot_password_ddt = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordDDTTest)
wrong_email = unittest.TestLoader().loadTestsFromTestCase(WrongEmailTest)
reset_password = unittest.TestLoader().loadTestsFromTestCase(ResetPasswordEmailTest)
forgot_full_flow = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordFullFlowTest)

# sign_in tests
signin_ui = unittest.TestLoader().loadTestsFromTestCase(SignInPageUITest)
signin = unittest.TestLoader().loadTestsFromTestCase(SignInTest)
signin_ddt = unittest.TestLoader().loadTestsFromTestCase(SignInDDTTest)
signin_links = unittest.TestLoader().loadTestsFromTestCase(LinksOnSignInPageTest)
signin_without_captcha = unittest.TestLoader().loadTestsFromTestCase(LogInWithoutCaptchaTest)

# signup tests
signup_email_links = unittest.TestLoader().loadTestsFromTestCase(LinksOnVerifyEmailScreenTest)
signup_ddt = unittest.TestLoader().loadTestsFromTestCase(SignUpDDTTest)
email_screen_ui = unittest.TestLoader().loadTestsFromTestCase(EmailVerificationScreenTest)
signup = unittest.TestLoader().loadTestsFromTestCase(SignUpTest)
signup_ui = unittest.TestLoader().loadTestsFromTestCase(SignUpPageUITest)
signup_links = unittest.TestLoader().loadTestsFromTestCase(LinksOnSignUpPageTest)
signup_full_flow = unittest.TestLoader().loadTestsFromTestCase(SignUpFullFlowTest)

# loading test suites
e2e_suite = unittest.TestSuite([forgot_password, signup_remote, signup_standalone, signup_random, signup_redis, ])

forgot_password_suite = unittest.TestSuite([forgot_password_ui, forgot_password_ddt, wrong_email, reset_password,
                                            forgot_full_flow, ])

login_suite = unittest.TestSuite([signin_ui, signin, signin_ddt, signin_links, signin_without_captcha, ])

signup_suite = unittest.TestSuite([signup_email_links, signup_ddt, email_screen_ui, signup, signup_ui, signup_links,
                                   signup_full_flow, ])

# execute test suites according "one by one" ordering.
unittest.TextTestRunner(verbosity=2).run(login_suite)
unittest.TextTestRunner(verbosity=2).run(forgot_password_suite)
unittest.TextTestRunner(verbosity=2).run(signup_suite)



