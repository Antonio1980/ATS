# !/usr/bin/env python
# -*- coding: utf8 -*-

import os as _os
import subprocess
from tests_sources.test_utils.os_util import detect_os
from tests_sources.test_utils.file_util import write_file_output


class Terminal(object):
    @classmethod
    def set_up_class(self):
        if detect_os() == "windows":
            print("It's Windows OS.   ")
        else:
            print("It's kind of Unix OS.   ")

    @classmethod
    def get_cur_date(self):
        process = subprocess.check_output("date")
        print('Current date is:', process.decode("utf-8"))

    @classmethod
    def ping_host(self, host):
        process = subprocess.run(['ping', host], stdout=subprocess.PIPE)
        return process.stdout

    @classmethod
    def run_cd(self, dir_name):
        _os.chdir(dir_name)

    @classmethod
    def run_newman(self, command):
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        process = str(proc.stdout)
        return process

    @classmethod
    def run_command_out(self, command, file):
            try:
                proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate(timeout=100)[0]
                process = proc.decode("utf-8")
                write_file_output(process, file)
                return process
            except subprocess.TimeoutExpired:
                raise TimeoutError

    @classmethod
    def run_command_in(self, command, *option):
        if(option):
            list(command)
            command.append(option)
        else:
            list(command)
        try:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate(timeout=15)[0]
            return proc
        except subprocess.TimeoutExpired:
            raise TimeoutError
