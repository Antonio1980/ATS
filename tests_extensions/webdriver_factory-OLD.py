# !/usr/bin/env python
# -*- coding: utf8 -*-

import selenium.webdriver as webdriver
from selenium.webdriver import DesiredCapabilities

from tests_configuration.tests_definitions import BaseConfig


class WebdriverFactory:
    @staticmethod
    def get_browser(browser_name):
        if (browser_name == 'firefox'):
            return webdriver.Firefox(BaseConfig.W_FIREFOX_PATH)
        elif (browser_name == 'chrome'):
            return webdriver.Chrome(BaseConfig.W_CHROME_PATH)
        elif (browser_name == 'ie'):
            return webdriver.Ie(BaseConfig.W_IE_PATH)

        raise Exception("No such " + browser_name + " browser exists")


# Need to add ie and firefox driver.
class RemoteWebDriverFactory:
    @staticmethod
    def get_browser(browser_name):
        if (browser_name.lower() == 'firefox'):
            return webdriver.Firefox()
        elif (browser_name.lower() == 'chrome'):
            default_driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4444/wd/hub',
                desired_capabilities={'browserName': 'chrome',
                                      'version': '63.0'})
            return default_driver
        elif (browser_name.lower() == 'ie'):
            return webdriver.Ie()
        elif (browser_name.lower() == 'js'):
            js_driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.HTMLUNITWITHJS)
            return js_driver
        elif (browser_name.lower() == 'opera'):
            opera_driver = webdriver.Remote(
                command_executor='http://127.0.0.1:4444/wd/hub',
                desired_capabilities=DesiredCapabilities.OPERA)
            return opera_driver

        raise Exception("No such " + browser_name + " browser exists")









