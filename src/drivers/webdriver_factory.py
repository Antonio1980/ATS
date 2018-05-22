# !/usr/bin/env python
# -*- coding: utf8 -*-

import selenium.webdriver as webdriver
from src.test_definitions import BaseConfig
from src.test_utils.os_utils import detect_os
from src.base.enums import OperationSystem, Browsers


class WebDriverFactory:
    @classmethod
    def get_browser(self, browser_name):
        if detect_os() == OperationSystem.WINDOWS:
            return self.get_browser_win(browser_name)
        else:
            return self.get_browser_lin(browser_name)
        raise Exception("No such " + browser_name + " browser exists")


    @classmethod
    def get_browser_win(self, browser_name):
        if (browser_name == Browsers.FIREFOX):
            return webdriver.Firefox(BaseConfig.W_FIREFOX_PATH)
        elif (browser_name == Browsers.CHROME):
            return webdriver.Chrome(BaseConfig.W_CHROME_PATH)
        elif (browser_name == Browsers.IE):
            return webdriver.Ie(BaseConfig.W_IE_PATH)
        elif (browser_name == Browsers.IE_EDGE):
            return webdriver.Edge(BaseConfig.W_EDGE_PATH)
        raise Exception("No such " + browser_name + " browser exists")


    @classmethod
    def get_browser_lin(self, browser_name):
        if (browser_name == 'firefox'):
            return webdriver.Firefox(BaseConfig.L_FIREFOX_PATH)
        elif (browser_name == 'chrome'):
            return webdriver.Chrome(BaseConfig.L_CHROME_PATH)
        raise Exception("No such " + browser_name + " browser exists")
