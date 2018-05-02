# !/usr/bin/env python
# -*- coding: utf8 -*-

import platform
import selenium.webdriver as webdriver
from tests_configuration.tests_definitions import BaseConfig


class WebDriverFactory:
    @classmethod
    def get_browser(self, browser_name):
        if self.detect_os() == "windows":
            print(self.detect_os())
            return self.get_browser_win(browser_name)
        else:
            return self.get_browser_lin(browser_name)
        raise Exception("No such " + browser_name + " browser exists")

    @classmethod
    def get_browser_win(self, browser_name):
        if (browser_name == 'firefox'):
            return webdriver.Firefox(BaseConfig.W_FIREFOX_PATH)
        elif (browser_name == 'chrome'):
            return webdriver.Chrome(BaseConfig.W_CHROME_PATH)
        elif (browser_name == 'ie'):
            return webdriver.Ie(BaseConfig.W_IE_PATH)
        raise Exception("No such " + browser_name + " browser exists")

    @classmethod
    def get_browser_lin(self, browser_name):
        if (browser_name == 'firefox'):
            return webdriver.Firefox(BaseConfig.L_FIREFOX_PATH)
        elif (browser_name == 'chrome'):
            return webdriver.Chrome(BaseConfig.L_CHROME_PATH)
        elif (browser_name == 'ie'):
            return webdriver.Ie(BaseConfig.L_IE_PATH)
        raise Exception("No such " + browser_name + " browser exists")

    @classmethod
    def detect_os(self):
        if (self.is_mac() == 1):
            return "macintosh"
        elif (self.is_win() == 1):
            return "windows"
        elif (self.is_lin() == 1):
            return "linux"
        else:
            raise Exception("The OS not detected")

    @classmethod
    def is_mac(self):
        #return platform.index(r"^mac*") >= 0
        if platform.system().lower() == "darwin":
            return 1
        else:
            print("platform.system().lower()")

    @classmethod
    def is_win(self):
        if platform.system().lower() == "windows":
            return 1
        else:
            print("platform.system().lower()")

    @classmethod
    def is_lin(self):
        if platform.system().lower() == "linux":
            return 1
        else:
            print("platform.system().lower()")

if __name__ == '__main__':
    pass