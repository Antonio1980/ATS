# !/usr/bin/env python
# -*- coding: utf8 -*-

import codecs
import csv
import configparser


def config_parse(config_file):
    parser = configparser.ConfigParser()
    with open(config_file, mode='r', buffering=-1, closefd=True):
        parser.read(config_file)
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


def write_file_output(process, file):
    with codecs.open(file, "a", "utf-8") as f:
        f.write(process)
        f.flush()





