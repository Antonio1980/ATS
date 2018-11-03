from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.base_exception import AutomationError
from tests.tests_web_platform.locators import base_page_locators


class BasePage(Browser):
    def __init__(self):
        super(Browser, self).__init__()
        self.proxy = "appProxy"
        self.base = BaseConfig.WTP_STAGING_URL
        self.test_token = BaseConfig.TEST_TOKEN
        self.wtp_base_url = self.base + self.proxy
        self.api_base_url = BaseConfig.API_STAGING_URL
        self.base_locators = base_page_locators
        self.script_document_1 = "$('.doc_1_1_0Hidden.hidden').show();"
        self.script_document_2 = "$('.doc_1_2_0Hidden.hidden').show();"
        self.script_document_3 = "$('.doc_2_1_0Hidden.hidden').show();"
        self.script_input_val = '''return $("input[name='phonePrefix']").val();'''
        self.script_signup = '$("#openAccountDxForm .captchaCode").val("test_QA_test");'
        self.script_signin = '$(".formContainer.formBox input.captchaCode").val("test_QA_test");'
        self.script_forgot = '$("#dxPackageContainer_forgotPassword .captchaCode").val("test_QA_test");'
        self.script_test_token = "$.ajaxPrefilter(function (options) {if (!options.beforeSend) {options.beforeSend = function (xhr) {xhr.setRequestHeader('Test-Token', '%s');}}})" % self.test_token

    def go_back_and_wait(self, driver, previous_url):
        delay = 5
        try:
            self.go_back(driver)
            return self.wait_url_contains(driver, previous_url, delay)
        except AutomationError as e:
            print("{0} go_back_and_wait failed with error: {1}".format(e.__class__.__name__, e.__cause__))
            return False
