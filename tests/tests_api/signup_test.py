import unittest
import requests
from proboscis import test
from test_definitions import BaseConfig
from tests.tests_web_platform.pages.signup_page import SignUpPage


@test(groups=['api', ])
class SignUpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = BaseConfig.API_STAGING_URL
        cls.signup_page = SignUpPage()
        cls.email = cls.signup_page.email
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.password = cls.signup_page.password
        cls.first_last_name = cls.signup_page.username
        cls.headers = {'Content-Type': "application/json"}
        cls.payload = "{\n\t\"jsonrpc\": \"2.0\",\n\t\"method\": \"Authorization.SignUp\"," \
                      "\n\t\"params\": [{\n\t\t\"FirstName\": \"%s\",\n\t\t\"LastName\": \"%s\"," \
                      "\n\t\t\"Email\": \"%s\",\n\t\t\"Password\": \"%s\"," \
                      "\n\t\t\"receivePromoEmail\": false,\n\t\t\"AcceptTerms\": true," \
                      "\n\t\t\"Captcha\": \"test_test\",\n\t\t\"siteLanguage\": \"en\"," \
                      "\n\t\t\"EmailValidationUrl\": \"https://plat.dx.exchange/appProxy/openAccountDx.html\"," \
                      "\n\t\t\"receivePromoSMS\": false,\n\t\t\"receivePromoPushToMobile\": false," \
                      "\n\t\t\"receiveTradingEmail\": false \n\t}],\n\t\"id\": \"1\"\n}" % (cls.first_last_name, cls.first_last_name, cls.email, cls.password)

    @test(groups=['smoke', 'auth_service', 'positive', ])
    def test_signup(self):
        response = requests.request("POST", self.url, data=self.payload, headers=self.headers)
        print(response.text)

    @classmethod
    def tearDownClass(cls):
        pass
