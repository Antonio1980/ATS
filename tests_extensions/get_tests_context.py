# !/usr/bin/env python
# -*- coding: utf8 -*-

import configparser
import csv


def config_parse(config_file):
    parser = configparser.ConfigParser()
    with open(config_file, mode='r', buffering=-1, encoding=None, errors=None, newline=None, closefd=True) as configfile:
        parser.read(config_file)
        parser.sections()
        return parser


def get_csv_data(data_file):
    rows = []
    with open(data_file, "r") as csv_data:
        content = csv.reader(csv_data)
        next(content, None)
        for row in content:
            rows.append(row)

    return rows


def get_credentials_positive(data_file, row, column1, column2):
    rows = []
    with open(data_file, "r") as csv_data:
        content = csv.reader(csv_data)
        next(content, None)
        for item in content:
            rows.append(item)
    username = rows[row][column1]
    password = rows[row][column2]
    return {'username': username, 'password': password}