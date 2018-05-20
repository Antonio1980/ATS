# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from tests.base.terminal import Terminal
from tests_sources.test_utils.terminal_util import *


class SmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(self):
        self.terminal = Terminal
        self.terminal.set_up_class()

    @classmethod
    @test(groups=['services', 'smoke'])
    def test_smoke_services(self):
        print(NEWMAN_RUN)
        self.terminal.run_newman(NEWMAN_RUN)
        #self.terminal.run_command_out(NEWMAN_RUN2, NEWMAN_OUTPUT)
        self.terminal.run_command_in(SEND_MAIL_REPORT, NEWMAN_OUTPUT)


    # @classmethod
    # @test(groups=['unit'])
    # def test_for_test_smoke(self):
    #     self.terminal.get_cur_date()
    #     print("OUTPUT______________________")
    #     print(TERMINAL_OUTPUT)
    #     print("PING______________________")
    #     print(self.terminal.ping_host(HOST))
    #     print("PWD______________________")
    #     print(self.terminal.run_command_out(PWD, TERMINAL_OUTPUT))
    #     print("LS______________________")
    #     print(self.terminal.run_command_out(LS, TERMINAL_OUTPUT))
    #     print("CD______________________")
    #     print(self.terminal.run_cd(test_utils_dir))
    #     print("PWD______________________")
    #     print(self.terminal.run_command_out(PWD, TERMINAL_OUTPUT))
    #     print("LS______________________")
    #     print(self.terminal.run_command_out(LS, TERMINAL_OUTPUT))
    #     print("CHMOD______________________")
    #     print(self.terminal.run_command_in(CHMOD, NEWMAN_BASH))


