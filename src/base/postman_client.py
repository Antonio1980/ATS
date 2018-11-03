"""
Author: Anton Shipulin.
Created: 25.10.2018
Version: 2.0
"""

import json
import requests
from test_definitions import BaseConfig
from src.base.instruments import Instruments
from src.base.base_exception import AutomationError

balance_url = BaseConfig.BALANCE_SERVICE
balance_headers = {'Content-Type': 'application/json'}


class PostmanClient(object):
    def __init__(self, auth_token):
        self.test_token = BaseConfig.TEST_TOKEN
        self.postman_url = BaseConfig.API_STAGING_URL
        self.headers = {'Content-Type': "application/json", 'Authorization': auth_token, 'Test-Token': self.test_token,
                        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36'}

    # PaymentService methods
    def add_credit_card(self, email, phone):
        payload = "{\r\n \"jsonrpc\": \"2.0\",\r\n \"method\": \"Payment.AddCard\",\r\n \"params\": [{\r\n \"phone\": "\
                  "\"" + phone + "\",\r\n\"customerEmail\":\"" + email + "\",\r\n \"cardNumber\":\"4111111111111111\","\
                  "\r\n\"cvv\":\"111\",\r\n\"expYear\":2020,\r\n \"expMonth\":12,\r\n\"holderName\":\"QaTest TestQa\","\
                  "\r\n\"address\": \"Street 12/2\",\r\n \"postalCode\": \"123456\",\r\n \"city\": \"Ashdod\",\r\n " \
                  "\"country\": \"US\",\r\n \"state\": \"FL\",\r\n\"currency\":\"USD\",\r\n \"phonePrefix\":\"+972\"," \
                  "\r\n \"passportNumber\": \"A5584534\",\r\n \"personalId\": \"669998558\"\r\n }]\r\n}"
        try:
            _response = requests.request("POST", self.postman_url, data=payload, headers=self.headers)
            return json.loads(_response.text)
        except AutomationError as e:
            print("{0} add_credit_card failed with error: {1}".format(e.__class__.__name__, e.__cause__))

    def add_deposit_credit_card(self, card_id, deposit_amount, currency_id):
        payload = "{\r\n \"jsonrpc\": \"2.0\",\r\n \"method\": \"Payment.DepositCreditCard\",\r\n \"params\": " \
                  "[{\r\n \"cardId\": " + card_id + ",\r\n \"amount\": " + deposit_amount + ",\r\n \"cvv\": " \
                  "\"111\",\r\n \"currencyId\": " + currency_id + ",\r\n \"acceptTerms\" : true\r\n }]\r\n}"
        try:
            _response = requests.request("POST", self.postman_url, data=payload, headers=self.headers)
            return json.loads(_response.text)
        except AutomationError as e:
            print("{0} add_deposit_credit_card failed with error: {1}".format(e.__class__.__name__, e.__cause__))

    # OrderService methods
    def create_order(self, direction, quantity, instrument_id, price=None):
        quantity_calc = Instruments.calculate_decimals(quantity)
        q_value = str(quantity_calc[0])
        q_precisions = str(quantity_calc[1])
        if price:
            price_calc = Instruments.calculate_decimals(price)
            p_value = str(price_calc[0])
            p_precisions = str(price_calc[1])
            payload = "{\r\n \"jsonrpc\": \"2.0\",\r\n \"method\": \"OrderManagement.Create\",\r\n\"params\": " \
                      "[\r\n {\r\n \"order\": {\r\n \"direction\": " + direction + ",\r\n \"quantity\": {\r\n " \
                      "\"value\": " + q_value + ",\r\n \"decimals\": " + q_precisions + "\r\n},\r\n \"orderType\": " \
                      "2, \r\n\"price\": {\r\n\"value\": " + p_value + ",\r\n\"decimals\": " + p_precisions + \
                      " \r\n},\r\n \"instrumentId\": " + instrument_id + "\r\n }\r\n }\r\n ]\r\n}"
        else:
            payload = "{\r\n \"jsonrpc\": \"2.0\",\r\n \"method\": \"OrderManagement.Create\",\r\n\"params\": " \
                      "[\r\n {\r\n \"order\": {\r\n \"direction\": " + direction + ",\r\n \"quantity\": {\r\n " \
                      "\"value\": " + q_value + ",\r\n \"decimals\": " + q_precisions + "\r\n },\r\n \"orderType\": " \
                      "1,\r\n \"instrumentId\": " + instrument_id + "\r\n }\r\n }\r\n ]\r\n}"
        try:
            _response = requests.request("POST", self.postman_url, data=payload, headers=self.headers)
            return json.loads(_response.text)
        except AutomationError as e:
            print("{0} create_order failed with error: {1}".format(e.__class__.__name__, e.__cause__))

    # Balance methods
    def get_balance_panel(self):
        payload = "{\r\n \"jsonrpc\": \"2.0\",\r\n \"method\": \"Balance.GetBalancePanel\",\r\n \"params\": []\r\n}"
        try:
            _response = requests.request("POST", self.postman_url, data=payload, headers=self.headers)
            return json.loads(_response.text)
        except AutomationError as e:
            print("{0} get_balance_panel failed with error: {1}".format(e.__class__.__name__, e.__cause__))

    def convert_rate(self, currency_id, currency_id_2):
        payload = "{\r\n \"jsonrpc\": \"2.0\", \r\n \"method\": \"Balance.CurrenciesConverter\", \r\n \"params\": " \
                  "[{\r\n \"CurrencyId\" : [" + currency_id + "],\r\n \"CurrencyTo\": " + currency_id_2 + "\r\n}]\r\n}"
        try:
            _response = requests.request("POST", self.postman_url, data=payload, headers=self.headers)
            return json.loads(_response.text)
        except AutomationError as e:
            print("{0} convert_rate failed with error: {1}".format(e.__class__.__name__, e.__cause__))

    # BalanceService methods
    @staticmethod
    def subtract_balance(customer_id, currency_id, amount):
        payload = "{\r\n\t\"id\": \"1\",\r\n \"jsonrpc\": \"2.0\",\r\n \"method\": \"balance.subtract\",\r\n " \
                  "\"params\":\r\n {\t\r\n \t \"customerId\": " + customer_id + ",\r\n \t \"currencyId\": " + \
                  currency_id + ",\r\n \t \"amount\": " + amount + ",\r\n \t \"metadata\": \r\n \t {\r\n \t " \
                  "\"operationReference\": \"create_order_123\"\r\n \t }\r\n }\r\n}"
        try:
            _response = requests.request("POST", balance_url, data=payload, headers=balance_headers)
            return json.loads(_response.text)
        except AutomationError as e:
            print("{0} subtract_balance failed with error: {1}".format(e.__class__.__name__, e.__cause__))

    @staticmethod
    def add_balance(customer_id, currency_id, deposit_amount):
        payload = "{\r\n\t\"id\": \"1\",\r\n \"jsonrpc\": \"2.0\",\r\n\"method\":\"balance.add\",\r\n \"params\":\r\n" \
                  "{\t\r\n \t \"customerId\": " + customer_id + ",\r\n \t \"currencyId\": " + currency_id + ",\r\n \t" \
                  "\"amount\": " + deposit_amount + ",\r\n \t \"metadata\": \r\n \t {\r\n \t \"operationReference\": " \
                                                                                                                                              "\"create_order_123\"\r\n \t }\r\n}\r\n}"
        try:
            _response = requests.request("POST", balance_url, data=payload, headers=balance_headers)
            return json.loads(_response.text)
        except AutomationError as e:
            print("{0} add_balance failed with error: {1}".format(e.__class__.__name__, e.__cause__))

    @staticmethod
    def get_currency_balance(customer_id, currency_id):
        payload = "{\n \"id\": \"1\",\n \"jsonrpc\":\"2.0\",\n \"method\":\"balance.get\",\n \"params\":\n " \
                  "{\t\n \"customerId\": " + customer_id + ",\n \t\"currencyId\": " + currency_id + "\n }\n}"
        try:
            _response = requests.request("POST", balance_url, data=payload, headers=balance_headers)
            return json.loads(_response.text)
        except AutomationError as e:
            print("{0} get_currency_balance failed with error: {1}".format(e.__class__.__name__, e.__cause__))

    @staticmethod
    def get_all_currencies_balance(customer_id):
        payload = "{\r\n\t\"id\": \"1\",\r\n \"jsonrpc\": \"2.0\",\r\n \"method\": \"balance.getAll\",\r\n " \
                  "\"params\":\r\n {\t\r\n \t \"customerId\": " + customer_id + "\r\n}\r\n}"
        try:
            _response = requests.request("POST", balance_url, data=payload, headers=balance_headers)
            return json.loads(_response.text)
        except AutomationError as e:
            print("{0} get_all_currencies_balance failed with error: {1}".format(e.__class__.__name__, e.__cause__))


# if __name__ == '__main__':
#     postman = PostmanClient(
#         "eyJhbGciOiJIUzUxMiIsInR5cCI6IkpXVCJ9.eyJlbWFpbCI6IkNzZUtFbG9uQ2ljWkBndWVycmlsbGFtYWlsYmxvY2suY29tIiwiZmlyc3ROYW1lIjoiUUF0ZXN0IiwibGFzdE5hbWUiOiJUZXN0UWEiLCJjdXN0b21lcklkIjoiMTAwMDAxMTAwMDAwMDAxNzY3IiwiZXhwIjoxNTQyOTgxNjM0LCJqdGkiOiIxMDAwMDExMDAwMDAwMDE3NjcifQ.arE98w4K1ECsvB9S0bioyO3eBHj089eRwriOwH_zpP6p-qgHXQpfOBn3CjaNW2z-AV-LIEqLXxUdxsKl1EQaGg")
#     response_add = postman.add_credit_card("CseKElonCicZ@guerrillamailblock.com", "0526404096")
#     response_deposit = postman.add_deposit_credit_card('192', '200', '2')
#     balance_response = PostmanClient.add_balance('100001100000001767', '3', '200')
#     cur_balance = PostmanClient.get_currency_balance('100001100000001767', '3')
#     pass
