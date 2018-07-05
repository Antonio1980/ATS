# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from tests.tests_me_admin.login_tests.login_ddt import LogInTest


# loading test cases

# login test suite
login = unittest.TestLoader().loadTestsFromTestCase(LogInTest)

# create test suites
login_suite = unittest.TestSuite([login, ])

# execute test suite
# unittest.TextTestRunner(verbosity=2).run(login_suite)
