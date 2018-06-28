#!/usr/bin/python
# -*- coding: utf8 -*-

import os
from src.test_utils.file_utils import config_parse


class BaseConfig(object):
    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'base_config.cfg')
    path_dir = os.path.abspath(os.path.dirname(__file__))
    parser = config_parse(config_file)

    ME_BASE_URL = parser.get('BASE_URL', 'base_url_me')
    CRM_BASE_URL = parser.get('BASE_URL', 'base_url_crm')
    BO_BASE_URL = parser.get('BASE_URL', 'base_url_bo')
    CRM_BASE_URL2 = parser.get('BASE_URL', 'base_url_crm2')
    BO_BASE_URL2 = parser.get('BASE_URL', 'base_url_bo2')
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

    W_CHROME_PATH = path_dir + parser.get('WEB_DRIVER_WIN', 'w_chrome')
    W_FIREFOX_PATH = path_dir + parser.get('WEB_DRIVER_WIN', 'w_firefox')
    W_IE_PATH = path_dir + parser.get('WEB_DRIVER_WIN', 'w_ie')
    W_EDGE_PATH = path_dir + parser.get('WEB_DRIVER_WIN', 'w_edge')
    W_JS_PATH = path_dir + parser.get('WEB_DRIVER_WIN', 'w_js')

    L_CHROME_PATH = path_dir + parser.get('WEB_DRIVER_LIN', 'l_chrome')
    L_FIREFOX_PATH = path_dir + parser.get('WEB_DRIVER_LIN', 'l_firefox')

    WTP_TESTS_RESULT = path_dir + parser.get('TEST_DATA', 'wtp_tests_result')
    CRM_TESTS_RESULT = path_dir + parser.get('TEST_DATA', 'crm_tests_result')
    WTP_LOGIN_DATA = path_dir + parser.get('TEST_DATA', 'me_login_data_csv')
    CRM_LOGIN_DATA = path_dir + parser.get('TEST_DATA', 'crm_login_data_csv')
    FORGOT_PASSWORD_DATA = path_dir + parser.get('TEST_DATA', 'forgot_data_csv')
    CRM_CREATE_USER = path_dir + parser.get('TEST_DATA', 'crm_create_user_csv')
    ME_LOGIN_DATA = path_dir + parser.get('TEST_DATA', 'me_login_data_csv')
    OPEN_ACCOUNT_DATA = path_dir + parser.get('TEST_DATA', 'open_account_data_csv')

    DB_HOST = parser.get('DATA_BASE', 'host')
    DB_PORT = parser.get('DATA_BASE', 'port')
    DB_USERNAME = parser.get('DATA_BASE', 'username')
    DB_PASSWORD = parser.get('DATA_BASE', 'password')
    DB_NAME = parser.get('DATA_BASE', 'db_name')
    DB_TABLE = parser.get('DATA_BASE', 'db_table')

    TESTRAIL_USER = parser.get('TESTRAIL', 'user')
    TESTRAIL_PASSWORD = parser.get('TESTRAIL', 'password')
    TESTRAIL_URL = parser.get('TESTRAIL', 'server_url')
    TESTRAIL_RUN = parser.get('TESTRAIL', 'test_run')

    CRM_CUSTOMER_ID = parser.get('USERS', 'crm_customer_id')
    CRM_CUSTOMER_EMAIL = parser.get('USERS', 'crm_customer_email')
    WTP_USER_EMAIL = parser.get('USERS', 'wtp_user_email')

    BIN_CARD_NUMBER = parser.get('CREDIT_CARD', 'bin_number')
    CC_CARD_NUMBER = parser.get('CREDIT_CARD', 'cc_number')
