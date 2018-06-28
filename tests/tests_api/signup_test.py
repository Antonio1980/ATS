# !/usr/bin/env python
# -*- coding: utf8 -*-

import unittest
import http.client
from proboscis import test
from tests.test_definitions import BaseConfig


@test(groups=['api', ])
class SignUpTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.conn = http.client.HTTPConnection("acl,dx,exchange")
        cls.test_case = ''
        cls.test_run = BaseConfig.TESTRAIL_RUN
        cls.headers = {'Content-Type': "application/json"}
        cls.payload = "{\r\n\t\"jsonrpc\": \"2.0\",\r\n\t\"method\": \"Authorization.SignUp\",\r\n\t\"params\": " \
                      "[{\r\n\t\t\"FirstName\": \"QA_test\",\r\n\t\t\"LastName\": \"Test_qa\",\r\n\t\t\"" \
                      "Email\": \"antishipul@mailinator.com\",\r\n\t\t\"Password\": \"1Aa@<>12\",\r\n\t\t\"" \
                      "receivePromoEmail\": false,\r\n\t\t\"AcceptTerms\": true,\r\n\t\t\"Captcha\": \"test_test\"," \
                      "\r\n\t\t\"siteLanguage\": \"en\",\r\n\t\t\"EmailValidationUrl\": \"https://plat.dx.exchange/appProxy/openAccountDx.html\"," \
                      "\r\n\t\t\"receivePromoSMS\": false,\r\n\t\t\"receivePromoPushToMobile\": false,\r\n\t\t\"" \
                      "receiveTradingEmail\": false \r\n\t}],\r\n\t\"id\": \"1\"\r\n}\r\n"

    @classmethod
    @test(groups=['smoke', 'auth_service', 'positive', ])
    def test_signup(cls):
        cls.conn.request("POST", "https://acl.dx.exchange", cls.payload, cls.headers)
        res = cls.conn.getresponse()
        data = res.read()
        print(data.decode("utf-8"))

    @classmethod
    def tearDownClass(cls):
        pass
