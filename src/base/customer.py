"""
Author: Anton Shipulin.
Created: 20.10.2018
Version: 2.0
"""

import re
from src.base.browser import Browser
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.postman_client import PostmanClient
from src.base.base_exception import AutomationError


class Customer(object):
    def __init__(self):
        super(Customer, self).__init__()
        self.zip = "45263"
        self.city = "Ashdod"
        self.test_case = "3750"
        self.password = "1Aa@<>12"
        self.birthday = "13/08/1980"
        self.test_token = BaseConfig.TEST_TOKEN
        self.username = Instruments.generate_username()
        self.email = self.username + "@mailinator.com"
        self.phone = Instruments.generate_phone_number()
        self.user_first_last_name = Instruments.generate_user_first_last_name()
        self.script_storage_clear = "localStorage.clear();"
        self.script_signin = '$(".formContainer.formBox input.captchaCode").val("test_QA_test");'
        self.script_signup = '$("#openAccountDxForm .captchaCode").val("test_QA_test");'
        self.script_forgot = '$("#dxPackageContainer_forgotPassword .captchaCode").val("test_QA_test");'
        self.script_customer_id = "return SO.model.Customer.getCustomerId();"
        self.script_is_signed = "return SO.model.Customer.isLoggedIn();"
        self.script_registration_step = "return SO.model.Customer.currentCustomer.registrationStep"
        self.script_input_val = '''return $("input[name='phonePrefix']").val();'''
        self.script_test_token = "$.ajaxPrefilter(function (options) {if (!options.beforeSend) {options.beforeSend = " \
                                 "function (xhr) {xhr.setRequestHeader('Test-Token', '%s');}}})" % self.test_token

    @classmethod
    def get_browser_functionality(cls):
        return Browser()

    @classmethod
    def get_guerrilla_details(cls):
        try:
            response = Instruments.get_guerrilla_email()
            guerrilla_email = response[1]['email_addr']
            sid_token = response[1]['sid_token']
            time_stamp = str(response[1]['email_timestamp'])
            guerrilla_username = guerrilla_email.split('@')[0]
            # 0- email, 1- username, 2- sid_token, 3- time_stamp
            return guerrilla_email, guerrilla_username, sid_token, time_stamp
        except AutomationError as e:
            print("{0} get_guerrilla_details failed with error: {1}".format(e.__class__.__name__, e.__cause__))

    @classmethod
    def get_api_access(cls, auth_token):
        return PostmanClient(auth_token)


class ForgottenCustomer(Customer):
    def __init__(self):
        super(ForgottenCustomer, self).__init__()
        pattern = r"([\w\.-]+)"
        # rows = Instruments.run_mysql_query(
        # "SELECT email FROM customers WHERE email LIKE '%@guerrillamailblock.com%' AND status=2;")
        # index_ = random.randrange(len(rows))
        # self.forgotten_email = rows[index_]
        # method signature: 1- File, 2- Row, 3- First column, 4- Second column etc.
        customer_details = Instruments.get_account_details(BaseConfig.WTP_TESTS_CUSTOMERS, 0, 0, 1, 2, 3, 4)
        self.forgotten_email = customer_details['email']
        self.forgotten_password = customer_details['password']
        self.forgotten_customer_id = customer_details['customer_username']
        self.forgotten_guerrilla_token = customer_details['guerrilla_token']
        self.forgotten_guerrilla_timestamp = customer_details['guerrilla_timestamp']
        username = re.findall(pattern, self.forgotten_email)
        self.forgotten_username = username[0]


class RegisteredCustomer(Customer):
    def __init__(self):
        super(RegisteredCustomer, self).__init__()
        pattern = r"([\w\.-]+)"
        customer_details = Instruments.get_account_details(BaseConfig.TOOL_OUTPUT_FILE, 0, 0, 1, 2, 3, 4)
        self.pended_email = customer_details['email']
        self.pended_password = customer_details['password']
        self.pended_customer_id = customer_details['customer_username']
        self.pended_guerrilla_token = customer_details['guerrilla_token']
        self.pended_guerrilla_timestamp = customer_details['guerrilla_timestamp']
        username = re.findall(pattern, self.pended_email)
        self.pended_username = username[0]


# if __name__ == '__main__':
#     customer = Customer()
#     pass
