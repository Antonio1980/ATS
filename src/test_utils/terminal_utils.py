import os
from src.repository import repository_dir
from tests.test_definitions import BaseConfig

test_utils_dir = os.path.abspath(os.path.dirname(__file__))
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