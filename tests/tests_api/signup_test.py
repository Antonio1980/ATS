import unittest
import requests
from proboscis import test
from test_definitions import BaseConfig


@test(groups=['api', ])
class SignUpTest2(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.url = BaseConfig.API_BASE_URL
        cls.test_case = ''
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.headers = {'Content-Type': "application/json"}
        cls.payload = "{\n\t\"jsonrpc\": \"2.0\",\n\t\"method\": \"Authorization.SignUp\"," \
                      "\n\t\"params\": [{\n\t\t\"FirstName\": \"QA_test\",\n\t\t\"LastName\": \"Test_qa\"," \
                      "\n\t\t\"Email\": \"antishipul@mailinator.com\",\n\t\t\"Password\": \"1Aa@<>12\"," \
                      "\n\t\t\"receivePromoEmail\": false,\n\t\t\"AcceptTerms\": true," \
                      "\n\t\t\"Captcha\": \"test_test\",\n\t\t\"siteLanguage\": \"en\"," \
                      "\n\t\t\"EmailValidationUrl\": \"https://plat.dx.exchange/appProxy/openAccountDx.html\"," \
                      "\n\t\t\"receivePromoSMS\": false,\n\t\t\"receivePromoPushToMobile\": false," \
                      "\n\t\t\"receiveTradingEmail\": false \n\t}],\n\t\"id\": \"1\"\n}"

    @test(groups=['smoke', 'auth_service', 'positive', ])
    def test_signup2(self):
        response = requests.request("POST", self.url, data=self.payload, headers=self.headers)
        print(response.text)

    @classmethod
    def tearDownClass(cls):
        pass
