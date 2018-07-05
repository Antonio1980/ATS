# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.terminal import Terminal
from src.test_utils.terminal_utils import *


class SmokeTest(unittest.TestCase, Terminal):
    @classmethod
    def setUpClass(cls):
        cls.set_up_class()

    @classmethod
    @test(groups=['services', 'smoke'])
    def test_smoke_services(cls):
        print(NEWMAN_RUN)
        print(CURL_RUN+HOST)
        cls.run_newman(NEWMAN_RUN)
        cls.run_command_out(CURL_RUN, CURL_HTML, HOST)
        cls.run_command_in(SEND_MAIL_REPORT, NEWMAN_OUTPUT)

    @classmethod
    @test(groups=['unit'])
    def test_for_test_smoke(cls):
        cls.get_cur_date()
        print("OUTPUT______________________")
        print(TERMINAL_OUTPUT)
        print("PING______________________")
        print(cls.ping_host(HOST))
        print("PWD______________________")
        print(cls.run_command_out(PWD, TERMINAL_OUTPUT))
        print("LS______________________")
        print(cls.run_command_out(LS, TERMINAL_OUTPUT))
        print("CD______________________")
        print(cls.run_cd(test_utils_dir))
        print("PWD______________________")
        print(cls.run_command_out(PWD, TERMINAL_OUTPUT))
        print("LS______________________")
        print(cls.run_command_out(LS, TERMINAL_OUTPUT))
        print("CHMOD______________________")
        print(cls.run_command_in(CHMOD, NEWMAN_BASH))


