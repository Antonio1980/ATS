"""
Author: Anton Shipulin.
Created: 01.08.2018
Version: 1.05
"""

import time
import subprocess
import multiprocessing
from selenium import webdriver
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from selenium.webdriver import DesiredCapabilities
from src.base.enums import OperationSystem, Browsers
from selenium.common.exceptions import WebDriverException


class WebDriverFactory(object):
    @classmethod
    def get_driver(cls, browser_name=None):
        if browser_name is None:
            browser_name = Browsers.CHROME.value
        if Instruments.detect_os() == OperationSystem.WINDOWS.value:
            return cls.get_driver_win(browser_name)
        elif (Instruments.detect_os() == OperationSystem.DARWIN.value) or \
                (Instruments.detect_os() == OperationSystem.LINUX.value):
            return cls.get_driver_lin(browser_name)
        else:
            raise Exception("Operational System not detected.")

    @classmethod
    def get_driver_win(cls, browser_name):
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
    def get_driver_lin(cls, browser_name):
        if browser_name == Browsers.FIREFOX.value:
            return webdriver.Firefox(BaseConfig.L_FIREFOX_PATH)
        elif browser_name == Browsers.CHROME.value:
            return webdriver.Chrome(BaseConfig.L_CHROME_PATH)
        else:
            raise Exception("No such " + browser_name + " browser exists")

    @classmethod
    def get_browser_stack_driver(cls, remote_details, local=False):
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

    @classmethod
    def get_remote_driver(cls, browser_name):
        browser_name = browser_name.lower()
        _executor = "http://127.0.0.1:4444/wd/hub"
        if browser_name == Browsers.FIREFOX.value:
            return webdriver.Remote(command_executor=_executor, desired_capabilities=DesiredCapabilities.FIREFOX)
        elif browser_name == Browsers.CHROME.value:
            return webdriver.Remote(command_executor=_executor, desired_capabilities=DesiredCapabilities.CHROME)
        elif browser_name == Browsers.IE.value:
            return webdriver.Remote(command_executor=_executor,
                                    desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)
        elif browser_name == Browsers.EDGE.value:
            return webdriver.Remote(command_executor=_executor, desired_capabilities=DesiredCapabilities.EDGE)
        elif browser_name == Browsers.OPERA.value:
            return webdriver.Remote(command_executor=_executor, desired_capabilities=DesiredCapabilities.OPERA)
        elif browser_name == Browsers.HTMLUNITWITHJS.value:
            return webdriver.Remote(command_executor=_executor, desired_capabilities=DesiredCapabilities.HTMLUNITWITHJS)
        else:
            raise Exception("No such " + browser_name + " browser exists")

    @classmethod
    def start_selenium_server(cls, browser_name):
        p = multiprocessing.Process(target=cls.start_server(browser_name))
        return p.start()

    @classmethod
    def start_server(cls, browser_name):
        """
        Calls self method run_command_in for selenium-standalone-server.jar.
        """
        browser_name = browser_name.lower()
        if browser_name == Browsers.FIREFOX.value:
            option = "-Dwebdriver.chrome.driver=" + BaseConfig.W_FIREFOX_PATH
        elif browser_name == Browsers.CHROME.value:
            option = "-Dwebdriver.chrome.driver=" + BaseConfig.W_CHROME_PATH
        elif browser_name == Browsers.IE.value:
            option = "-Dwebdriver.chrome.driver=" + BaseConfig.W_IE_PATH
        elif browser_name == Browsers.EDGE.value:
            option = "-Dwebdriver.chrome.driver=" + BaseConfig.W_EDGE_PATH
        else:
            raise Exception("No such " + browser_name + " browser exists")

        command = ["java", option, "-jar", BaseConfig.SELENIUM_JAR]
        cls.run_terminal_command(command)

    @classmethod
    def run_terminal_command(cls, command):
        return subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)


# if __name__ == '__main__':
#     WebDriverFactory.start_selenium_server(Browsers.CHROME.value)
#     driver = WebDriverFactory.get_remote_driver(Browsers.CHROME.value)
#     pass
