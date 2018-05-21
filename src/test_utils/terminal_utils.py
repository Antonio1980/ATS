# !/usr/bin/env python
# -*- coding: utf8 -*-

import os
from src.test_data.data_helper import test_data_dir


test_utils_dir = os.path.abspath(os.path.dirname(__file__))
UTILS_HOME_DIR = test_utils_dir
DATA_HOME_DIR = test_data_dir
HOST = 'www.google.com'

LS = ['ls', '-ltr']
CHMOD = ['chmod', '+x']
PWD = ['pwd']


COLLECTION = test_data_dir + '/services_collection.json'
ENVIRONMENT = test_data_dir + '/services_environment.json'
TERMINAL_OUTPUT = test_data_dir + '/logs/terminal.log'
NEWMAN_OUTPUT = test_data_dir + '/logs/newman.log'
NEWMAN_REPORTER_OUTPUT = test_data_dir + '/logs/newman_report.json'
NEWMAN_BASH = test_data_dir + '/run_newman.sh'

NEWMAN_RUN = 'newman run ' + COLLECTION + ' -r cli,json --reporter-json-export ' + NEWMAN_REPORTER_OUTPUT + ' | tee ' + NEWMAN_OUTPUT
SEND_MAIL_REPORT = ['mail -s  "Report Postman" antons@coins.exchange < ']
NEWMAN_RUN2 = 'newman run ' + COLLECTION + ' -r cli,json --reporter-json-export ' + NEWMAN_REPORTER_OUTPUT



