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
    W_CRM_LOGIN_DATA = path_dir + parser.get('TEST_DATA_WIN', 'w_crm_login_data_csv')
    W_CRM_FORGOT_DATA = path_dir + parser.get('TEST_DATA_WIN', 'w_crm_forgot_data_csv')
    W_ME_LOGIN_DATA = path_dir + parser.get('TEST_DATA_WIN', 'w_me_login_data_csv')

    L_CHROME_PATH = path_dir + parser.get('WEB_DRIVER_LIN', 'l_chrome')
    L_FIREFOX_PATH = path_dir + parser.get('WEB_DRIVER_LIN', 'l_firefox')
    L_CRM_LOGIN_DATA = path_dir + parser.get('TEST_DATA_LIN', 'l_crm_login_data_csv')
    L_CRM_FORGOT_DATA = path_dir + parser.get('TEST_DATA_LIN', 'l_crm_forgot_data_csv')
    L_ME_LOGIN_DATA = path_dir + parser.get('TEST_DATA_LIN', 'l_me_login_data_csv')




