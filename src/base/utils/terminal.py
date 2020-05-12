"""
Author: Anton Shipulin.
Created: 01.08.2018
Version: 1.05
"""

import os as _os
import subprocess

from config_definitions import BaseConfig, repository_dir
from src.base.enums import OperationSystem
from src.base.instruments import Instruments
from src.base.utils.utils import Utils

test_utils_dir = _os.path.abspath(_os.path.dirname(__file__))
UTILS_HOME_DIR = test_utils_dir
DATA_HOME_DIR = repository_dir
HOST = BaseConfig.CRM_BASE_URL

LS = ['ls', '-ltr']
CHMOD = ['chmod', '+x']
PWD = ['pwd']

COLLECTION = repository_dir + '/services_collection.json'
ENVIRONMENT = repository_dir + '/services_environment.json'
TERMINAL_OUTPUT = repository_dir + '/logs/terminal.log'
NEWMAN_OUTPUT = repository_dir + '/logs/newman.log'
NEWMAN_REPORTER_OUTPUT = repository_dir + '/logs/newman_report.json'
CURL_HTML = repository_dir + '/logs/curl_output.html'
NEWMAN_BASH = repository_dir + '/run_newman.sh'
CURL_RUN = 'curl '
NEWMAN_RUN = 'newman run ' + COLLECTION + ' -r cli,json --reporter-json-export ' + NEWMAN_REPORTER_OUTPUT + ' | tee ' + NEWMAN_OUTPUT
SEND_MAIL_REPORT = ['mail -s  "Report Postman" antons@coins.exchange < ']
NEWMAN_RUN2 = 'newman run ' + COLLECTION + ' -r cli,json --reporter-json-export ' + NEWMAN_REPORTER_OUTPUT


class Terminal:
    @classmethod
    def set_up_class(cls):
        if Instruments.detect_os() == OperationSystem.WINDOWS.value:
            print("It's Windows OS.   ")
        else:
            print("It's kind of Unix OS.   ")

    @classmethod
    def get_cur_date(cls):
        process = subprocess.check_output("date")
        print('Current date is:', process.decode("utf-8"))

    @classmethod
    def ping_host(cls, host):
        process = subprocess.run(['ping', host], stdout=subprocess.PIPE)
        return process.stdout

    @classmethod
    def run_cd(cls, dir_name):
        _os.chdir(dir_name)

    @classmethod
    def run_newman(self, command):
        proc = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
        process = str(proc.stdout)
        return process

    @classmethod
    def run_command_out(cls, command, file, *option, **option2):
        command = list(command)
        if option:
            command.append(option)
        if option2:
            command.append(option2)
        try:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate(
                timeout=100)[0]
            process = proc.decode("utf-8")
            Utils.save_stream_into_file(process, file)
            return process
        except subprocess.TimeoutExpired:
            raise TimeoutError

    @classmethod
    def run_command_in(cls, command, *option):
        if option:
            list(command)
            command.append(option)
        else:
            list(command)
        try:
            proc = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True).communicate(timeout=100)[0]
            return proc
        except subprocess.TimeoutExpired:
            raise TimeoutError
