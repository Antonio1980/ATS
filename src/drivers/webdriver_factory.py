from selenium import webdriver
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.enums import OperationSystem, Browsers


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
        elif browser_name == Browsers.IE_EDGE.value:
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
