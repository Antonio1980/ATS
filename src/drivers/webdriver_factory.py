"""
Author: Anton Shipulin.
Created: 01.08.2018
Version: 1.05
"""

import time
from selenium import webdriver
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.enums import OperationSystem, Browsers
from selenium.common.exceptions import WebDriverException


class WebDriverFactory:
    @classmethod
    def get_browser(cls, browser_name=None):
        if browser_name is None:
            browser_name = Browsers.CHROME.value
        if Instruments.detect_os() == OperationSystem.WINDOWS.value:
            return cls.get_browser_win(browser_name)
        elif (Instruments.detect_os() == OperationSystem.DARWIN.value) or \
                (Instruments.detect_os() == OperationSystem.LINUX.value):
            return cls.get_browser_lin(browser_name)
        else:
            raise Exception("Operational System not detected.")

    @classmethod
    def get_browser_win(cls, browser_name):
        browser_name = browser_name.lower()
        if browser_name == Browsers.FIREFOX.value:
            return webdriver.Firefox(executable_path=BaseConfig.W_FIREFOX_PATH)
        elif browser_name == Browsers.CHROME.value:
            return webdriver.Chrome(BaseConfig.W_CHROME_PATH)
        elif browser_name == Browsers.IE.value:
            return webdriver.Ie(BaseConfig.W_IE_PATH)
        elif browser_name == Browsers.EDGE.value:
            return webdriver.Edge(BaseConfig.W_EDGE_PATH)
        else:
            raise Exception("No such " + browser_name + " browser exists")

    @classmethod
    def get_browser_lin(cls, browser_name):
        if browser_name == Browsers.FIREFOX.value:
            return webdriver.Firefox(BaseConfig.L_FIREFOX_PATH)
        elif browser_name == Browsers.CHROME.value:
            return webdriver.Chrome(BaseConfig.L_CHROME_PATH)
        else:
            raise Exception("No such " + browser_name + " browser exists")

    @classmethod
    def get_remote_driver(cls, remote_details, local=False):
        browser_name, browser_version, os_name, os_version, resolution = remote_details
        _executor = BaseConfig.BROWSER_STACK
        desired_cap = {
            'browser': browser_name, 'browser_version': browser_version, 'os': os_name, 'os_version': os_version, 'resolution': resolution
        }
        count = 0
        while True:
            try:
                desired_cap['browserstack.local'] = local
                desired_cap['browserstack.selenium_version'] = '3.5.2'
                driver = webdriver.Remote(command_executor=_executor, desired_capabilities=desired_cap)
                return driver
            except WebDriverException as e:
                s = "%s" % e
                print("Got exception %s" % s)
                print("%s" % dir(s))
                if "Empty pool of VM for setup Capabilities" not in s:
                    raise
                time.sleep(5)
            if count == 60:
                raise Exception("Time out trying to get a browser")
            count += 1

# if __name__ == '__main__':
#     driver = WebDriverFactory.get_remote_driver('chrome', '68', 'windows', '10')
#     driver.get('http:www.google.com')
