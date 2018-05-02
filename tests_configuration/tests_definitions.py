#!/usr/bin/python
# -*- coding: utf8 -*-

from configparser import *
import os


class BaseConfig:
    config_file = os.path.join(os.path.dirname(__file__), 'base_config.ini')
    config = ConfigParser(allow_no_value=True, inline_comment_prefixes=(";"))
    config.optionxform = str
    config.sections()
    config.read(config_file)

    ROOT_PATH = os.path.dirname(os.path.abspath(__file__))
    # W_CHROME_PATH: str = ROOT_PATH + config['WEBDRIVER WIN']['w_chrome']
    W_CHROME_PATH: str = config['WEBDRIVER_WIN']['w_chrome']
    W_FIREFOX_PATH: str = config['WEBDRIVER_WIN']['w_firefox']
    W_IE_PATH: str = config['WEBDRIVER_WIN']['w_ie']
    W_JS_PATH: str = config['WEBDRIVER_WIN']['w_js']

    L_CHROME_PATH: str = ROOT_PATH + config['WEBDRIVER_LIN']['u_chrome']
    L_FIREFOX_PATH: str = ROOT_PATH + config['WEBDRIVER_LIN']['u_firefox']

    W_TEST_DATA: str = config['TEST_DATA_WIN']['w_data_csv']
    L_TEST_DATA: str = ROOT_PATH + config['TEST_DATA_LIN']['u_data_csv']

    BASE_URL: str = config['BASE']['base_url']
