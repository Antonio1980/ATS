# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest

# load test cases
from tests.tests_login.login import LogInTest
from tests.tests_login.login2 import LogInTest2

test_login = unittest.TestLoader().loadTestsFromTestCase(LogInTest)
test_login2 = unittest.TestLoader().loadTestsFromTestCase(LogInTest2)

# create test suite
test_suite = unittest.TestSuite([test_login2])

# execute test suite
unittest.TextTestRunner(verbosity=2).run(test_suite)