#!/usr/bin/python
# -*- coding: utf8 -*-

import os
from src.test_utils.file_utils import config_parse


class BaseConfig:
    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'base_config.cfg')
    path_dir = os.path.abspath(os.path.dirname(__file__))
    parser = config_parse(config_file)

    CRM_BASE_URL = parser.get('BASE_URL', 'base_url_crm')
    BO_BASE_URL = parser.get('BASE_URL', 'base_url_bo')
    ME_BASE_URL = parser.get('BASE_URL', 'base_url_me')

    W_CHROME_PATH = path_dir + parser.get('WEB_DRIVER_WIN', 'w_chrome')
    W_FIREFOX_PATH = path_dir + parser.get('WEB_DRIVER_WIN', 'w_firefox')
    W_IE_PATH = path_dir + parser.get('WEB_DRIVER_WIN', 'w_ie')
    W_EDGE_PATH = path_dir + parser.get('WEB_DRIVER_WIN', 'w_edge')
    W_JS_PATH = path_dir + parser.get('WEB_DRIVER_WIN', 'w_js')

    L_CHROME_PATH = path_dir + parser.get('WEB_DRIVER_LIN', 'l_chrome')
    L_FIREFOX_PATH = path_dir + parser.get('WEB_DRIVER_LIN', 'l_firefox')

    CRM_LOGIN_DATA = path_dir + parser.get('TEST_DATA', 'crm_login_data_csv')
    CRM_FORGOT_DATA = path_dir + parser.get('TEST_DATA', 'crm_forgot_data_csv')
    ME_LOGIN_DATA = path_dir + parser.get('TEST_DATA', 'me_login_data_csv')

    DB_HOST = parser.get('DATA_BASE', 'host')
    DB_USERNAME = parser.get('DATA_BASE', 'username')
    DB_PASSWORD = parser.get('DATA_BASE', 'password')
    DB_NAME = parser.get('DATA_BASE', 'db_name')
    DB_TABLE = parser.get('DATA_BASE', 'db_table')

    TESTRAIL_USER = parser.get('TESTRAIL', 'user')
    TESTRAIL_TOKEN = parser.get('TESTRAIL', 'token')
    TESTRAIL_URL = parser.get('TESTRAIL', 'server_url')
    TESTRAIL_RUN = parser.get('TESTRAIL', 'test_run')






