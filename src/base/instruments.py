import csv
import redis
import codecs
import pymysql
import argparse
import platform
from test_definitions import BaseConfig
from src.base.enums import OperationSystem
from src.base.http_client import APIClient

# API client- connector for TestRail manager.
client = APIClient(BaseConfig.TESTRAIL_URL, BaseConfig.TESTRAIL_USER, BaseConfig.TESTRAIL_PASSWORD)


def update_test_case(test_run, test_case, status):
    """
    Calls API client to send HTTP request.
    :param test_run: current test run.
    :param test_case: current test case.
    :param status: test actual result.
    :return: API response.
    """
    if status == 1:
        # 'add_result_for_case/'-run, -38 / 2590
        return client.send_post(
            'add_result_for_case/' + test_run + '/' + test_case,
            {'status_id': status, 'comment': 'This test ' + test_case + ' PASSED !'}
        )
    else:
        return client.send_post(
            'add_result_for_case/' + test_run + '/' + test_case,
            {'status_id': status, 'comment': 'This test ' + test_case + ' FAILED !'}
        )


def get_test_case(test_case):
    """
    Send GET request to TestRail.
    :param test_case: test case ID.
    :return: API response.
    """
    return client.send_get('get_case/' + test_case)


def run_mysql_query(query):
    """
    To run SQL query on MySQL DB.
    :param query: SQL query.
    :return: data from executed query.
    """
    _host = BaseConfig.DB_HOST
    _db_name = BaseConfig.DB_NAME
    _username = BaseConfig.DB_USERNAME
    _password = BaseConfig.DB_PASSWORD
    _port = 30002
    connection = pymysql.connect(host=_host, port=_port, user=_username, passwd=_password, database=_db_name)
    rows = []
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    finally:
        connection.commit()
        connection.close()
        return rows


def get_redis_value(key, host='10.100.1.11', port='30001'):
    """
    Connects to Redis DB to get value by provided key.
    :param key: second part of the searched key (customer_id).
    :param host: Redis DB host.
    :param port: Redis DB port.
    :return:
    """
    redis_db = redis.StrictRedis(host=host, port=port, db=0)
    value = redis_db.get("phone:confirm:" + key)
    return int(value)


def get_redis_token(tokens_list, customer_id):
    """
    Connect to Redis and search for a key.
    :param tokens_list: list of tokens.
    :param customer_id: string of customer id registered.
    :return: verification token if found.
    """
    redis_db = redis.StrictRedis(host='10.100.1.11', port='30001', db=0)
    if tokens_list is not None:

        def _get_redis_key(key):
            value = redis_db.hgetall(key)
            return value
        for i in tokens_list:
            _key = _get_redis_key(i)
            if len(_key) != 0:
                if int(_key[b'customerId']) == int(customer_id):
                    return i.split('_')[3]
            else:
                continue


def get_redis_keys(key, host='10.100.1.11', port='30001'):
    """
    Connects to Redis DB to get value by provided key.
    :param key: second part of the searched key (customer_id).
    :param host: Redis DB host.
    :param port: Redis DB port.
    :return:
    """
    redis_db = redis.StrictRedis(host=host, port=port, db=0)
    value = redis_db.keys(key)
    return value


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


def get_csv_data(data_file):
    """
    Allows to get data from csv file.
    :param data_file: csv data file.
    :return: list of rows from csv.
    """
    rows = []
    with open(data_file, "r") as csv_data:
        content = csv.reader(csv_data)
        next(content, None)
        for row in content:
            rows.append(row)
    return rows


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
        # To skip first row
        # next(content, None)
        for item in content:
            rows.append(item)
    email = rows[row][column1]
    password = rows[row][column2]
    customer_username = rows[row][column3]
    return {'email': email, 'password': password, 'customer_username': customer_username}


def write_file_output(process, file):
    """
    Allows to write data into a file.
    :param process: python process in 'UTF-8' encoding
    :param file: any file.
    """
    with codecs.open(file, "a", "utf-8") as f:
        f.write(process)
        f.flush()


def write_file_user(result, file):
    """
    Allows to append a string into a file.
    :param result: string to append.
    :param file: file to append for.
    """
    # with open(file, "a") as my_file:
    #     my_file.write(result)
    with open(file, "r+") as f:
        s = f.read()
        f.seek(0)
        f.write(result + s)


def write_file_result(result, file):
    """
    Allows to append a string into a file.
    :param result: string to append.
    :param file: file to append for.
    """
    with open(file, "a") as my_file:
        my_file.write(result)


def detect_os():
    """
    Checks the Operational System.
    :return: String with OS name.
    """
    if _is_mac():
        return OperationSystem.DARWIN.value
    elif _is_win():
        return OperationSystem.WINDOWS.value
    elif _is_lin():
        return OperationSystem.LINUX.value
    else:
        raise Exception("The OS is not detected")


def _is_mac():
    return platform.system().lower() == OperationSystem.DARWIN.value


def _is_win():
    return platform.system().lower() == OperationSystem.WINDOWS.value


def _is_lin():
    return platform.system().lower() == OperationSystem.LINUX.value
