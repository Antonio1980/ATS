# !/usr/bin/env python
# -*- coding: utf8 -*-

import csv
import codecs
import argparse
import configparser


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


def get_account_details(data_file, row, column1, column2, column3, column4):
    """
    Allows to get data from csv file.
    :param data_file: csv data file.
    :param row: specific row in csv file.
    :param column1: first column in csv file.
    :param column2: second column in csv file.
    :param column3: third column in csv file.
    :param column4: fourth column in csv file.
    :return: dictionary object with username and password.
    """
    rows = []
    with open(data_file, "r") as csv_data:
        content = csv.reader(csv_data)
        next(content, None)
        for item in content:
            rows.append(item)
    firstname = rows[row][column1]
    lastname = rows[row][column2]
    email = rows[row][column3]
    password = rows[row][column4]
    return {'firstname': firstname, 'lastname': lastname, 'email': email, 'password': password}


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