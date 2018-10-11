"""
Author: Anton Shipulin.
Created: 01.08.2018
Version: 1.05
"""

import re
import csv
import json
import math
import redis
import arrow
import codecs
import random
import string
import pymysql
import argparse
import platform
import requests
import warnings
import phonenumbers
from faker import Faker
from bs4 import BeautifulSoup
from phonenumbers import carrier
from test_definitions import BaseConfig
from src.base.enums import OperationSystem
from src.base.http_client import HTTPClient
from phonenumbers.phonenumberutil import number_type


class Instruments(object):
    # API client- connector for TestRail manager.
    testrail_client = HTTPClient(BaseConfig.TESTRAIL_URL)
    # API client- connector for Guerrilla mail service.
    guerrilla_client = HTTPClient(BaseConfig.GUERRILLA_API)
    # Redis client- connector for Redis DB.
    redis_client = redis.StrictRedis(host=BaseConfig.REDIS_HOST, port=BaseConfig.REDIS_PORT, db=0)

    @staticmethod
    def calculate_decimal_price(x, y):
        return x / math.pow(10, y)

    @staticmethod
    def run_mysql_query(query):
        """
        To run SQL query on MySQL DB.
        :param query: SQL query.
        :return: data from executed query.
        """
        # Ignore "Not closed socket connection" warning.
        warnings.simplefilter("ignore", ResourceWarning)
        # SQL client- connector for MySQL DB.
        connection = pymysql.connect(host=BaseConfig.SQL_HOST, port=int(BaseConfig.SQL_PORT),
                                     user=BaseConfig.SQL_USERNAME, passwd=BaseConfig.SQL_PASSWORD,
                                     database=BaseConfig.SQL_DB, charset='utf8mb4', autocommit=True)
        try:
            with connection.cursor() as cursor:
                cursor.execute(query)
                rows = cursor.fetchall()
                cursor.close()
                if rows:
                    return rows
        finally:
            connection.close()

    @staticmethod
    def get_guerrilla_mail(method, uri=None, _token=None):
        """
        Runs HTTP requests front of Guerrilla API.
        :param method:
        :param uri: API action to perform.
        :param _token: API token header.
        :return: API _response as a json object.
        """
        _response = None
        guerrilla_base_url = "https://www.guerrillamail.com/ajax.php?f="
        url = guerrilla_base_url + uri
        if _token is None:
            _headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                'Content-Type': 'application/json'}
        else:
            _headers = {
                'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_10_1) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/39.0.2171.95 Safari/537.36',
                'Content-Type': 'application/json', 'Cookie': "PHPSESSID=" + _token}
        if method.lower() == "get":
            _response = requests.request("GET", url, headers=_headers)
        elif method.lower() == "post":
            _response = requests.request("POST", url, headers=_headers)
        return json.loads(_response.text)

    @staticmethod
    def email_generator(size=8, chars=string.ascii_lowercase + string.digits):
        """
        Generates random string with chars and digits.
        :param size: string length expected (default is 8).
        :param chars: string characters consistency.
        :return: random string.
        """
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def generate_random_num(size=8, chars=string.digits):
        """
        Generates random number with digits.
        :param size: string length expected (default is 8).
        :param chars: numbers characters consistency.
        :return: random number.
        """
        return ''.join(random.choice(chars) for _ in range(size))

    @staticmethod
    def parse_redis_token(tokens, pattern):
        """
        Parser for Redis token (splitter).
        :param tokens: list of tokens as is (from Redis).
        :param pattern: regex pattern.
        :return: list of cleared tokens.
        """
        temp, temp1, temp2 = [], [], []
        for i in tokens:
            i = str(i)
            temp.append(i.split(pattern))
        for j in temp:
            for k in j[::1]:
                temp1.append(k)
        while '' in temp1:
            temp1.remove('')
        for x in temp1:
            temp2.append(x[:-1])
        return temp2

    @staticmethod
    def parse_args(run_number):
        """
        Allows to pass data to TestRail as arguments.
        :param run_number: test run in TestRail.
        :return: array of arguments.
        """
        parser = argparse.ArgumentParser()
        parser.add_argument('-run', '-' + run_number)
        args = parser.parse_args()
        return args

    @staticmethod
    def parse_html(html):
        """
        HTML parser, converts a string (if it html content) to HTML object.
        :param html: string with html content.
        :return: HTML object.
        """
        return BeautifulSoup(html, 'html.parser')

    @staticmethod
    def get_csv_data(data_file):
        """
        Allows to get data from csv file.
        :param data_file: csv data file.
        :return: list of rows from csv.
        """
        rows = []
        with open(data_file, "r") as csv_data:
            content = csv.reader(csv_data)
            # skipping first row
            next(content, None)
            for row in content:
                rows.append(row)
        return rows

    @staticmethod
    def get_account_details(data_file, row, column1, column2, column3):
        """
        Allows to get data from csv file.
        :param data_file: csv data file.
        :param row: specific row in csv file.
        :param column1: first column in csv file.
        :param column2: second column in csv file.
        :param column3: third column in csv file.
        :return: dictionary object with username and password.
        """
        rows = []
        with open(data_file, "r") as csv_data:
            content = csv.reader(csv_data)
            for item in content:
                rows.append(item)
        email = rows[row][column1]
        password = rows[row][column2]
        customer_username = rows[row][column3]
        return {'email': email, 'password': password, 'customer_username': customer_username}

    @staticmethod
    def write_file_output(process, file):
        """
        Allows to write data into a file.
        :param process: python process in 'UTF-8' encoding
        :param file: any file.
        """
        with codecs.open(file, "a", "utf-8") as f:
            f.write(process)
            f.flush()

    @staticmethod
    def write_file_user(result, file):
        """
        Allows to append a string into a file.
        :param result: string to append.
        :param file: file to append for.
        """
        with open(file, "r+") as f:
            s = f.read()
            f.seek(0)
            f.write(result + s)

    @staticmethod
    def write_file_result(result, file):
        """
        Allows to append a string into a file.
        :param result: string to append.
        :param file: file to append for.
        """
        with open(file, "a") as my_file:
            my_file.write(result)

    @staticmethod
    def check_phone_number(phone_number):
        """
        Utility to check if passed phone number is valid number.
        :param phone_number: phone number to check.
        :return: True if number is valid and False otherwise.
        """
        return carrier._is_mobile(number_type(phonenumbers.parse(phone_number)))

    @staticmethod
    def generate_phone_number():
        """
        Creates random valid phone number.
        :return: phone number as a string.
        """
        fake = Faker()
        pure_phone = fake.phone_number()
        if 'x' in pure_phone:
            phone = pure_phone.split('x')[0]
        elif '(' or ')' in pure_phone:
            phone = re.sub('[()]', '', pure_phone)
        else:
            phone = pure_phone
        return phone

    @staticmethod
    def generate_user_first_last_name():
        """
        Creates random user first_last_name.
        :return: user first_last_name as a string.
        """
        fake = Faker()
        return '_'.join(fake.name().split(' '))

    @staticmethod
    def generate_pure_user_first_last_name():
        """
        Creates random user first and last_name.
        :return: user first_last_name as a string.
        """
        fake = Faker()
        return fake.name()

    @staticmethod
    def detect_os():
        """
        Detects the OS on which Python tests will run.
        :return: enum string value of OS name.
        """
        def _is_mac():
            return platform.system().lower() == OperationSystem.DARWIN.value

        def _is_win():
            return platform.system().lower() == OperationSystem.WINDOWS.value

        def _is_lin():
            return platform.system().lower() == OperationSystem.LINUX.value

        if _is_mac():
            return OperationSystem.DARWIN.value
        elif _is_win():
            return OperationSystem.WINDOWS.value
        elif _is_lin():
            return OperationSystem.LINUX.value
        else:
            raise Exception("The OS is not detected")

    @classmethod
    def write_file_preconditions(cls, rows, email_suffix):
        """
        Allows to create crm_users_preconditions.csv file with random data.
        :param rows: rows number to create.
        :param email_suffix: email service provider.
        """
        language, permissions, status, user_type = "eng", "sup", "act", "Admin"
        header = "first_last_name,phone,email,username,language,permissions,status,user_type\n"
        file = BaseConfig.CRM_USERS_PRECONDITIONS
        with open(file, "w") as f:
            f.write(header)
        with open(file, "a") as my_file:
            for i in range(rows):
                first_last_name = cls.generate_user_first_last_name()
                phone = cls.generate_phone_number()
                email = first_last_name + email_suffix
                username = first_last_name
                body = "{0},{1},{2},{3},{4},{5},{6},{7}\n".format(first_last_name, phone, email, username, language,
                                                                  permissions, status, user_type)
                my_file.write(body)

    @classmethod
    def set_guerrilla_email(cls, _username, _token=None):
        """
        Send POST request with given email address to guerrilla API.
        :param _username: given username to set.
        :param _token: API token.
        :return: API response as Json.
        """
        return cls.guerrilla_client.send_post('set_email_user', {'email_user': _username,
                                                                 'lang': 'en', 'site': 'guerrillamail.com'}, _token)

    @classmethod
    def get_guerrilla_emails(cls, _username, _token):
        """
        Get list of mails from guerrilla API.
        :param _username:
        :param _token:
        :return:
        """
        return cls.guerrilla_client.send_get('get_email_list&offset=0&site=guerrillamail.com&_=' + _username, _token)

    @classmethod
    def check_guerrilla_email(cls, _time_stamp, _token):
        """
        Get list of mails from guerrilla API.
        :param _time_stamp: email time-stamp passes as part of url.
        :param _token: guerrilla API token.
        :return:
        """
        return cls.guerrilla_client.send_get('check_email&seq=1&site=guerrillamail.com&_=' + _time_stamp, _token)

    @classmethod
    def get_last_guerrilla_email(cls, _time_stamp, mail_id, _token):
        """
        Get last email from guerrilla API.
        :param _time_stamp: email time-stamp passes as part of url.
        :param mail_id: email-id passes as part of url.
        :param _token: guerrilla API token.
        :return:
        """
        return cls.guerrilla_client.send_get('fetch_email&email_id=mr_' + mail_id + '&site=guerrillamail.com&_=' +
                                             _time_stamp, _token)

    @classmethod
    def get_guerrilla_email(cls):
        """
        Generates random email from guerrilla API.
        :return: new random email address.
        """
        return cls.guerrilla_client.send_get('get_email_address')

    @classmethod
    def update_test_case(cls, test_run, test_case, status):
        """
        Calls API client to send HTTP request.
        :param test_run: current test run.
        :param test_case: current test case.
        :param status: test actual result.
        :return: API response.
        """
        if status == 1:
            # 'add_result_for_case/'-run, -38 / 2590
            return cls.testrail_client.send_post('add_result_for_case/' + test_run + '/' + test_case,
                                                 {'status_id': status,
                                                  'comment': 'This test ' + test_case + ' PASSED !'})
        else:
            return cls.testrail_client.send_post('add_result_for_case/' + test_run + '/' + test_case,
                                                 {'status_id': status,
                                                  'comment': 'This test ' + test_case + ' FAILED !'})

    @classmethod
    def get_test_case(cls, test_case):
        """
        Send GET request to TestRail.
        :param test_case: test case ID.
        :return: API response.
        """
        return cls.testrail_client.send_get('get_case/' + test_case)

    @classmethod
    def get_redis_value(cls, key):
        """
        Connects to Redis DB to get value by provided key.
        :param key: second part of the searched key (customer_id).
        :param host: Redis DB host.
        :param port: Redis DB port.
        :return:
        """
        value = cls.redis_client.get("phone:confirm:" + key)
        return int(value)

    @classmethod
    def get_redis_token(cls, tokens_list, customer_id):
        """
        Connect to Redis and search for a key.
        :param tokens_list: list of tokens.
        :param customer_id: string of customer id registered.
        :return: verification token if found.
        """
        if tokens_list is not None:
            def _get_redis_key(key):
                return cls.redis_client.hgetall(key)

            for i in tokens_list:
                _key = _get_redis_key(i)
                if len(_key) != 0:
                    if int(_key[b'customerId']) == int(customer_id):
                        return i.split('_')[3]
                else:
                    continue

    @classmethod
    def get_redis_keys(cls, key):
        """
        Connects to Redis DB to get value by provided key.
        :param key: second part of the searched key (customer_id).
        :return: list of all keys.
        """
        return cls.redis_client.keys(key)

    """
    Author: Christina Koch.
    Created: 20.08.2018
    """
    @classmethod
    def add_customer_balance(cls, customer_id, currency_id, amount):
        """
        Connects to Redis DB to set value by provided key:_customer_id.
        :param customer_id: redis DB key.
        :param currency_id: Id of currency for balance.
        :param amount: amount of deposit.
        """
        customer_id, cur_balance = str(customer_id), None
        cur_balance = cls.redis_client.hget('balance_' + customer_id, currency_id)
        added_balance = cls.redis_client.hincrby('balance_' + customer_id, currency_id, amount)
        cur_balance = 0 if cur_balance is None else int(cur_balance)
        if added_balance == cur_balance + int(amount):
            print("Balance was added successfully, current balance: ", added_balance)
            return True
        else:
            print("Error occurred...")
            return False

    @classmethod
    def add_customer_deposit(cls, customer_id, currency_id, amount):
        """
        Connects to SQL DB and inserts value for provided customer_id.
        :param customer_id: Id of customer for insert.
        :param currency_id: Id of currency for balance.
        :param amount: amount of deposit to insert.
        :return: True if all successful and False otherwise.
        """
        customer_id, currency_id, amount = str(customer_id), str(currency_id), str(amount)
        date = arrow.utcnow()
        _ = "0000-00-00 00:00:00"
        cur_date = date.format('YYYY-MM-DD')
        cur_date_full = date.format('YYYY-MM-DD HH:mm:ss')
        id = cls.generate_random_num(6)
        query = "INSERT INTO deposits(id, customerId, paymentMethodId, clearingCompanyId, currencyId, amount, rateUSD,"\
                "rateEUR, rateBTC, referenceNumber, statusId, sourceId, IPAddress, balanceChangeTransactionGuid, " \
                "comments, canceledByWId, cancelingWId, addedBy, updatedBy, confirmedBy, canceledBy, cancelReasonId, " \
                "cancelReason, declinedBy, declineReason, dateConfirmed, dateValue, dateCanceled, dateDeclined, " \
                "dateInserted, dateUpdated) VALUES(" + id + ", " + customer_id + ", 3, 0, " + currency_id + ", " + \
                amount + ", 0.00012500, 0.00014388, 1.00000000, '2134776', 2, 3, '10.244.10.1', '', '', 0, 0, 9, 9, 9,"\
                "0, 0, '', 0, '', '" + cur_date_full + "', '" + cur_date + "', '" + _ + "', '" + _ + "', '" + \
                cur_date_full + "', '" + cur_date_full + "');"
        cls.run_mysql_query(query)
        print("Deposit {0} was added successfully, for customer:  ".format(amount), customer_id)
        return True

    @classmethod
    def add_customer_deposit_balance(cls, customer_id, currency_id, amount):
        """
        Inserts given amount into Redis and SQL DB.
        :param customer_id: Id of customer for insert.
        :param currency_id: Id of currency for balance.
        :param amount: amount of deposit to insert.
        :return: True if all successful and False otherwise.
        """
        if cls.add_customer_balance(customer_id, currency_id, amount):
            if cls.add_customer_deposit(customer_id, currency_id, amount):
                print("Deposit was added into customer- {0} balance successfully, current deposit: ".format(
                    customer_id), amount)
                return True
            else:
                print("Error occurred with add_customer_balance...")
        else:
            print("Error occurred with add_customer_balance...")


