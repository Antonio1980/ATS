# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
from proboscis import test
from src.base.terminal import Terminal


class SmokeTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.terminal = Terminal()
        cls.terminal.set_up_class()

    @classmethod
    @test(groups=['services', 'smoke'])
    def test_smoke_services(cls):
        print(Terminal.NEWMAN_RUN)
        print(Terminal.CURL_RUN + Terminal.HOST)
        cls.terminal.run_newman(Terminal.NEWMAN_RUN)
        cls.terminal.run_command_out(Terminal.CURL_RUN, Terminal.CURL_HTML, Terminal.HOST)
        cls.terminal.run_command_in(Terminal.SEND_MAIL_REPORT, Terminal.NEWMAN_OUTPUT)

    @classmethod
    @test(groups=['unit'])
    def test_for_test_smoke(cls):
        cls.terminal.get_cur_date()
        print("OUTPUT______________________")
        print(Terminal.TERMINAL_OUTPUT)
        print("PING______________________")
        print(cls.terminal.ping_host(Terminal.HOST))
        print("PWD______________________")
        print(cls.terminal.run_command_out(Terminal.PWD, Terminal.TERMINAL_OUTPUT))
        print("LS______________________")
        print(cls.terminal.run_command_out(Terminal.LS, Terminal.TERMINAL_OUTPUT))
        print("CD______________________")
        #print(cls.terminal.run_cd(test_utils_dir))
        print("PWD______________________")
        print(cls.terminal.run_command_out(Terminal.PWD, Terminal.TERMINAL_OUTPUT))
        print("LS______________________")
        print(cls.terminal.run_command_out(Terminal.LS, Terminal.TERMINAL_OUTPUT))
        print("CHMOD______________________")
        print(cls.terminal.run_command_in(Terminal.CHMOD, Terminal.NEWMAN_BASH))


