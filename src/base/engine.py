import csv
import codecs
import pymysql
import argparse
import platform
import configparser
from src.base.enums import OperationSystem
from src.base.http_client import APIClient
from tests.test_definitions import BaseConfig


client = APIClient(BaseConfig.TESTRAIL_URL, BaseConfig.TESTRAIL_USER, BaseConfig.TESTRAIL_PASSWORD)


def run_mysql_query(self, query):
    _host = BaseConfig.DB_HOST
    _username = BaseConfig.DB_USERNAME
    _password = BaseConfig.DB_PASSWORD
    _db_name = BaseConfig.DB_NAME
    _port = 30002
    connection = pymysql.connect(host=_host, port=_port, user=_username, passwd=_password,
                                 database=_db_name)
    rows = []
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        rows = cursor.fetchall()
    finally:
        connection.commit()
        connection.close()
        return rows


def config_parse(config_file):
    """
    Method allows to get configuration data.
    :param config_file: configuration file.
    :return: configuration data as ConfigParser object.
    """
    parser = configparser.ConfigParser()
    with open(config_file, mode='r', buffering=-1, closefd=True):
        parser.read(config_file)
        return parser


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


def get_crm_credentials_positive(data_file, row, column1, column2):
    """
    Allows to get data from csv file.
    :param data_file: csv data file.
    :param row: specific row in csv file.
    :param column1: first column in csv file.
    :param column2: second column in csv file.
    :return: dictionary object with username and password.
    """
    rows = []
    with open(data_file, "r") as csv_data:
        content = csv.reader(csv_data)
        next(content, None)
        for item in content:
            rows.append(item)
    username = rows[row][column1]
    password = rows[row][column2]
    return {'username': username, 'password': password}


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
        next(content, None)
        for item in content:
            rows.append(item)
    first_last_name = rows[row][column1]
    email = rows[row][column2]
    password = rows[row][column3]
    return {'firstname': first_last_name, 'email': email, 'password': password}


def write_file_output(process, file):
    """
    Allows to write data into a file.
    :param process: python process in 'UTF-8' encoding
    :param file: any file.
    """
    with codecs.open(file, "a", "utf-8") as f:
        f.write(process)
        f.flush()


def write_file_result(result, file):
    """
    Allows to append a string into a file.
    :param result: string to append.
    :param file: file to append for.
    """
    with open(file, "a") as myfile:
        myfile.write(result)


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


def update_test_case(test_run, test_case, status):
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
    case = client.send_get('get_case/' + test_case)
    return case
