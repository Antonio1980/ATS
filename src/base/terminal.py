"""
Author: Anton Shipulin.
Created: 01.08.2018
Version: 1.05
"""

import os as _os
import subprocess
from src.base.enums import OperationSystem
from src.base.instruments import Instruments


class Terminal(object):
    @classmethod
    def set_up_class(cls):
        if Instruments.detect_os() == OperationSystem.WINDOWS.value:
            print("It's Windows OS.   ")
        else:
            print("It's kind of Unix OS.   ")

    @staticmethod
    def get_cur_date():
        process = subprocess.check_output("date")
        print('Current date is:', process.decode("utf-8"))

    @staticmethod
    def ping_host(host):
        process = subprocess.run(['ping', host], stdout=subprocess.PIPE)
        return process.stdout

    @staticmethod
    def run_cd(dir_name):
        _os.chdir(dir_name)

    @staticmethod
    def run_newman(command):
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        process = str(proc.stdout)
        return process

    @staticmethod
    def run_command_out(command, file, *option, **option2):
        command = list(command)
        if option:
            command.append(option)
        if option2:
            command.append(option2)
        try:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate(
                timeout=100)[0]
            process = proc.decode("utf-8")
            Instruments.write_file_output(process, file)
            return process
        except subprocess.TimeoutExpired:
            raise TimeoutError

    @staticmethod
    def run_command_in(command, *option):
        if option:
            list(command)
            command.append(option)
        else:
            list(command)
        try:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate(
                timeout=100)[0]
            return proc
        except subprocess.TimeoutExpired:
            raise TimeoutError
