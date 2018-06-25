# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from tests.tests_web_platform.registration_tests.C3961_registration_ddt_test import RegistrationTestDDT
from tests.tests_web_platform.forgot_password_tests.C3558_forgot_password_ui_test import ForgotPasswordUiTest
from tests.tests_web_platform.registration_tests.NF_C3750_full_registration_flow_test import RegistrationFlowTest


# loading test cases
wtp_test_forgot_password = unittest.TestLoader().loadTestsFromTestCase(ForgotPasswordUiTest)

wtp_test_registration_flow = unittest.TestLoader().loadTestsFromTestCase(RegistrationFlowTest)
wtp_test_registration_ddt = unittest.TestLoader().loadTestsFromTestCase(RegistrationTestDDT)

# create test suite
wtp_test_suite = unittest.TestSuite([wtp_test_forgot_password, wtp_test_registration_flow, wtp_test_registration_ddt, ])

# execute test suite
unittest.TextTestRunner(verbosity=2).run(wtp_test_suite)