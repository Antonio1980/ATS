#!/usr/bin/python
# -*- coding: utf8 -*-

import os
import configparser
from src.drivers import drivers_dir
from src.repository import repository_dir


def get_parser(config_file):
    parser = configparser.ConfigParser()
    with open(config_file, mode='r', buffering=-1, closefd=True):
        parser.read(config_file)
        return parser


class BaseConfig(object):
    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'base_config.cfg')
    path_dir = os.path.abspath(os.path.dirname(__file__))
    parser = get_parser(config_file)

    ME_BASE_URL = parser.get('BASE_URL', 'base_url_me')
    CRM_BASE_URL = parser.get('BASE_URL', 'base_url_crm')
    BO_BASE_URL = parser.get('BASE_URL', 'base_url_bo')
    CRM_STAGING_URL = parser.get('BASE_URL', 'crm_staging_url')
    BO_STAGING_URL = parser.get('BASE_URL', 'bo_staging_url')
    CRM_INTEGRATION_URL = parser.get('BASE_URL', 'crm_integration_url')
    BO_INTEGRATION_URL = parser.get('BASE_URL', 'bo_integration_url')
    API_BASE_URL = parser.get('BASE_URL', 'api_base_url')
    API_INTEGRATION_URL = parser.get('BASE_URL', 'api_integration_url')
    API_STAGING_URL = parser.get('BASE_URL', 'api_staging_url')
    WTP_BASE_URL = parser.get('BASE_URL', 'wtp_base_url')
    WTP_INTEGRATION_URL = parser.get('BASE_URL', 'wtp_integration_url')
    WTP_STAGING_URL = parser.get('BASE_URL', 'wtp_staging_url')

    W_CHROME_PATH = drivers_dir + parser.get('WEB_DRIVER_WIN', 'w_chrome')
    W_FIREFOX_PATH = drivers_dir + parser.get('WEB_DRIVER_WIN', 'w_firefox')
    W_IE_PATH = drivers_dir + parser.get('WEB_DRIVER_WIN', 'w_ie')
    W_EDGE_PATH = drivers_dir + parser.get('WEB_DRIVER_WIN', 'w_edge')
    W_JS_PATH = drivers_dir + parser.get('WEB_DRIVER_WIN', 'w_js')

    L_CHROME_PATH = drivers_dir + parser.get('WEB_DRIVER_LIN', 'l_chrome')
    L_FIREFOX_PATH = drivers_dir + parser.get('WEB_DRIVER_LIN', 'l_firefox')

    WTP_TESTS_RESULT = repository_dir + parser.get('TEST_DATA', 'wtp_tests_result')
    CRM_TESTS_RESULT = repository_dir + parser.get('TEST_DATA', 'crm_tests_result')
    WTP_LOGIN_DATA = repository_dir + parser.get('TEST_DATA', 'me_login_data')
    CRM_LOGIN_DATA = repository_dir + parser.get('TEST_DATA', 'crm_login_data')
    FORGOT_PASSWORD_DATA = repository_dir + parser.get('TEST_DATA', 'forgot_data')
    CRM_CREATE_USER = repository_dir + parser.get('TEST_DATA', 'crm_create_user')
    ME_LOGIN_DATA = repository_dir + parser.get('TEST_DATA', 'me_login_data')
    OPEN_ACCOUNT_DATA = repository_dir + parser.get('TEST_DATA', 'open_account_data')
    WTP_TESTS_CUSTOMERS = repository_dir + parser.get('TEST_DATA', 'wtp_tests_customers')
    CRM_TESTS_USERS = repository_dir + parser.get('TEST_DATA', 'crm_tests_users')
    WTP_LOG_FILE = repository_dir + parser.get('TEST_DATA', 'wtp_log_file')

    DB_HOST = parser.get('DATA_BASE', 'host')
    DB_PORT = parser.get('DATA_BASE', 'port')
    DB_USERNAME = parser.get('DATA_BASE', 'username')
    DB_PASSWORD = parser.get('DATA_BASE', 'password')
    DB_NAME = parser.get('DATA_BASE', 'db_name')
    DB_TABLE = parser.get('DATA_BASE', 'db_table')

    DOCUMENT_JPG = repository_dir + parser.get('FILES', 'document_jpg')
    DOCUMENT_PNG = repository_dir + parser.get('FILES', 'document_png')

    TESTRAIL_USER = parser.get('TESTRAIL', 'user')
    TESTRAIL_PASSWORD = parser.get('TESTRAIL', 'password')
    TESTRAIL_URL = parser.get('TESTRAIL', 'server_url')
    TESTRAIL_RUN = parser.get('TESTRAIL', 'test_run')

    BIN_CARD_NUMBER = parser.get('CREDIT_CARD', 'bin_number')
    CC_CARD_NUMBER = parser.get('CREDIT_CARD', 'cc_number')


if __name__ == '__main__':
    print(BaseConfig().W_CHROME_PATH)
