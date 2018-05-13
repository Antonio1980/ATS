#!/usr/bin/python
# -*- coding: utf8 -*-

import os
from tests_sources.test_utils.file_util import config_parse


class BaseConfig:
    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'base_config.cfg')
    path_dir = os.path.abspath(os.path.dirname(__file__))
    parser = config_parse(config_file)

    CRM_BASE_URL = parser.get('BASE_URL', 'base_url_crm')
    BO_BASE_URL = parser.get('BASE_URL', 'base_url_bo')
    W_CHROME_PATH: str = path_dir + parser.get('WEB_DRIVER_WIN', 'w_chrome')
    W_TEST_DATA = path_dir + parser.get('TEST_DATA_WIN', 'w_data_csv')
    W_FIREFOX_PATH = path_dir + parser.get('WEB_DRIVER_WIN', 'w_firefox')
    W_IE_PATH = path_dir + parser.get('WEB_DRIVER_WIN', 'w_ie')
    W_JS_PATH = path_dir + parser.get('WEB_DRIVER_WIN', 'w_js')

    L_CHROME_PATH: str = path_dir + parser.get('WEB_DRIVER_LIN', 'l_chrome')
    L_TEST_DATA = parser.get('TEST_DATA_LIN', 'l_data_csv')
    L_FIREFOX_PATH = path_dir + parser.get('WEB_DRIVER_LIN', 'l_firefox')



