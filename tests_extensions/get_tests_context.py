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
    with open(str(data_file), "r") as csv_data:
        content = csv.reader(csv_data)
        next(content, None)
        for row in content:
            rows.append(row)

    return rows


def get_csv_by_value(data_file):
    with open(data_file, 'r') as f:
        mycsv = csv.reader(f)
        next(mycsv, None)
        mycsv = list(mycsv)
        username = mycsv[0][0]
        password = mycsv[0][1]