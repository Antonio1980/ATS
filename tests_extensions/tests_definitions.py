#!/usr/bin/python
# -*- coding: utf8 -*-
import configparser
import os

from tests_extensions.get_tests_context import config_parse

class BaseConfig:
    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'base_config.cfg')
    dir_data = os.path.abspath(os.path.dirname(__file__))
    parser = config_parse(config_file)

    BASE_URL = parser.get('BASE_URL', 'base_url')
    W_CHROME_PATH: str = dir_data + parser.get('WEB_DRIVER_WIN', 'w_chrome')
    W_TEST_DATA = dir_data + parser.get('TEST_DATA_WIN', 'w_data_csv')
    W_FIREFOX_PATH = dir_data + parser.get('WEB_DRIVER_WIN', 'w_firefox')
    W_IE_PATH = dir_data + parser.get('WEB_DRIVER_WIN', 'w_ie')
    W_JS_PATH = dir_data + parser.get('WEB_DRIVER_WIN', 'w_js')

    L_CHROME_PATH: str = dir_data + parser.get('WEB_DRIVER_LIN', 'l_chrome')
    L_TEST_DATA = parser.get('TEST_DATA_LIN', 'l_data_csv')
    L_FIREFOX_PATH = dir_data + parser.get('WEB_DRIVER_LIN', 'l_firefox')
    L_CHROME_MAC_PATH = dir_data + parser.get('WEB_DRIVER_LIN', 'l_chrome_mac')

if __name__ == '__main__':
    config_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'base_config.cfg')
    dir_data = os.path.abspath(os.path.dirname(__file__))
    parser = config_parse(config_file)
    print(parser.get('WEB_DRIVER_LIN', 'l_chrome'))
    print(dir_data)