if __name__ == '__main__':
    res = Instruments.calculate_decimal_price(140, 2)
    print(res)
#     res = Instruments.start_selenium_server()
#     print(res)
    # res = Instruments.add_customer_balance(100001100000001021, 5, 150000)
    # res = Instruments.add_customer_deposit_balance(100001100000001221, 3, 150000)
    # res = Instruments.add_customer_deposit(100001100000000966, 5, 150000.00000000)
    # print(res)
    # res = Instruments.run_mysql_query("""INSERT INTO deposits VALUES(1216, 100001100000000966, 3, 0, 5, 150000.00000000, 0.00012500, 0.00014388, 1.00000000, 2134776, 2, 3, '10.244.10.1', '', 0, 0, 9, 9, 9, 0, 0, NULL, 0, NULL, '2018-09-03 08:34:07', '2018-09-03', '0000-00-00 00:00:00', '0000-00-00 00:00:00', '2018-09-03 08:34:07', '2018-09-03 08:34:07');""")
    # print(res)
    # res = Instruments.add_customer_balance('100001100000000966', '5', '150000')
    # print(res)
#     parsed_html = Instruments.parse_html('<table><tr><td>Dear Brianna Smith Brianna Smith</td></tr><tr><td>Your new password for the DX.exchange is: <span>oohQ9FtG2T</span></td></tr><tr><td>This is a temporary password for the next 24 hours.</td></tr><tr><td>Click <a href="http://staging-crm.dx.exchange/dx/login/">here</a> to login_positive to the CRM with the temporary password.</td></tr><tr><td>Upon login_positive, you will be asked to change the password to a permanent one.</td></tr></table>')
#     new_pass = parsed_html.table.find_all('td')[1].span.string
#     print(new_pass)
#     new_password = parsed_html.tbody.find_all('td')[2]['span']
#     instruments = Instruments()
#     instruments.write_file_preconditions(10, "@mailinator.com")
#     res = instruments.get_test_case('2590')
#     print(res)
#     res2 = instruments.update_test_case('41', '2590', 1)
#     print(res2)
#     t = Instruments.generate_token()
#     print(t)
#     username = Instruments.generate_user_first_last_name()
#     print(username)
#     response = Instruments.get_guerrilla_email()
#     print(response)
#     email = response[1]['email_addr']
#     sid_token = response[1]['sid_token']
#     time_stamp = str(response[1]['email_timestamp'])
#     response2 = Instruments.check_guerrilla_email(time_stamp, sid_token)
#     print(response2)
#     sid_token = response2[1]['sid_token']
#     post_response = Instruments.set_guerrilla_email(username)
#     print("SET",post_response)
#     sid_token = post_response[2].split('=')[1].split(';')[0]
#     time_stamp = str(post_response[1]['email_timestamp'])
#     get_response = Instruments.get_guerrilla_emails(username, sid_token)
#     print(get_response)
#     sid_token = get_response[1]['sid_token']
#     mail_id = str(get_response[1]['list'][0]['mail_id'])
#     print("mail_id...", mail_id)
#     response3 = Instruments.get_last_guerrilla_email(time_stamp, mail_id, sid_token)
#     print(response3)
