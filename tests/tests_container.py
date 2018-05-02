# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest

# load test cases
from tests.tests_login.login import LogInTest

test_login = unittest.TestLoader().loadTestsFromTestCase(LogInTest)

# create test suite
test_suite = unittest.TestSuite([test_login])

# execute test suite
unittest.TextTestRunner(verbosity=2).run(test_suite)