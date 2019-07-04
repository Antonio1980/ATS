import time
import pychrome
import subprocess
import multiprocessing
from src.base import logger
from selenium import webdriver
from config_definitions import BaseConfig
from src.base.instruments import Instruments
from selenium.webdriver import DesiredCapabilities
from src.base.log_decorator import automation_logger
from src.base.enums import OperationSystem, Browsers
from src.base.automation_error import AutomationError
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.firefox import GeckoDriverManager
from selenium.common.exceptions import WebDriverException
from testcontainers.selenium import BrowserWebDriverContainer


class WebDriverFactory:
    remote_executor = BaseConfig.R_DRIVER_URL
    f_12_executor = BaseConfig.F_12_DRIVER_URL

    chrome_options = webdriver.ChromeOptions()
    chrome_options.add_argument('--headless')
    chrome_options.add_argument('--no-sandbox')
    chrome_options.add_argument('--disable-gpu')
    # chrome_options.add_argument('--enable-benchmarking')
    # chrome_options.add_argument('--enable-net-benchmarking')
    # chrome_options.add_argument('--remote-debugging-port=9222')
    chrome_options.add_experimental_option('w3c', False)

    @classmethod
    @automation_logger(logger)
    def get_google_dev_tools(cls):
        """
        Use with Remote Driver instance.
        @return: browser f12 functionality.
        """

        def request_will_be_sent(**kwargs):
            print("loading: %s" % kwargs.get('request').get('url'))

        browser = pychrome.Browser(url=cls.f_12_executor)
        f_12 = browser.new_tab()
        f_12.Network.requestWillBeSent = request_will_be_sent
        f_12.start()
        f_12.Network.enable()
        return f_12

    @classmethod
    @automation_logger(logger)
    def get_driver(cls, browser_name=None):
        """
        Define Operational System and return driver accordingly.
        :param browser_name: Chrome, Firefox, Edge or IE
        :return: web driver.
        """
        if browser_name is None:
            browser_name = Browsers.CHROME.value
        if Instruments.detect_os() == OperationSystem.WINDOWS.value:
            return cls.get_driver_win(browser_name)
        elif Instruments.detect_os() == OperationSystem.DARWIN.value:
            return cls.get_driver_mac(browser_name)
        elif Instruments.detect_os() == OperationSystem.LINUX.value:
            return cls.get_driver_lin(browser_name)
        else:
            error = "Operational System not detected."
            logger.logger.exception(error)
            raise AutomationError(error)

    @classmethod
    @automation_logger(logger)
    def get_driver_win(cls, browser_name):
        """
        Choose needed driver according to Windows OS.
        :param browser_name: Chrome, Firefox, Edge or IE
        :return: web driver.
        """
        browser_name = browser_name.lower()
        if browser_name == Browsers.FIREFOX.value:
            try:
                return webdriver.Firefox(executable_path=GeckoDriverManager().install())
            except Exception as e:
                logger.logger.exception(e)
                return webdriver.Firefox(executable_path=BaseConfig.W_FIREFOX_PATH)
        elif browser_name == Browsers.CHROME.value:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option('w3c', False)
            try:
                return webdriver.Chrome(ChromeDriverManager().install(), options=chrome_options)
            except Exception as e:
                logger.logger.exception(e)
                return webdriver.Chrome(BaseConfig.W_CHROME_PATH, options=chrome_options)
        elif browser_name == Browsers.IE.value:
            return webdriver.Ie(BaseConfig.W_IE_PATH)
        elif browser_name == Browsers.EDGE.value:
            return webdriver.Edge(BaseConfig.W_EDGE_PATH)
        else:
            error = "No such " + browser_name + " browser exists"
            logger.logger.exception(error)
            raise AutomationError(error)

    @classmethod
    @automation_logger(logger)
    def get_driver_lin(cls, browser_name):
        """
        Choose needed driver according to Linux OS.
        :param browser_name: Chrome, Firefox
        :return: web driver.
        """
        if browser_name == Browsers.FIREFOX.value:
            try:
                return webdriver.Firefox(executable_path=GeckoDriverManager().install())
            except Exception as e:
                logger.logger.exception(e)
                return webdriver.Firefox(executable_path=BaseConfig.L_FIREFOX_PATH)
        elif browser_name == Browsers.CHROME.value:
            try:
                return webdriver.Chrome(ChromeDriverManager().install(), options=cls.chrome_options)
            except Exception as e:
                logger.logger.exception(e)
                return webdriver.Chrome(BaseConfig.L_CHROME_PATH, options=cls.chrome_options)
        else:
            error = "No such " + browser_name + " browser exists"
            logger.logger.exception(error)
            raise AutomationError(error)

    @classmethod
    @automation_logger(logger)
    def get_driver_mac(cls, browser_name):
        """
        Choose needed driver according to Darwin OS.
        :param browser_name: Chrome, Firefox
        :return: web driver for mac.
        """
        if browser_name == Browsers.FIREFOX.value:
            try:
                return webdriver.Firefox(executable_path=GeckoDriverManager().install())
            except Exception as e:
                logger.logger.exception(e)
                return webdriver.Firefox(executable_path=BaseConfig.M_FIREFOX_PATH)
        elif browser_name == Browsers.CHROME.value:
            chrome_options = webdriver.ChromeOptions()
            chrome_options.add_experimental_option('w3c', False)
            try:
                return webdriver.Chrome(ChromeDriverManager().install(), chrome_options=chrome_options)
            except Exception as e:
                logger.logger.exception(e)
                return webdriver.Chrome(BaseConfig.M_CHROME_PATH, chrome_options=chrome_options)
        else:
            error = "No such " + browser_name + " browser exists"
            logger.logger.exception(error)
            raise AutomationError(error)

    @classmethod
    @automation_logger(logger)
    def get_webdriver_container(cls, browser_name):
        """
        Provides driver as Docker container..
        :param browser_name: Chrome, Firefox
        :return: web driver.
        """
        if browser_name == Browsers.FIREFOX.value:
            return BrowserWebDriverContainer(DesiredCapabilities.FIREFOX)
        elif browser_name == Browsers.CHROME.value:
            return BrowserWebDriverContainer(DesiredCapabilities.CHROME)
        else:
            error = "No such " + browser_name + " container exists"
            logger.logger.exception(error)
            raise AutomationError(error)

    @classmethod
    @automation_logger(logger)
    def get_browser_stack_driver(cls, remote_details, local=False):
        """
        Remote connection to Browesrstack server.
        :param remote_details: {'browser': 'Chrome', 'browser_version': '68.0', 'os': 'OS X', 'os_version': 'Sierra',
                               'resolution': '1920x1080'}
        :param local: default - False
        :return: remote web driver
        """
        _executor = BaseConfig.BROWSER_STACK
        remote_details['browserstack.local'] = local
        remote_details['browserstack.selenium_version'] = '3.5.2'
        count = 0
        while True:
            try:
                return webdriver.Remote(command_executor=_executor, desired_capabilities=remote_details)
            except WebDriverException as e:
                s = "%s" % e
                logger.logger.error("Got exception %s" % s)
                logger.logger.error("%s" % dir(s))
                if "Empty pool of VM for setup Capabilities" not in s:
                    raise
                time.sleep(5)
            if count == 60:
                error = "Time out trying to get a browser"
                logger.logger.exception(error)
                raise AutomationError(error)
            count += 1

    @classmethod
    @automation_logger(logger)
    def get_remote_driver(cls, browser_name):
        """

        :param browser_name: ('Chrome', '68.0', 'OS X', 'Sierra', '1920x1080')
        :return:
        """
        if isinstance(browser_name, tuple):
            browser_name = browser_name[0].lower()
        else:
            browser_name = browser_name.lower()
        if browser_name == Browsers.FIREFOX.value:
            return webdriver.Remote(command_executor=cls.remote_executor,
                                    desired_capabilities=DesiredCapabilities.FIREFOX)
        elif browser_name == Browsers.CHROME.value:
            return webdriver.Remote(command_executor=cls.remote_executor,
                                    desired_capabilities=DesiredCapabilities.CHROME)
        elif browser_name == Browsers.IE.value:
            return webdriver.Remote(command_executor=cls.remote_executor,
                                    desired_capabilities=DesiredCapabilities.INTERNETEXPLORER)
        elif browser_name == Browsers.EDGE.value:
            return webdriver.Remote(command_executor=cls.remote_executor,
                                    desired_capabilities=DesiredCapabilities.EDGE)
        elif browser_name == Browsers.OPERA.value:
            return webdriver.Remote(command_executor=cls.remote_executor,
                                    desired_capabilities=DesiredCapabilities.OPERA)
        elif browser_name == Browsers.HTML_UNIT_WITH_JS.value:
            return webdriver.Remote(command_executor=cls.remote_executor,
                                    desired_capabilities=DesiredCapabilities.HTMLUNITWITHJS)
        else:
            error = "No such " + browser_name + " browser exists"
            logger.logger.exception(error)
            raise AutomationError(error)

    @classmethod
    @automation_logger(logger)
    def start_selenium_server(cls, browser_name):
        multiprocessing.Process(target=cls.start_server(browser_name)).start()

    @classmethod
    @automation_logger(logger)
    def start_server(cls, browser_name):
        """
        Calls self method run_command_in to start selenium-standalone-server.jar.
        """
        browser_name = browser_name.lower()
        if browser_name == Browsers.FIREFOX.value:
            option = "-Dwebdriver.firefox.driver=" + BaseConfig.W_FIREFOX_PATH
        elif browser_name == Browsers.CHROME.value:
            option = "-Dwebdriver.chrome.driver=" + BaseConfig.W_CHROME_PATH
        elif browser_name == Browsers.IE.value:
            option = "-Dwebdriver.ie.driver=" + BaseConfig.W_IE_PATH
        elif browser_name == Browsers.EDGE.value:
            option = "-Dwebdriver.edge.driver=" + BaseConfig.W_EDGE_PATH
        else:
            error = "No such " + browser_name + " browser exists"
            logger.logger.exception(error)
            raise AutomationError(error)

        command = ["java", option, "-jar", BaseConfig.SELENIUM_JAR]
        cls.run_terminal_command(command)

    @staticmethod
    @automation_logger(logger)
    def run_terminal_command(command):
        """

        :param command:
        """
        subprocess.Popen(
            command, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, shell=True)
