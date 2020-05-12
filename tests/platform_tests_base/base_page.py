from config_definitions import BaseConfig
from src.base.browser import Browser
from src.base.log_decorator import automation_logger
from src.base import logger, test_token, base_url, api_base_url


class BasePage(Browser):

    def __init__(self):
        super(Browser, self).__init__()
        self.proxy = "/appProxy"
        self.base = base_url
        self.api_base_url = api_base_url
        self.wtp_base_url = self.base + self.proxy
        self.ui_delay = float(BaseConfig.UI_DELAY)
        self.script_test_token = "$.ajaxPrefilter(function (options) {if (!options.beforeSend) {options.beforeSend = " \
                                 "function (xhr) {xhr.setRequestHeader('Test-Token', '%s');}}})" % test_token

    @automation_logger(logger)
    def go_back_and_wait(self, driver, previous_url):
        try:
            self.go_back(driver)
            return self.wait_url_contains(driver, previous_url, self.ui_delay)
        except Exception as e:
            logger.logger.error("{0} go_back_and_wait failed with error: {1}".format(e.__class__.__name__,
                                                                                           e.__cause__), e)
            return False
